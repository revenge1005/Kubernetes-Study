----

> # 1. HPA 설정과 부하 테스트

## (1) HPA 설정
```
kubectl autoscale (-f <파일명> | <컨트롤러> <오브젝트> | <컨트롤러>/<오브젝트>) [--min=<최소_파드_수>] --max=<최대_파드_수> [--cpu-percent=<목표_CPU_사용률>] [옵션]
```

```
$ kubectl autoscale deployment web-php --cpu-percent=50 --min=1 --max=10

### HPA 설정 후 상태
$ kubectl get deploy,rs,hpa,pod,svc
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/web-php   1/1     1            1           61m

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/web-php-7b7566bd54   1         1         1       61m

NAME                                          REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
horizontalpodautoscaler.autoscaling/web-php   Deployment/web-php   0%/50%    1         10        1          38s

NAME                           READY   STATUS    RESTARTS   AGE
pod/web-php-7b7566bd54-bqlsf   1/1     Running   0          40m

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP        42d
service/web-php      NodePort    10.110.150.193   <none>        80:31446/TCP   61m
```

## (2) 대화형 파드를 기동해서 무한 루프 셸을 실행
```
$ kubectl run -it busybox --restart=Never --rm --image=busybox sh

/ # while true; do wget -q -O - http://web-php > /dev/null; done
```

## (3) 오토스케일링 동작 상태 모니터링

```
$ while true; do  kubectl get hpa; sleep 10; done
NAME      REFERENCE            TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   <unknown>/50%   1         10        0          4s
NAME      REFERENCE            TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   <unknown>/50%   1         10        0          14s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        1          24s
# <<-- 액세스 부하 개시
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        1          34s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        1          44s
NAME      REFERENCE            TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   161%/50%   1         10        1          54s
NAME      REFERENCE            TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   381%/50%   1         10        4          64s
NAME      REFERENCE            TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   381%/50%   1         10        4          74s
NAME      REFERENCE            TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   127%/50%   1         10        8          84s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   47%/50%   1         10        8          94s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   47%/50%   1         10        8          104s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   46%/50%   1         10        8          115s
# <<-- 액세스 부하 정지
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   32%/50%   1         10        8          2m35s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   32%/50%   1         10        8          2m45s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   1%/50%    1         10        8          2m55s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        8          3m5s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        8          3m15s
.
.
.
web-php   Deployment/web-php   0%/50%    1         10        8          7m18s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        8          7m28s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        6          7m38s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        1          7m48s
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web-php   Deployment/web-php   0%/50%    1         10        1          7m58s
```