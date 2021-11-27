
# 1. 여러 컨테이너 중 일부가 이상 종료 할 때의 동작

+ 첫 번째 컨테이너는 정상 종료, 두 번째 컨테이너는 이상 종료한 경우 파드의 종료 상태는 Completed가 되어 정상 종료한 것으로 처리된다.

+ 반대의 경우 즉, 첫 번째 컨테이너가 이상 종료하고, 두번째 컨테이너가 정상 종료하는 경우에는 파드의 종료 상태에 Error가 표시되어 파드가 이상 종료 한 것으로 취급

----

# 2. 매니페스트 (job-cotainer-failed.yml)

```
apiVersion: batch/v1
kind: Job
metadata:
  name: two-containers
spec:
  template:
    spec:
      containers:
      - name: busybox1
        image: busybox:1
        command: ["sh", "-c", "sleep 5; exit 0"]
      - name: busybox2
        image: busybox:1
        command: ["sh", "-c", "sleep 5; exit 1"]
      restartPolicy: Never
  backoffLimit: 2
```

----

# 3. 결과

+ (2) 파드의 종료 상태를 보면 STATUS를 보면 Completed로 문제 없어 보인다.

+ 그러나 (1) 잡의 상태의 Events 섹션을 보면 재실행이 반복되어 backoffLimit에 도달한 것을 알 수 있다.

+ 즉, 잡 컨트롤러는 kubectl get pod에 나오는 STATEUS의 값을 참조하지 않는다.

+ 파드 내의 컨테이너가 모두 정상 종료하는 것을 기준으로 재실행을 반복한다.

### (1) 두 번째 컨테이너가 이상 종료하는 경우의 동작

```
$ kubectl describe job
Name:             two-containers
Namespace:        default

<중략>

Events:
  Type     Reason                Age   From            Message
  ----     ------                ----  ----            -------
  Normal   SuccessfulCreate      58s   job-controller  Created pod: two-containers--1-ng78m
  Normal   SuccessfulCreate      51s   job-controller  Created pod: two-containers--1-q7tgn
  Normal   SuccessfulCreate      41s   job-controller  Created pod: two-containers--1-zpvwg
  Warning  BackoffLimitExceeded  1s    job-controller  Job has reached the specified backoff limit
```

### (2) 파드의 종료 상태

```
# kubectl get pod
NAME                      READY   STATUS      RESTARTS   AGE
two-containers--1-ng78m   0/2     Completed   0          102s
two-containers--1-q7tgn   0/2     Completed   0          95s
two-containers--1-zpvwg   0/2     Completed   0          85s
```