
# 1. 컨트롤러에 의한 파드 실행

'kubectl run'에 옵션을 지정하면 파드를 디플로이먼트 컨트롤러의 제어하에 실행하는 것이 가능하다.

이때 사용하는 옵션이 '--restart=Always'이며, 파드만 독립적으로 실행하고 싶을 때는 '--restart=Never' 옵션을 주면 된다.

'kubectl run'의 옵션 '--restart='를 생략하면 기본값으로 Always로 실행된다.

즉, 기본적으로 디플로이먼트에 의해 파드가 기동되며, 이 경우 백그라운드엣 실행되기 때문에 옵션 '-it' 는 무시된다.

``` 
$ kubectl  create deployment --image=hello-world hello-world
deployment.apps/hello-world created


$ kubectl get all
NAME                              READY   STATUS             RESTARTS     AGE
pod/hello-world-d758f5675-nrn88   0/1     CrashLoopBackOff   1 (7s ago)   14s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   28d

NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/hello-world   0/1     1            0           14s

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/hello-world-d758f5675   1         1         0       14s


$ kubectl logs pod/hello-world-d758f5675-nrn88

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

# 2. 디플로이먼트 삭제

```
$ kubectl get deployment
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
hello-world   0/1     1            0           2m34s

$ kubectl delete deployment hello-world
deployment.apps "hello-world" deleted
```

# 3. 웹 서버 Nginx 디폴로이먼트 실행 예

웹 서버의 파드 5개 기동해 보고, 하나의 파드에 문제가 발생해도 디플로이먼트가 파드 개수가 5개가 되도록 유지시켜 준다.

```
$ kubectl create deployment --image=nginx webserver
deployment.apps/webserver created

$ kubectl scale --replicas=5 deployment webserver
deployment.apps/webserver scaled

$ kubectl get all
NAME                             READY   STATUS              RESTARTS   AGE
pod/webserver-559b886555-6hxpx   0/1     ContainerCreating   0          15s
pod/webserver-559b886555-fb479   0/1     ContainerCreating   0          15s
pod/webserver-559b886555-m887m   0/1     ContainerCreating   0          15s
pod/webserver-559b886555-tw58x   0/1     ContainerCreating   0          30s
pod/webserver-559b886555-wclrl   0/1     ContainerCreating   0          15s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   28d

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver   0/5     5            0           30s

NAME                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/webserver-559b886555   5         5         0       30s
```

일부 파드를 지워졌을 때 새로운 파드가 자동으로 생성되는 것을 확인할 수 있다.

즉, 파드는 일시적인 존재로 그 자체가 되살아난 것이 아니라 새로운 파드가 만들어진 것을 볼 수 있으며, 컨테이너의 애플리케이션은 기본적으로 상태가 없어야 한다.(Stateless)

```
$ kubectl delete pod webserver-559b886555-6hxpx webserver-559b886555-fb479
pod "webserver-559b886555-6hxpx" deleted
pod "webserver-559b886555-fb479" deleted

$ kubectl get deploy,pod
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver   5/5     5            5           3m1s

NAME                             READY   STATUS              RESTARTS   AGE
pod/webserver-559b886555-m887m   1/1     Running             0          2m46s
pod/webserver-559b886555-s4nr4   0/1     ContainerCreating   0          12s
pod/webserver-559b886555-tw58x   1/1     Running             0          3m1s
pod/webserver-559b886555-vc67j   0/1     ContainerCreating   0          11s
pod/webserver-559b886555-wclrl   1/1     Running             0          2m46s
```