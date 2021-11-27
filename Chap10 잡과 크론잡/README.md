
# 1. 잡 활용 예

### (1) 동시 실행과 순차 실행

+ 복수의 처리들 간에 순서가 없어 상호 독립적으로 실행할 수 있는 배치 처리를 생각해 볼 수 있다.

+ 잡 컨트롤러는 복수의 노드 위에서 여러 개의 파드를 동시에 실행하여 배치 처리를 빠르게 완료할 수 있다.

+ 대표적인 예로 대량 메일 발송, 이미지/동영상/음원 파일의 변환 처리, 대량 데이터를 포함하는 KVS형 데이터베이스 검색 등이 있다.

### (2) 파드를 실행할 노드 선택

+ 이번엔 다양한 사양의 노드로 구성된 클러스터에서 배치 처리를 실행하는 경우를 생각해 보자.

+ 매니페스트에 CPU 아키텍처, 코어 수, 메모리 요구량, 노드 셀렉터 라벨 등이 기재 되는데, 마스터 노드의 스케줄러는 기재된 조건을 만족하는 적절한 노드를 선택해서 파드를 배치한다.

### (3) 정기 실행 배치 처리

+ 크론잡은 설정한 시간에 정기적으로 잡을 실행한다.

+ 따라서 백업이나 메시간마다 실행되는 배치 처리 등에 사용할 수 있다.

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
kubectl get jobs
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
잡의 목록 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl describe jobs
</td>
<td>
잡의 상세 내용 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl delete jobs
</td>
<td>
잡 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl get cronjobs
</td>
<td>
크론잡의 목록 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl describe cronjobs
</td>
<td>
크론잡의 상세 내용 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl delete cronjobs
</td>
<td>
크론잡 삭제
</td>
</tr>
</table>