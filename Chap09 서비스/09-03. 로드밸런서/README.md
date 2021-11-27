
# 1. 로드밸런서

+ 로드밸런서(LoadBalancer) 타입은 ESC(Elastic Container Service), GKE(Google Kubernetes Engin)과 같은 클라우드 서비스를 사용할 때 사용 가능한 옵션

+ 로드밸런서의 서비스를 만드는 매니페스트로서 클라우드상의 공인 IP를 통해 인터넷에 HTTP 포트를 오픈한다.

----

# 2. 로드밸런서 매니페스트 (svc-lb.yml)

```
apiVersion: v1
kind: Service
metadata:
    name: web-service-lb
spec:
    selector:
        app: web
    ports:
    - name: webserver
      protocol: TCP
      port: 80
    type: LoadBalancer
```

----

# 3. 로드밸런서 설정

```
### 디플로이먼트 매니페스트 적용
$ kubectl apply -f deploy.yml
deployment.apps/web-deploy created


### 로드밸런서 적용
$ kubectl apply -f svc-lb.yml
service/web-service-lb created


### 서비스 목록
$ get service
NAME             TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)        AGE
kubernetes       ClusterIP      10.96.0.1       <none>            443/TCP        29d
web-service-lb   LoadBalancer   10.110.83.178   xxx.xxx.xxx.xxx   80:31111/TCP   10s


### 로드밸런서 상세 표시
$ kubectl describe service web-service-lb
Name:                     web-service-lb
Namespace:                default
Labels:                   <none>
Annotations:              kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"web-service-lb","namespace":"default"},"spec":{"ports":[{"name":"webserver","p...}]}}
Selector:                 app=web
Type:                     LoadBalancer
IP:                       10.110.83.178
LoadBalancer Ingress:     xxx.xxx.xxx.xxx               ## 공인 IP
Port:                     webserver  80/TCP             ## 파드명, 번호, 프로토콜
TargetPort:               80/TCP                        ## 파드의 포트
NodePort:                 webserver  31111/TCP          ## NodePort도 동시에 공개됨
Endpoints:                10.32.0.3:80,10.40.0.1:80,10.40.0.2:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   
    Type    Reason                  Age    From                 Message
    ----    ----                    ----   -----                ----
    Normal  EnsuringLoadBalancer    12m    service-controller   Ensuring load balancer
    Normal  EnsuredLoadBalancer     12m    service-controller   Ensured load balancer


### 로드밸런서 타입의 서비스 동작 확인
$ kubectl get no
NAME             STATUS   ROLES    AGE   VERSION
192.168.219.17   Ready    <none>   11h   v1.22.3+IKS
192.168.219.30   Ready    <none>   11h   v1.22.3+IKS

### 파드 목록, 배치된 노드와 파드의 IP 주소도 출력
$ kubectl get pod -o wide
NAME                          READY   STATUS    AGE   IP          NODE         
web-deploy-86cd4d65b9-5dfnc   1/1     Running   15m   10.40.0.2   192.168.219.30  
web-deploy-86cd4d65b9-gwnm5   1/1     Running   15m   10.32.0.3   192.168.219.17  
web-deploy-86cd4d65b9-svpnw   1/1     Running   15m   10.40.0.1   192.168.219.30  

### 반복적으로 서비스에 접근
$ while true; do curl http://xxx.xxx.xxx.xxx; sleep 1; done
web-deploy-86cd4d65b9-5dfnc
web-deploy-86cd4d65b9-svpnw
web-deploy-86cd4d65b9-gwnm5
web-deploy-86cd4d65b9-gwnm5
web-deploy-86cd4d65b9-5dfnc
web-deploy-86cd4d65b9-5dfnc
web-deploy-86cd4d65b9-svpnw
web-deploy-86cd4d65b9-5dfnc
```