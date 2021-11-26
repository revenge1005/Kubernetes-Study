# 1. kubectl 명령

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
kubectl cluster-info
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
K8s 클러스터의 엔드포인트를 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl get node
</td>
<td>
K8s 클러스터를 구성하는 목록 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl run
</td>
<td>
파드를 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl get pod
</td>
<td>
파드의 목록 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl delete pod 
</td>
<td>
파드의 이름을 지정해서 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl get all
</td>
<td>
모든 오브젝트를 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl logs
</td>
<td>
컨테이너 프로세스가 STDOUT이나 STDERR로 출력하는 로그를 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl get deploy,pod
</td>
<td>
디플로이먼트와 파드의 목록 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl get deploy
</td>
<td>
디플로이먼트 목록 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl delete deploy
</td>
<td>
디플로이먼트와 관련된 레플리카셋 및 파드를 일괄 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl get jobs
</td>
<td>
잡의 실행 상태를 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl create job
</td>
<td>
잡 컨트롤러 제어하에서 파드를 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl create deployment
</td>
<td>
디플로이먼트 컨트롤러 제어하에서 파드를 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl scale
</td>
<td>
레플리카 수 변경
</td>
</tr>
</table>
