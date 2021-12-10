----

> # 1. 오토스케일

+ 오토스케일은 CPU와 메모리 사용률에 따라 파드나 노드의 수를 자동으로 늘리고 줄이는 기능

+ 특히 퍼블릭 클라우드에서는 노드의 개수, 이용 시간에 따라 비용이 달라지기 때문에 비용 최적화와도 연결된다.

<br>

----

> # 2. 온프레미스에서의 오토스케일 활용

+ 예를 들면 업무 시간대에는 사용자의 요청을 처리하는 파드의 비중을 높이고, 심야 시간대에는 배치 처리를 수행하는 파드의 비중을 높이는 식의 활용

<br>

----

> # 3. 수평 파드 오토스케일러 (Horizontal Pod Autoscaler, HPA)

+ 쿠버네티스의 오토스케일을 개발하는 여러 서브 프로젝트가 있는데, 그중에서도 특히 주목할 많한 것이 다음 두 프로젝트이다.

    - 수평 파드 오토스케일러(Horizontal Pod Autoscaler, HPA)

    - 클러스터 오토스케일러(Cluster Autoscaler, CA)

+ HPA는 파드의 CPU 사용률을 감시하면서 파드의 레플리카 수를 늘리거나 줄이고, 한편 CA는 필요할 때 노드를 자동으로 추가한다.

+ 클라우드에서는 부하에 반응하여 노드의 개수를 조절하는 것이 비용 절감을 위해 좋지만, HPA는 이러한 요구 사항을 충족시키진 못한다.

+ 한편, CA를 사용하면 클라우드의 API와 연동하여 노드를 늘리거나 줄여 비용을 절약할 수 있다.

<br>

----

> # 4. 오토스케일링 작업

+ 오토스케일을 사용하기 위해서는 컨테이너가 갑작스러운 종료 요청에 대응할 수 있어야 한다.

+ 즉, 종료 요청 시그널 SIGTERM을 받으면 종료 처리를 수행하고 컨테이너를 종료하도록 구현해야 한다.

----

+ HPA는 대상이 되는 파드의 CPU 사용률을 정기적으로 수집하고 CPU 사용률의 평균을 목표값이 되도록 레플리카 수를 조절한다.

+ 이때 조절 범위는 **"MinReplicas <= Replicas <= MaxReplicas"** 가 된다.

+ (파드 수) = 소수접 값을 올려 정수 (파드들의 CPU 사용률 총합 / 목표 CPU 사용률)

----

## (1) (metrics server)

+ 메트릭 서버는 클러스터 전역에서 리소스 사용량 데이터를 집계한다.

+ kube-up.sh 스크립트에 의해 생성된 클러스터에는 기본적으로 메트릭 서버가 디플로이먼트 오브젝트로 배포된다. 

+ 만약 다른 쿠버네티스 설치 메커니즘을 사용한다면, 제공된 디플로이먼트 components.yaml 파일을 사용하여 메트릭 서버를 배포할 수 있다.

    - <참고> : https://kubernetes.io/ko/docs/tasks/debug-application-cluster/resource-metrics-pipeline/

----

## (2)【 설치 방법 】

+ 설치 : https://github.com/kubernetes-sigs/metrics-server/releases

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.4.5/components.yaml
### 내용 변경
kubectl edit deploy -n kube-system metrics-server
```
### 해당 부분 수정
```
apiVersion: apps/v1apiVersion: apps/v1
kind: DeploymentapiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-server
  namespace: kube-system
  labels:
    k8s-app: metrics-serverapiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-server
  namespace: kube-system
  labels:
    k8s-app: metrics-server

<중략>

    spec:
      serviceAccountName: metrics-server
      volumes:
      # mount in tmp so we can safely use from-scratch images and/or read-only containers
      - name: tmp-dir
        emptyDir: {}
      containers:
      - name: metrics-server
        k8s.gcr.io/metrics-server-amd64:v0.3.6
        args:
          - --kubelet-preferred-address-types=InternalDNS,InternalIP,ExternalDNS,ExternalIP,Hostname   ### 추가 (1)
          - --kubelet-insecure-tls     ### 추가 (2)
          - --cert-dir=/tmp
          - --secure-port=4443
          - --metric-resolution=30s    ### 15->30 변경
        ports:
        - name: main-port
          containerPort: 4443
          protocol: TCP
        securityContext:
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
        imagePullPolicy: Always
        volumeMounts:
        - name: tmp-dir
          mountPath: /tmp
      nodeSelector:
        beta.kubernetes.io/os:
      hostNetwork: true                 ### 추가 (3)
```
----

## (3) 실행

```
$ kubectl top node
NAME         CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
k8s-master   295m         14%    1662Mi          43%
k8s-node01   111m         5%     641Mi           34%
k8s-node02   107m         5%     715Mi           38%


$ kubectl apply -f autoscale.yml


$ kubectl get all
NAME                           READY   STATUS    RESTARTS   AGE
pod/web-php-7b7566bd54-xvlgg   1/1     Running   0          20s

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP        42d
service/web-php      NodePort    10.110.150.193   <none>        80:31446/TCP   20s

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/web-php   1/1     1            1           20s

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/web-php-7b7566bd54   1         1         1       20s


$ kubectl top pod
NAME                       CPU(cores)   MEMORY(bytes)
web-php-7b7566bd54-xvlgg   1m           18Mi
```

