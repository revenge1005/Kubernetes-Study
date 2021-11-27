
# 1. 크론잡

+ 정해진 시간에 잡 컨트롤러하의 파드를 실행할 수 있다.

----

# 2. 매니페스트 (cron-job.yml)

```
apiVersion: batch/v1
kind: CronJob
metadata:
    name: hello
spec:
    schedule: "*/1 * * * *"
    jobTemplate:
        spec:
            template:
                spec:
                    containers:
                    - name: hello
                      image: busybox
                      args:
                      - /bin/bash
                      - -c
                      - date; echo Hello from the Kubernetes cluster
                    restartPolicy: OnFailure
```

# 3. 매니페스트 작성 방법

### (1) 크론잡 API
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
batch/v1 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kind
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
CronJob 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
metadata
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
name은 필수 항목으로 네임스페이스 내에서 중복 없이 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
spec
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
잡 컨트롤러의 사양을 기술 (표 2 참조)
</td>
</tr>
</table>

### (2) 크론잡 사양
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
schedule
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
cron 형식으로 스케줄을 기술
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
jobTemplate
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
잡 템플릿, 주 내용은 파드 템플릿
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
startingDeadlineSeconds
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
잡이 시작되고 대기할 시간을 초단위로 지정, 지정한 시간 내에 시작을 못하면 취소됨
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
concurrencyPolicy
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
다음 정책 중 하나를 선택 <br> + Allow: 동시 실행 허가 (기본값) <br> Forbid: 이전 잡이 미완료인 경우에는 스킵 <br> Replace: 이전 미완료 잡을 중단하고 새로 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
suspend
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
기본값은 False, True로 하면 다음 스케줄이 정지됨
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
successfulJobsHistoryLimit
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
기본값은 3, 지정 횟수만큼의 성공한 잡이 보존됨
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
failedJobsHistoryLimit
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
기본값은 1, 지정 횟수만큼의 실패한 잡이 보존됨
</td>
</tr>
</table>