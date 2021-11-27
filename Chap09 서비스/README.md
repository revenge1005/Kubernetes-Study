# 1. 서비스 타입

<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
서비스 타입 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
ClusterIP
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
기본 설정값으로, 클러스터 내부의 파드에서 서비스의 이름으로 접근할 수 있다.
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
NodePort
</td>
<td>
ClusterIP의 접근 범위뿐만 아니라 K8s 클러스터 외부에서도 노드의 IP주소와 포트번호로 접근 가능
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
LoadBalancer
</td>
<td>
NodePort의 접근 범위뿐만 아니라 K8s 클러스터 외부에서 대표 IP 주소로 접근할 수 있다.
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
ExternalName
</td>
<td>
K8s 클러스터 내의 파드에서 외부 IP 주소에 서비스의 이름으로 접근할 수 있다.

</td>
</tr>
</table>

----

# 2. 이번에 사용한 kubectl 명령

<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl get service
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
서비스 목록 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl describe service
</td>
<td>
서비스의 자세한 내용을 표시
</td>
</tr>
</table>

----

# 3. 서비스의 매니페스트 예시

### (1) deploy.yml
```
apiVersion: apps/v1
kind: Deployment
metadata:
    name: web-deploy
spec:
    replicas: 3
    selector:                                       #> 디폴로이먼트와 파드를 매핑하는 설정
        matchLabels:
            app: web
    template:                                       #> 파드 템플릿
        metadata:
            labels:
                app: web                            #> 파드에 부여할 라벨
        spec:
            containers:
                - name: nginx
                  image: nginx:latest
```

### (2) service.yml
```
apiVersion: v1                                     #> 표 1
kind: Service
metadata:
    name: web-service
spec:                                              #> 표 2, type이 생략되어 ClusterIP가 사용
    selector:                                      #> 서비스와 파드를 매핑하는 설정
        app: web
    ports:                                         #> 표 3, 포트 설정
    - protocol: TCP
      port: 80
```

----

# 4. 매니페스트 작성 방법

[쿠버네티스 API 레퍼런스 - 서비스 URL](https://kubernetes.io/docs/reference/kubernetes-api/service-resources/service-v1/)

### 표 1 서비스 API 
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
apiVersion
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
v1 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kind
</td>
<td>
Service 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
metadata
</td>
<td>
+ name에 네임스페이스 내 유일한 이름을 설정 <br> + 여기서 설정한 이름은 내부 DNS에 등록되며, IP 주소 해결에 사용 <br> + 또한, 이후 기동된 파드의 환경 변수에 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
spec
</td>
<td>
서비스 사양
</td>
</tr>
</table>

### 표 2 서비스 사양
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
tyep
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
서비스 공개 방법을 설정 <br> 【타입 종류】: ClusterIP, NodePort, LoadBalancer, ExternalName
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
ports
</td>
<td>
서비스에 의해 공개되는 포트 번호 (표3)
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
selector
</td>
<td>
여기서 설정한 라벨과 일치하는 파드에 요청을 전송
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
sessionAffinity
</td>
<td>
설정이 가능한 세션 어피니티는 ClusterIP, 생략 시 None으로 설정됨
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
clusterIP
</td>
<td>
이 항목을 생략하면 대표 IP 주소가 자동으로 할당된다. <br> 그리고 None을 설정하면 헤드리스로 동작
</td>
</tr>
</table>

### 표 3 서비스 파드 사양
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
port
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
(필수 항목) 이 서비스에 의해 공개되는 포트번호
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
name
</td>
<td>
+ port가 하나인 경우는 생략할 수 있고, 여러 개인 경우 필수 설정 <br> + 각 포트의 이름은 서비스 스펙 내에서 유일해야 함
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
protocol
</td>
<td>
생략 시에는 TCP가 설정됨 
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
nodePort
</td>
<td>
+ 생략 시에는 시스템이 자동으로 할당 <br> + 타입이 NodePort, LoadBalancer인 경우 모든 노드에서 포트를 공개 <br> + 설정한 포트가 이미 사용 중인 경우에는 오브젝트 생성에 실패
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
targetPort
</td>
<td>
+ 생략 시에는 port와 돌일한 값이 사용됨 <br> + selector에 의해 대응되는 파드가 공개하는 포트번호 설정
</td>
</tr>
</table>

----

# 5. 서비스 생성과 기능 확인

### (1) 매니페스트 배포
```
$ kubectl apply -f deploy.yml
deployment.apps/web-deploy created

$ kubectl apply -f service.yml
service/web-service created

```

### (2) 디플로이먼트와 서비스 상태 출력
```
$ kubectl get all -o wide
NAME                              READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINA
pod/web-deploy-86cd4d65b9-2v5p2   1/1     Running   0          11s   10.40.0.2   k8s-node02   <none>
pod/web-deploy-86cd4d65b9-p4mkt   1/1     Running   0          11s   10.32.0.3   k8s-node01   <none>
pod/web-deploy-86cd4d65b9-pg7fw   1/1     Running   0          11s   10.40.0.1   k8s-node02   <none>

NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/kubernetes    ClusterIP   10.96.0.1       <none>        443/TCP   29d   <none>
service/web-service   ClusterIP   10.96.182.208   <none>        80/TCP    6s    app=web

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES         SELE
deployment.apps/web-deploy   3/3     3            3           11s   nginx        nginx:latest   app=

NAME                                    DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES
replicaset.apps/web-deploy-86cd4d65b9   3         3         3       11s   nginx        nginx:latest
```

### (3) 대화형 컨테이너를 기동하여 서비스에 요청 전송
```
$  kubectl run -it busybox --restart=Never --rm --image=busybox sh
If you don't see a command prompt, try pressing enter.

/ # wget -q -O - http://web-service
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

### (4) 서비스 관련 환경 변수
```
/ # env | grep WEB_SERVICE
WEB_SERVICE_PORT=tcp://10.96.182.208:80
WEB_SERVICE_SERVICE_PORT=80
WEB_SERVICE_PORT_80_TCP_ADDR=10.96.182.208
WEB_SERVICE_PORT_80_TCP_PORT=80
WEB_SERVICE_PORT_80_TCP_PROTO=tcp
WEB_SERVICE_PORT_80_TCP=tcp://10.96.182.208:80
WEB_SERVICE_SERVICE_HOST=10.96.182.208
```

### (5) 각 파드의 index.html에 호스트명을 적는 셸
```
$ for pod in $(kubectl get pods |awk 'NR>1 {print $1}'|grep web-deploy); \
do kubectl exec $pod -- /bin/sh -c "hostname>/usr/share/nginx/html/index.html"; done

```

### (6) 서비스 접속과 부하분산
```
$ kubectl run -it busybox --restart=Never --rm --image=busybox sh
If you don't see a command prompt, try pressing enter.
/ # while true; do wget -q -O - http://web-service; sleep 1;done
web-deploy-86cd4d65b9-2v5p2
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-pg7fw
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-2v5p2
web-deploy-86cd4d65b9-p4mkt
...
```