
# 1. 노드 장애 시의 동작

+ 실행 결과는 노드를 멈춘 후 1 분 간격으로 노드의 파드 목록을 출력하고 있다.

+ 그 결과, k8s-node01이 정지되고 1분 이내에 STATUS는 NotReady로 바꾸며, 노드의 상태를 얻을 수 없다고 표시된다.

+ 그리고 아무리 시간이 지나도 파드 mysql-0은 k8s-node02로 옮겨지지 않는다.

+ 그리고 마지막에 'kubectl delete node k8s-node01'을 실행하여 k8s-node01을 명시적으로 지워주면 그 때서야 k8s-node02에서 파드가 실행을 재개한다.

----

# 2. k8s-node01 정지 시 스테이트풀셋의 동작

+ 아래 결과를 통해 스테이트풀셋의 두 가지 특징을 파악할 수 있다.

+ (1) 퍼시스턴트 볼륨의 보호를 우선시하기 때문에 장애 노드 위에서 돌던 파드를 함부로 다른 노드에 옮기지 않는다는 점이다.

+ (2) 스테이트풀셋은 파드의 컨트롤러라는 역할을 넘어서서 노드를 삭제하지 않는다는 점이다.

+ 하지만 퍼블릭 클라우드의 스테이트풀셋은 노드 장애 시 동작이 다를 수 있다.

+ GKE에서는 노드의 가상 서버가 지워지면, 노드 수를 유지할 수 있도록 곧 자동으로 노드를 만들어서 기동하며, 그리고 파드는 해당 노드에서 다시 기동되어 애플리케이션이 재개된다.

+ 한편, IKS에서는 실행 예제와 같이 동작한다.

```
$ while true; do date;kubectl get node;echo;kubectl get pod -o wide;echo; sleep 60;done
Mon 29 Nov 2021 09:23:29 PM KST
NAME         STATUS     ROLES                  AGE   VERSION
k8s-master   Ready      control-plane,master   31d   v1.22.3
k8s-node01   NotReady   <none>                 31d   v1.22.3
k8s-node02   Ready      <none>                 31d   v1.22.3

NAME      READY   STATUS    RESTARTS   AGE     IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          3h43m   10.32.0.3   k8s-node01   <none>           <none>

## 11분 경과
Mon 29 Nov 2021 09:34:45 PM KST
NAME         STATUS     ROLES                  AGE   VERSION
k8s-master   Ready      control-plane,master   31d   v1.22.3
k8s-node01   NotReady   <none>                 31d   v1.22.3
k8s-node02   Ready      <none>                 31d   v1.22.3

NAME      READY   STATUS        RESTARTS   AGE     IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Terminating   0          3h55m   10.32.0.3   k8s-node01   <none>           <none>

## k8s-node01을 삭제하여 서비스 재개
$ kubectl delete node k8s-node01
node "k8s-node01" deleted

$ kubectl get pod -o wide
NAME      READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          21s   10.40.0.2   k8s-node02   <none>           <none>
```