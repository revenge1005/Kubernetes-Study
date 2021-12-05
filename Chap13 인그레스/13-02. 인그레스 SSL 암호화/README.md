
# 1. ingress-tls.yml

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-ingress
  annotations:
    kubernetes.io/ingress.class: 'nginx'
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'   # (1) 리다이렉트

spec:
  tls:                # (2) 암호화 설정 섹션
  - hosts:
    - abc.sample.com  # (3) 도메인 명
    secretName: tls-certificate  # (3) 서버 인증서

  rules:
  - host: abc.sample.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: helloworld-svc
            port:
              number: 8080
      - path: /apl2
        pathType: Prefix
        backend:
          service:
            name: nginx-svc
            port:
              number: 9080
  - host: xyz.sample.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: java-svc
            port:
              number: 9080

```

# 2. 자체 서명 인증성 생성

```
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx-selfsigned.key -out ngin-selfsigned.crt
Generating a RSA private key
...+++++
.........................+++++
writing new private key to 'nginx-selfsigned.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:
Email Address []:
```

# 3. 자체 서명 인증서를 시크릿에 보관

```
$ kubectl create secret tls tls-certificate --key nginx-selfsigned.key --cert nginx-selfsigned.crt
secret/tls-certificate created

$ kubectl get secrets
NAME                  TYPE                                  DATA   AGE
default-token-62jwj   kubernetes.io/service-account-token   3      37d
tls-certificate       kubernetes.io/tls                     2      7s
```

# 4. 보안 프로토콜을 적용한 인그레스 생성과 확인

```
$ kubectl apply -f ingress-tls.yml
ingress.networking.k8s.io/hello-ingress configured


## abc.sample.com의 도메인과 대응하는 시크릿의 이름이 출력되어 정상적으로 매니페스트가 적용된 것을 알 수 있다.
$ kubectl describe ingress
Name:             hello-ingress
Namespace:        default
Address:          192.168.219.11
Default backend:  default-http-backend:80 (<error: endpoints "default-http-backend" not found>)
TLS:
  tls-certificate terminates abc.sample.com   ## 이 부분에 주목
Rules:
  Host            Path  Backends
  ----            ----  --------
  abc.sample.com
                  /       helloworld-svc:8080 (10.40.0.2:80)
                  /apl2   nginx-svc:9080 (10.32.0.3:80,10.32.0.5:80,10.40.0.3:80)
  xyz.sample.com
                  /   java-svc:9080 (10.40.0.4:9080)
Annotations:      kubernetes.io/ingress.class: nginx
                  nginx.ingress.kubernetes.io/force-ssl-redirect: true
                  nginx.ingress.kubernetes.io/rewrite-target: /
Events:
  Type    Reason  Age                From                      Message
  ----    ------  ----               ----                      -------
  Normal  Sync    20s (x3 over 38m)  nginx-ingress-controller  Scheduled for sync


## 443 -> 30257 포트로 접근
$ kubectl get svc -n ingress-nginx
NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller             NodePort    10.100.151.240   <none>        80:32209/TCP,443:30257/TCP   77m
ingress-nginx-controller-admission   ClusterIP   10.109.248.125   <none>        443/TCP                      77m
```

