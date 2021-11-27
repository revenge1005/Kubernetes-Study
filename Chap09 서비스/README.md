1. 이번에 사용한 kubectl 명령

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

# 2. 서비스의 매니페스트 예시

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

