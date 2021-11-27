
# 1. 잡의 실행수와 동시 실행수

+ 잡 컨트롤러에 대한 기본 설정이라 할 수 있는 실행수(Completions)와 동시 실행수(Parallelism)이 있다.

----

# 2. 잡의 매니페스트 (job-normal-end.yml)

```
apiVersion: batch/v1                    # 표 1 배치잡 API
kind: Job
metadata:
  name: normal-end
spec:                                   # 표 2 배치잡의 사양
  template:
    spec:
      containers:
      - name: busybox
        image: busybox:latest
        command: ["sh",  "-c", "sleep 5; exit 0"]
      restartPolicy: Never
  completions: 6
  # parallelism: 2
```

----

# 3. 매니페스트 작성 방법

### (1) 배치잡 API
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
Job 설정
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

### (2) 잡 컨트롤러의 사양
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
template
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
구동하는 파드에 대해 기술하는 파드 템플릿
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
completion
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
총 실행 횟수, 0보다 큰 정수를 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
parallelism
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
동시 실행을 하는 파드의 개수, completion보다 작은 값을 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
activeDeadlineSeconds
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
잡의 최장 실행 시간을 초단위로 지정, 지정 시간이 지나면 강제 종료
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
backoffLimit
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
실패에 대한 최대 시행 횟수, 디폴트 값은 6 <br> 지수 back off 지연이 적용되어 10초, 20초, 40초와 같이 점차적으로 늘어나며 최대 6분까지 연장
</td>
</tr>
</table>

----

# 4. 확인

### (1) 실행 횟수 completions=6인 파드의 실행

```
### (a) 잡 작성
$ kubectl apply -f job-normal-end.yml
job.batch/normal-end created


### (b) 잡의 완료 상태 확인
$ kubectl get jobs
NAME         COMPLETIONS   DURATION   AGE
normal-end   1/6           17s        17s

### (c) 잡의 상세 정보
$ kubectl describe job
Name:             normal-end
Namespace:        default

<중략>

Parallelism:      1
Completions:      6

<중략>

Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  38s   job-controller  Created pod: normal-end--1-5554l
  Normal  SuccessfulCreate  29s   job-controller  Created pod: normal-end--1-l7rpb
  Normal  SuccessfulCreate  20s   job-controller  Created pod: normal-end--1-ckgbh
  Normal  SuccessfulCreate  11s   job-controller  Created pod: normal-end--1-hrsj4
  Normal  SuccessfulCreate  2s    job-controller  Created pod: normal-end--1-gwkkd
```

### (2) 실행 횟수 completions=6 그리고 parallelism=2인 잡을 실행

```
$ kubectl delete -f job-normal-end.yml

$ kubectl apply -f job-normal-end.yml

$ kubectl describe jobs
Name:             normal-end
Namespace:        default

<중략>

Parallelism:      2
Completions:      6

<중략>

Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  45s   job-controller  Created pod: normal-end--1-7sl5v
  Normal  SuccessfulCreate  45s   job-controller  Created pod: normal-end--1-f2bbc
  Normal  SuccessfulCreate  36s   job-controller  Created pod: normal-end--1-r6cwp
  Normal  SuccessfulCreate  36s   job-controller  Created pod: normal-end--1-kqxnq
  Normal  SuccessfulCreate  27s   job-controller  Created pod: normal-end--1-jbm45
  Normal  SuccessfulCreate  27s   job-controller  Created pod: normal-end--1-7572v
```