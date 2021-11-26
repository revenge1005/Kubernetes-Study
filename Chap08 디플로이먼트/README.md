# 1. 이번에 사용한 kubectl 명령

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
kubectl scale
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
레플리카 값을 변경
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl rollout
</td>
<td>
롤아웃의 상태 표시, 일시정지와 재개, 취소, 이력 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl drain <노드명>
</td>
<td>
가동 중인 파드를 다른 노드로 이동
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl cordon <노드명>
</td>
<td>
노드에서 새로운 파드의 스케줄 금지
</td>
</tr>

<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl uncordon <노드명>
</td>
<td>
노드에서 새로운 파드의 스케줄을 재게
</td>
</tr>
</table>

----

# 2. 디플로이먼트 매니페스트 예시

```
apiVersion: apps/v1                             #> 표 1 디플로이먼트 API
kind: Deployment
metadata:
  name: web-deploy
spec:                                           #> 표 2 디플로이먼트 사양
  replicas: 3
  selector:                                     
    matchLabels:                                #> 컨트롤러와 파드를 대응시키는 라벨
      app: web                                  #> <- 파드에 해당 레벨이 있어야 한다.
  template:                                     #> 파드 템플릿
    metadata:
      labels:
        app: web                                #> 파드의 라벨, 컨트롤러의 matchLabels와 일치해야 함
    spec:                                       #> 표 3 파드 템플릿의 사양 
      containers:                               #> 컨테이너 사양
      - name: nginx
        image: nginx:1.16
```

----

# 3. 매니페스트 작성 방법

[쿠버네티스 API 레퍼런스 - 디플로이먼트 URL](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/deployment-v1/)

### 표 1 디플로이먼트 API 
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
apiVersion
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
쿠버네티스 버전 1.9 이후는 app/v1
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kind
</td>
<td>
Deployment를 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
metadata
</td>
<td>
name에 오브젝트의 이름을 설정한다.
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
spec
</td>
<td>
디플로이먼트의 사양을 기술 (표 2 참조)
</td>
</tr>
</table>


### 표 2 디플로이먼트 사양
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
replicas 
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
파드 템플릿을 사용해서 기동할 파드의 개수를 지정한다.
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
selector
</td>
<td>
디플로이먼트 제어하의 레플리카셋과 파드를 대응시키기 위해 <br> matchLabels의 라벨이 사용 이 라벨이 파드 템플릿의 <br> 레이블과 일치하지만 않으면 에러 발생
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
template
</td>
<td>
파드 템플릿 (표 3 참조)
</td>
</tr>
</table>

### 표 3 파드 탬플릿
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
metadata
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
이 라벨의 내용은 상기 셀렉터가 지정한 라벨과 일치해야 함
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
containers
</td>
<td>
파드 컨테이너의 사양 (스탭 07의 표 3 참조)
</td>
</tr>
</table>