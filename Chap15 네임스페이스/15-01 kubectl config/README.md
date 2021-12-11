----

> # 1. kubectl config

+ kubectl을 사용할 때 네임스페이스를 지정하려면 "-n <네임스페이스명>"을 사용한다.

+ 이러한 옵션을 지정하지 않고 kubectl의 기본으로 사용하는 네임스페이스를 바꾸려면 "kubectl config"를 사용하면 된다.

+ 그러면 여러 개의 k8s 클러스터 중에서 조작할 클러스터와 그 네임스페스를 지정할 수 있다.

|커맨드|설명|
|------|---|
|kubectl get namespce|네임스페이스 목록 출력|
|kubectl config view|config 파일에 등록된 정보 출력|
|kubectl config get-contexts|Context 목록 출력|
|kubectl config set-context|Context 설정|
|kubectl config set-context \<Context명\> --namespace=\<네임스페이스명\> <br> --cluster=\<클러스터명\> --user=\<유저명\> |K8s 클러스터명, 네임스페이스, 유저를 조합하여 Context 작성|
|kubectl config current-context|현재 사용 중인 Context 표시|

<br>

----

> # 2. 조작할 k8s 클러스터와 네임스페이스를 교체

+ kubectl config는 마스터에 대한 접근 정보를 기반으로 하며, kubectl이 마스터에 대한 정보를 얻는 방법은 다음과 같다.

    - ① 실행 시 옵션으로 지정 '-kubeconfig <config_파일_경로>'

    - ② 홈 디렉토리 밑의 '.kube/config' 참조

    - ③ 환경 변수 KUBECONFIG에 지정된 경로 참조

----

## (1) 실습 환경

![01](https://user-images.githubusercontent.com/42735894/145680011-3b6d9cd3-7c22-4f07-9246-375b1d0b98c9.PNG)

----

## (2) k8s 클러스터 컨텍스트 변경

+ **첫 번째 클러스터 .kube/config 파일 변경**

```bash
$ kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO        NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin

$ vim .kube/config
```
```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: REDACTED
    server: https://192.168.219.10:6443
  name: k8s-cluster01                                 ## 변경 (1)
contexts:
- context:
    cluster: k8s-cluster01                            ## 변경 (2)
    user: k8s-cluster01-admin                         ## 변경 (3)
  name: kk8s-cluster01-admin@k8s-cluster01            ## 변경 (3)
current-context: k8s-cluster01-admin@k8s-cluster01    ## 변경 (4)
kind: Config
preferences: {}
users:
- name: help
  user:
    as-user-extra: {}
- name: k8s-cluster01-admin                           ## 변경 (5)
  user:
    client-certificate-data: REDACTED 
    client-key-data: REDACTED
```
```bash
$ systemctl daemon-reload

$ systemctl restart kubelet

## 변경된 것을 확인
$ kubectl config get-contexts
CURRENT   NAME                                CLUSTER         AUTHINFO              NAMESPACE
*         k8s-cluster01-admin@k8s-cluster01   k8s-cluster01   k8s-cluster01-admin
```

+ **마찬가지로 두 번째 클러스터도 변경하면 아래와 같다.**

```bash
$ kubectl config get-contexts
CURRENT   NAME                                CLUSTER         AUTHINFO              NAMESPACE
*         k8s-cluster02-admin@k8s-cluster02   k8s-cluster02   k8s-cluster02-admin
```
----

## (3) kubectl을 통한 multi-cluster 접속

+ 각 클러스터마다 config를 수정하여 이름 부분이 변경되었다면, 양쪽 클러스터에 모두 접속할 수 있는 kubectl 클러스터 계정의 config 파일에 또 다른 클러스터의 config 내용을 병합하여 아래와 같이 변경해둔다.

```bash
root@k8s-master:~# cp .kube/config .kube/config.old

root@k8s-master:~# vim .kube/config
```

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: REDACTED
    server: https://192.168.219.10:6443
  name: k8s-cluster01                                 
- cluster:                       ## 추가 (1)
    certificate-authority-data: REDACTED
    server: https://192.168.219.10:6443
  name: k8s-cluster02                                 
contexts:
- context:
    cluster: k8s-cluster01                            
    user: k8s-cluster01-admin                         
  name: kk8s-cluster01-admin@k8s-cluster01            
- context:                       ## 추가 (2)
    cluster: k8s-cluster02                            
    user: k8s-cluster02-admin                         
  name: kk8s-cluster02-admin@k8s-cluster02            
current-context: k8s-cluster01-admin@k8s-cluster01
kind: Config
preferences: {}
users:
- name: help
  user:
    as-user-extra: {}
- name: k8s-cluster01-admin                           
  user:
    client-certificate-data: REDACTED 
    client-key-data: REDACTED
- name: k8s-cluster02-admin       ## 추가 (3)                  
  user:
    client-certificate-data: REDACTED 
    client-key-data: REDACTED
```

+ **이제 다음과 같이 두 개의 클러스터를 전환하면서 kubectl 명령을 사용할 수 있게 된다.**

```bash
root@k8s-master:~# systemctl daemon-reload

root@k8s-master:~# systemctl restart kubelet.service

root@k8s-master:~# kubectl config get-contexts
CURRENT   NAME                                CLUSTER         AUTHINFO              NAMESPACE
*         k8s-cluster01-admin@k8s-cluster01   k8s-cluster01   k8s-cluster01-admin
          k8s-cluster02-admin@k8s-cluster02   k8s-cluster02   k8s-cluster02-admin
```

+ **k8s-cluster02에 webserver deployment 생성**

```bash
root@k8s-master2:~# kubectl create deployment --image=nginx webserver
deployment.apps/webserver created
root@k8s-master2:~# kubectl get all
NAME                             READY   STATUS              RESTARTS   AGE
pod/webserver-7c4f9bf7bf-hgr8f   0/1     ContainerCreating   0          10s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   102m

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver   0/1     1            0           10s

NAME                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/webserver-7c4f9bf7bf   1         1         0       10s
```

+ **k8s-cluster01에서 k8s-cluster02으로 전환하여 확인해 보자.**

```bash
root@k8s-master:~# kubectl config get-contexts
CURRENT   NAME                                CLUSTER         AUTHINFO              NAMESPACE
*         k8s-cluster01-admin@k8s-cluster01   k8s-cluster01   k8s-cluster01-admin
          k8s-cluster02-admin@k8s-cluster02   k8s-cluster02   k8s-cluster02-admin


root@k8s-master:~# kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   44d


## cluster02로 전환
root@k8s-master:~# kubectl config use-context k8s-cluster02-admin@k8s-cluster02
Switched to context "k8s-cluster02-admin@k8s-cluster02".


root@k8s-master:~# kubectl get all
NAME                             READY   STATUS    RESTARTS   AGE
pod/webserver-7c4f9bf7bf-hgr8f   1/1     Running   0          3m59s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   106m

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver   1/1     1            1           3m59s

NAME                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/webserver-7c4f9bf7bf   1         1         1       3m59s
```

<br>

----

> # 3. 컨텍스트 추가와 기본 네임스페이스 변경

```bash
## 컨텍스트 추가, prod 라는 이름의 컨텍스트를 만들고 싶을 때
root@k8s-master:~# kubectl config set-context prod --cluster=k8s-cluster01 --user=k8s-cluster01-admin --namespace=prod
Context "prod" created.


## 컨텍스트 목록, CURRENT 열에 * 표시된 컨텐스트가 현재 사용 중인 컨텍스트
root@k8s-master:~# kubectl config get-contexts
CURRENT   NAME                                CLUSTER         AUTHINFO              NAMESPACE
          k8s-cluster01-admin@k8s-cluster01   k8s-cluster01   k8s-cluster01-admin
*         k8s-cluster02-admin@k8s-cluster02   k8s-cluster02   k8s-cluster02-admin
          prod                                k8s-cluster01   k8s-cluster01-admin   prod


## prod 컨텍스트 사용
root@k8s-master:~# kubectl config use-context prod
Switched to context "prod".


root@k8s-master:~# kubectl config get-contexts
CURRENT   NAME                                CLUSTER         AUTHINFO              NAMESPACE
          k8s-cluster01-admin@k8s-cluster01   k8s-cluster01   k8s-cluster01-admin
          k8s-cluster02-admin@k8s-cluster02   k8s-cluster02   k8s-cluster02-admin
*         prod                                k8s-cluster01   k8s-cluster01-admin   prod


root@k8s-master:~# kubectl get all
No resources found in prod namespace.


root@k8s-master:~# kubectl get all -n default
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   44d


root@k8s-master:~# kubectl get all -n prod
No resources found in prod namespace.
```

<br>

----

> # 4. 참고

+ https://bryan.wiki/292