
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
kubectl create -f 파일명
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
파일에 기술된 오브젝트를 생성
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl delete -f 파일명
</td>
<td>
파일에 기솔된 오브젝트 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl apply -f 파일명
</td>
<td>
파일에 기재된 오브젝트가 있으면 변경하고 없으면 생성
</td>
</tr>
</table>

----

# 2. 매니페스트 예시

아래 매니페스트의 내용은 'kubectl run nginx --image=nginx:latest --restart=Never'를 실행한 것과 같은 의미를 가진다.

매니페스트는 YAML이나 JSON으로 기술할 수 있으며, 주로 YAML이 많이 사용된다.

```
apiVersion: v1                              ## 표 1 파드 API
kind: Pod
metadata:
    name: nginx
spec:                                       ## 표 2 파드 사양
    containers:                             ## 표 3 컨테이너 기동 조건 설정
        - name: nginx
          image: nginx:latest
```

----

# 3. 매니페스트 작성 방법

[쿠버네티스 API 레퍼런스](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/)

### 표 1 파드 API
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
v1 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kind
</td>
<td>
Pod 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
metadata
</td>
<td>
파드의 이름을 지정하는 name은 필수 항목이며, 네임 스페이스 내에서 유일한 이름이어야 한다.
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
spec
</td>
<td>
파드의 사양을 기술
</td>
</tr>
</table>


### 표 2 파드의 사양 
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
containers
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
컨테이너의 사양을 배열로 기술 (표 3 참조)
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
initContainers
</td>
<td>
초기화 전용 컨테이너의 사양을 배열로 기술, (내용은 containers와 동일)
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
nodeSelector
</td>
<td>
파드가 배포될 노드의 레이블을 지정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
volumes
</td>
<td>
파드 내 컨테이너 간에 공유할 수 있는 볼륨을 설정
</td>
</tr>
</table>


### 표 3 컨테이너 설정
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
image
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
이미지의 리포지터리명과 태그
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
name
</td>
<td>
컨테이너를 여러 개 기술할 경우 필수 항목
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
livenessProbe
</td>
<td>
컨테이너 애플리케이션이 정상적으로 동작 중인지 검사하는 프로브
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
readinessProbe
</td>
<td>
컨테이너 애플리케이션이 사용자의 요청을 받을 준비가 되었는지 검사하는 프로브
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
ports
</td>
<td>
외부로부터 요청을 전달받기 위한 포트 목록
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
resources
</td>
<td>
CPU와 메모리 요구량과 상한치
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
volumeMounts
</td>
<td>
파드에 정의한 볼륨을 컨테이너의 파일 시스템에 마운트하는 설정 (복수 개 기술 가능)
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
command
</td>
<td>
컨테이너 기동 시 실행할 커맨드 args가 인자로 적용
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
args
</td>
<td>
command의 실행 인자
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
env
</td>
<td>
컨테이너 내에 환경 변수를 설정
</td>
</tr>
</table>