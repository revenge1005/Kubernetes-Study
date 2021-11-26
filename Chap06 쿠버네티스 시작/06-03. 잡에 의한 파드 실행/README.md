
# 잡에 의한 파드 실행

hello-world 컨테이너는 메시지를 출력하고 종료하는 단발성 형태의 워크로드이며, 이에 적합한 쿠버네티스의 컨트롤러로 잡 컨트롤러가 있다.

'kubectl run'의 옵션으로 '--restart=OnFailure'를 지정하면, 잡 컨트롤러의 제어하에 파드가 기동된다.

잡 컨트롤러는 파드가 비정상 종료하면 재시작하며 파드가 정상 종료할 때까지 지정한 횟수만큼 재실행한다.

```
$  kubectl create job hello-world --image=hello-world
job.batch/hello-world created


$ kubectl get all
NAME                       READY   STATUS      RESTARTS   AGE
pod/hello-world--1-mfcbk   0/1     Completed   0          7s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   28d

NAME                    COMPLETIONS   DURATION   AGE
job.batch/hello-world   1/1           3s         9s


$ kubectl logs hello-world--1-mfcbk

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

# 종료 코드에 따른 동작 차이

잡 컨트롤러는 컨테이너의 프로세스 종료 코드 값으로 성공과 실패를 판정한다.

job-1은 정상 종료, job-2는 비정상 종료 하도록 셸 스크립트를 사용하고 있다.

job-1은 COMPLETIONS가 1/1이 되어 잡이 수행 완료된 반면, job-2는 30초가 지나도 0이다.

이때 'kubectl get pod'를 실행해 보면 job-2의 파드가 계속 재시작하는 것을 알 수 있다.

```
$ kubectl create job job-1 --image=ubuntu -- /bin/bash -c "exit 0"
job.batch/job-1 created


$ kubectl get jobs
NAME    COMPLETIONS   DURATION   AGE
job-1   1/1           10s        11s


$ kubectl create job job-2 --image=ubuntu -- /bin/bash -c "exit 1"
job.batch/job-2 created


$ kubectl get job,pod
NAME              COMPLETIONS   DURATION   AGE
job.batch/job-1   1/1           10s        63s
job.batch/job-2   0/1           13s        13s

NAME                 READY   STATUS      RESTARTS   AGE
pod/job-1--1-6stfq   0/1     Completed   0          63s
pod/job-2--1-2cb8l   0/1     Error       0          9s
pod/job-2--1-d8457   0/1     Error       0          13s
```
