
# 1. 수동 테이크 오버 

+ 하드웨어 보수 작업으로 노드를 일시적으로 정지해야 하는 경우의 조작 방법 (실습하기 위해서는 2개 이상의 노드가 필요함)

+ 예제에서는 k8s-node02를 계획적으로 정지하기 위해 새로운 파드가 배치되지 않게 하고, k8s-node02에서 실행되는 파드를 다른 노드로 강제로 이동시키고 있다.

+ 그러면 k8s-node01에서 MySQL 파드가 기동하게 된다.

+ 여기서 주의할 점은 파드의 이동은 "라이브 마이그레이션"이 아니기 때문에 MySQL 서비스를 일단 정지하고 이동해야 한다.

+ 그러면 실행 중인 트랙잭션은 취소되어 롤백된다 이러한 노드 교체 작업은 계획적으로 실시하는 것이 좋다.

### (1) 유지 보수를 위해 노드를 정지시키기 (스케줄 금지 및 파드 이동)

```
$ kubectl get node
NAME         STATUS  ROLES                  AGE   VERSION
k8s-master   Ready   control-plane,master   31d   v1.22.3
k8s-node01   Ready   <none>                 31d   v1.22.3
k8s-node02   Ready   <none>                 31d   v1.22.3


### MySQL의 파드가 k8s-node02에서 작동하고 있는 것을 확인
$ kubectl get pod mysql-0 -o wide
NAME      READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          15m   10.40.0.1   k8s-node02   <none>           <none>


### k8s-node02에 새로운 파드의 스케줄 금지
$ kubectl cordon k8s-node02
node/k8s-node02 cordoned


### 가동 중인 파드를 k8s-node02에서 k8s-node01으로 이동
$ kubectl drain k8s-node02 --ignore-daemonsets
node/k8s-node02 already cordoned
WARNING: ignoring DaemonSet-managed Pods: kube-system/kube-proxy-b6fxq, kube-system/weave-net-97cw4
evicting pod default/mysql-0
pod/mysql-0 evicted
node/k8s-node02 evicted


### 이동 완료 후 상태
$ kubectl get pod mysql-0 -o wide
NAME      READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          52s   10.32.0.3   k8s-node01   <none>           <none>
```

### (2) 유지 부소 완료 후 노드 복귀 (k8s-node02에 스케줄 재개)

```
$ kubectl get pod mysql-0 -o wide
NAME      READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          15m   10.32.0.3   k8s-node01   <none>           <none>

$ kubectl uncordon k8s-node02
node/k8s-node02 uncordoned
```