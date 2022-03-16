----

# 1. 시크릿과 컨피그맵

+ 애플리케이션의 설정 정보나 패스워드와 같은 인증 정보는 컨테이너에 담지 않고 분리하여 네임스페이스에 저장하고 컨테이너가 읽도록 해야 한다.

+ 그러면 테스트 환경과 프로덕션 환경별로 컨테이너를 별도로 빌드할 필요가 없게 된다.

+ 네임스페이스에 저장한 설정 정보를 "컨피그맵(ConfigMap)", 인증 정보와 같이 보안이 필요한 정보를 네임스페이스에 저장한 것을 "시크릿(Secret)"이라 한다.

    - 컨테이너에서는 이들 오브젝트를 파일 시스템으로 마운트하여 파일로 읽거나 환경 변수로 참조할 수 있다.

<br>

----

# 2. 시크릿 특징

+ 시크릿은 패스워드, 토큰, 키 처럼 보안이 필요한 데이터를 저장하는데 사용한다.

    - 보안 데이터의 노출 리스크를 줄이기 위해 사용하며, 사이즈는 1MB 미만이어야 한다.

+ 서비스 어카운트를 만들면 서비스 어카운트의 토큰을 담은 시크릿이 네임스페이스에 자동으로 생성된다.

    - 해당 토큰은 RBAC 기반의 접근 제어에 사용된다.

+ 사용자가 시크릿을 등록하면 파드의 환경 변수나 마운트된 볼륨의 파일을 통해 접근할 수 있다.

+ 시크릿은 네임스페이스에 속하며, 다른 네임스페이스에서는 읽을 수 없다.

+ 시크릿 자체는 암호화와는 직접적인 관계가 없으며 벤더가 제공하는 추가적인 암호화 기능을 사용할 수 있다.

+ 파드가 시크릿을 사용하도록 설정했으면 기동하기 전에 시크릿이 존재해야 한다.

<br>

----

# 3. 시크릿 사용 사례

+ 테스트 환경에서 테스트를 통과한 애플리케이션의 이미지는 가능하면 다시 빌드하지 않고 운영 환경에 배포하는 것이 좋다.

    - 컨테이너의 이미지에 테스트용 DB에 대한 ID와 PW 정보가 담겨 있으면 운영 환경에 배포하기 전에 값을 바꾸고 다시 빌드해야만 한다.

    - 이렇게 되면 컨테이너의 불변성이라는 특징을 살릴 수 없으며 의도치 않는 문제가 발생할 수 있다.

+ 이런 경우, 테스트 환경과 운영 환경 각각의 네임스페이스에 시크릿을 만들어 ID와 PW를 저장하도록 한다.

    - 컨테이너에서는 등록된 시크릿을 환경 변수로 읽도록 구현한다.

    - 그러면 응용 프로그램의 이미지를 다시 빌들할 필요 없이 배포하는 것이 가능하다.

----

## (1) 시크릿 등록
```bash
### 시크릿에 등록할 문자열 Base64 인코딩
$ echo -n 'test' | base64
dGVzdA==

$ echo -n 'password' | base64
cGFzc3dvcmQ=
```
```yaml
### DB 사용자 ID와 PW를 시크릿으로 등록하는 매니페스트: db_credentials.yml
apiVersion: v1
kind: Secret
metadata:
    name: db-credentials
type: Opaque
data:
    username: dGVzdA==
    password: cGFzc3dvcmQ=
```
```bash
$ kubectl apply -f db_credentials.yml
secret/db-credentials created

$ kubectl get -f db_credentials.yml
NAME             TYPE     DATA   AGE
db-credentials   Opaque   2      44s
```

## (2) 시크릿이 담긴 환경 변수 출력
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-apl
spec:
  containers:
  - name: nginx
    image: nginx
    env:
      - name: DB_USERNAME ## 환경 변수
        valueFrom:
          secretKeyRef:
            name: db-credentials ## 시크릿명
            key: username ## 시크릿 키
      - name: DB_PASSWORD ## 환경 변수
        valueFrom:
          secretKeyRef:
            name: db-credentials
            key: password
```
```bash
$ kubectl apply -f reg_secret_env.yml
pod/web-apl created

$ kubectl get pod
NAME      READY   STATUS    RESTARTS   AGE
web-apl   1/1     Running   0          28s

$ kubectl exec -it web-apl -- bash -c 'echo $DB_USERNAME, $DB_PASSWORD'
test, password
```

## (3) 시크릿에 TLS 인증서와 키 파일 등록
```bash
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout selfsigned.key -out selfsigned.crt

$ ls
selfsigned.crt  selfsigned.key

$ kubectl create secret tls www-cert --cert=selfsigned.crt --key=selfsigned.key
secret/www-cert created

$ kubectl get secrets www-cert
NAME       TYPE                DATA   AGE
www-cert   kubernetes.io/tls   2      9s

$ kubectl describe secrets www-cert
Name:         www-cert
Namespace:    prod
Labels:       <none>
Annotations:  <none>

Type:  kubernetes.io/tls

Data
====
tls.crt:  1245 bytes
tls.key:  1704 bytes
```
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - protocol: TCP
      containerPort: 443
    volumeMounts: ## 마운트 정의
    - name: cert-vol ## 시크릿의 볼륨 이름
      mountPath: /etc/cert ## 컨테이너상의 마운트 경로
  volumes: ## 볼륨 정의
  - name: cert-vol ## 시크릿의 볼륨 이름
    secret:
      secretName: www-cert ## 시크릿의 이름
```
```
$ kubectl get pod
NAME   READY   STATUS    RESTARTS   AGE
web    1/1     Running   0          21s

$ kubectl exec -it web -- df -h
Filesystem                   Size  Used Avail Use% Mounted on
overlay                      9.8G  1.9G  7.4G  21% /
tmpfs                         64M     0   64M   0% /dev
tmpfs                        980M     0  980M   0% /sys/fs/cgroup
tmpfs                        1.9G  8.0K  1.9G   1% /etc/cert
/dev/mapper/ubuntu--lvm-var  9.8G  1.9G  7.4G  21% /etc/hosts
shm                           64M     0   64M   0% /dev/shm
tmpfs                        1.9G   12K  1.9G   1% /run/secrets/kubernetes.io/serviceaccount
tmpfs                        980M     0  980M   0% /proc/acpi
tmpfs                        980M     0  980M   0% /proc/scsi
tmpfs                        980M     0  980M   0% /sys/firmware

$ kubectl exec -it web -- ls /etc/cert
tls.crt  tls.key
```

<br>

----

# 4. 컨피그맵

+ 시크릿은 보안이 필요한 정보를 저장하여 참조를 제한하는 반면, 컨피그맵은 네임스페이스에 설정 정보를 저장하고 공유하는 것을 목적으로 한다.

+ <컨피그맵 특징>

    - 컨피그맵을 등록할 때는 시키릿처럼 값을 Base64로 인코딩하지 않아도 된다.

    - 컨피그맵의 경우 'kubectl describe configmap'으로 내용 표시

    - 시크릿과 컨피그맵은 정기적으로 갱신이 체크되며, 볼륨으로 마운트된 경우에도 kubelet의 갱신 주기에 따른 지연이 있기는 하지만 자동으로 갱신됨

    - 클러스터 롤 view의 대상 리소스에 시키릿은 포함되지 않지만, 컨피그맵은 포함된다. (즉, 참조 권한만으로도 컨피그맵의 내용 참조 가능)

<br>

----

# 5. 컨피그맵 실습

+ Nginx의 SSL/TLS 설정 파일을 컨피그맵에 등록

+ Nginx의 공식 이미지에서 설정 파일은 '/etc/nginx/conf.d'에 배치하면 된다.


## (1) 설정 파일을 일괄로 컨피그맵에 등록
```
$ kubectl create configmap nginx-conf --from-file=tls.conf
configmap/nginx-conf created


$ kubectl get configmaps nginx-conf
NAME         DATA   AGE
nginx-conf   1      7s


$ kubectl describe configmaps nginx-conf
Name:         nginx-conf
Namespace:    prod
Labels:       <none>
Annotations:  <none>

Data
====
tls.conf:
----
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
server {
    listen 443 ssl;
    server_name www.sample.com;
    ssl_certificate /etc/cert/tls.crt;
    ssl_certificate_key /etc/cert/tls.key;
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}
```

## (2) 파드에서 컨피그맵의 값을 환경 변수로 읽기

+ cm-env.yml

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config
data:
  log_level: INFO
```

+ cm-env-read.yml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-apl
spec:
  containers:
  - name: web
    image: nginx
    env:
    - name: LOG_LEVEL ## 컨테이너 환경 변수명
      valueFrom:
        configMapKeyRef:
          name: env-config ## 컨피그맵명
          key: log_level ## 키 항목
```
+ 환경 변수 LOG_LEVEL에 INFO란 값이 있음을 알 수 있다.

```
$ kubectl apply -f cm-env.yml
configmap/env-config created

$ kubectl apply -f cm-env-read.yml
pod/web-apl created

$ kubectl exec -it web-apl env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=web-apl
TERM=xterm
LOG_LEVEL=INFO             <<---- 환경 변수 LOG_LEVEL
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
NGINX_VERSION=1.21.4
NJS_VERSION=0.7.0
PKG_RELEASE=1~bullseye
HOME=/root
```