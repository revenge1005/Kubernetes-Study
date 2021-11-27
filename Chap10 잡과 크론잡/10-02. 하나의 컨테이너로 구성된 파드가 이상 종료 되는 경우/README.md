
# 1. 하나의 컨테이너로 구성된 파드가 이상 종료 되는 경우

+ 'backoffLimit: 3'으로 실행 횟수를 최대 3회로 제한

+ parallelism(동시 실행수)와 completions(총 실행수)에 대한 설정은 생략되어 있으므로 기본값인 1이 사용된다.

----

# 2. 이상 종료하는 잡의 매니페스트 (job-abnormal-end.yml)

```
apiVersion: batch/v1
kind: Job
metadata:
  name: abnormal-end
spec:
  backoffLimit: 3
  template:
    spec:
      containers:
      - name: busybox
        image: busybox:latest
        command: ["sh",  "-c", "sleep 5; exit 1"]
      restartPolicy: Never
```

----

# 3. 결과

```
$ kubectl describe jobs.batch abnormal-end
Name:             abnormal-end
Namespace:        default
Selector:         controller-uid=cc8181f1-6420-48fa-98ca-125a0a750861
Labels:           controller-uid=cc8181f1-6420-48fa-98ca-125a0a750861
                  job-name=abnormal-end
Annotations:      <none>
Parallelism:      1
Completions:      1
Completion Mode:  NonIndexed
Start Time:       Sat, 27 Nov 2021 23:21:43 +0900
Pods Statuses:    0 Running / 0 Succeeded / 4 Failed
Pod Template:
  Labels:  controller-uid=cc8181f1-6420-48fa-98ca-125a0a750861
           job-name=abnormal-end
  Containers:
   busybox:
    Image:      busybox:latest
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      sleep 5; exit 1
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type     Reason                Age   From            Message
  ----     ------                ----  ----            -------
  Normal   SuccessfulCreate      81s   job-controller  Created pod: abnormal-end--1-qzs67
  Normal   SuccessfulCreate      72s   job-controller  Created pod: abnormal-end--1-cv99t
  Normal   SuccessfulCreate      62s   job-controller  Created pod: abnormal-end--1-5t6nt
  Normal   SuccessfulCreate      42s   job-controller  Created pod: abnormal-end--1-sn852
  Warning  BackoffLimitExceeded  2s    job-controller  Job has reached the specified backoff limit
```