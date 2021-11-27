
+ 경우에 따라서는 동일한 클라이언트에서 온 요청은 언제나 같은 파드에 전송하고 싶을 수 있다.

+ 그런 경우에는 매니페스트의 세션 어피니티(sessionAffinity)를 ClintIP로 설정하면 된다.

----

```
$ cat svc-sa.yml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - protocol: TCP
    port: 80
  sessionAffinity: ClientIP      # 클라이언트 IP 주소에 따라 전송될 파드가 결정됨


$ kubectl apply -f svc-sa.yml
service/web-service configured


$ kubectl get pod
NAME                          READY   STATUS    RESTARTS   AGE
web-deploy-86cd4d65b9-2v5p2   1/1     Running   0          104m
web-deploy-86cd4d65b9-p4mkt   1/1     Running   0          104m
web-deploy-86cd4d65b9-pg7fw   1/1     Running   0          104m


## 부하분산 테스트에서 모두 같은 호스트명을 반환하고 있다.
$ kubectl run -it busybox --restart=Never --rm --image=busybox sh
If you don't see a command prompt, try pressing enter.
/ #
/ # while true; do wget -q -O - http://web-service; sleep 1;done
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-p4mkt
web-deploy-86cd4d65b9-p4mkt
...
```
