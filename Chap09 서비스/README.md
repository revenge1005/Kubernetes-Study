# 1. 서비스 타입



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

# 3. 매니페스트 작성 방법

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
port가 하나인 경우는 생략할 수 있고, 여러 개인 경우 필수 설정 <br> 각 포트의 이름은 서비스 스펙 내에서 유일해야 함
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
clusterIP
</td>
<td>
+ 이 항목을 생략하면 대표 IP 주소가 자동으로 할당된다. <br> + 그리고 None을 설정하면 헤드리스로 동작
</td>
</tr>
</table>