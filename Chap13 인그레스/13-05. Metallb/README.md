----

> # 1. MetalLB

https://metallb.universe.tf/

+ 쿠버네티스의 서비스 타입에는 NodePort, LoadBalancer 등 다양하게 지원하며, 이때 LoadBalancer는 클라우드 서비스 사업자를 위한 것으로 AWS, GCP, Azure에서 제공하는 LoadBalancer를 위한 것이다.

+ 그렇기 때문에 온-프레미스(On-Premise) 환경에서 LoadBalancer를 지원하지 않았지만, 온-프레미스 환경에서도 LoadBalancer 타입의 ExternalIP를 제공해줄 수 있는 도구가 나왔고 그것이 바로 "MetalLB"이다.

<br>

----

> # 2. NodePort, LoadBalancer 서비스 타입과 MetalLB 동작 과정 비교

### (1) NodePort

![nodeport](https://user-images.githubusercontent.com/42735894/145426933-f77ea90e-0b5d-471c-bdd7-a5c7ff172137.PNG)

----

### (2) LoadBalancer (Cloud)

![cloud_loadbalancer](https://user-images.githubusercontent.com/42735894/145426952-21a9330e-faba-4999-8e83-3b6c1a191b77.PNG)

----

### (3) MetalLB

+ **MetalLB Controller : 작동 방식 (프로토콜)을 정의하고, External-IP 부여하여 관리한다.**

+ **MetalLB speaker : 정해진 프로토콜 (L2/ARP, L3/BGP)에 따라 경로를 만들 수 있게 네트워크 정보를 광고하고 수집해 각 파드의 경로를 제공**

![metallb](https://user-images.githubusercontent.com/42735894/145426946-9f727058-13b4-4cbf-b714-7e6cd83c91a0.PNG)

<br>

----

> # 3. MetalLB Install

### (1) 준비 
```
$ kubectl edit configmap -n kube-system kube-proxy

apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
  strictARP: true   ### false -> true 변경
```

### (2) 설치
```
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.11.0/manifests/namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.11.0/manifests/metallb.yaml
```

### (3) ConfigMap (Layer 2 Configuration)

+ https://metallb.universe.tf/configuration/

+ Metallb에서 사용할 외부 IP나 운영 모드 등을 설정

```
cat <<EOF > metallb-l2config.yml
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.219.240-192.168.219.250
EOF
```
```
$ kubectl apply -f metallb-l2config.yml
configmap/config created
```

<br>

----

> # 4. 애플리케이션 배포와 테스트

### (1) 인그레스 컨트롤러 (Nginx)
```
$ wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.0/deploy/static/provider/baremetal/deploy.yaml


$ vim deploy.yaml

<중략>

spec:
  type: LoadBalancer        ### 서비스 타입을 NodePort->LoadBalancer 변경
  ipFamilyPolicy: SingleStack
  ipFamilies:
    - IPv4
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: http
      appProtocol: http
    - name: https
      port: 443
      protocol: TCP
      targetPort: https
      appProtocol: https

<중략>


### External-ip 할당 된 것을 확인할 수 있다.
$ kubectl get all -n ingress-nginx
NAME                                            READY   STATUS      RESTARTS   AGE
pod/ingress-nginx-admission-create--1-v7xkz     0/1     Completed   0          49s
pod/ingress-nginx-admission-patch--1-kcdzf      0/1     Completed   1          49s
pod/ingress-nginx-controller-5fd866c9b6-68hqj   1/1     Running     0          49s

NAME                                         TYPE           CLUSTER-IP     EXTERNAL-IP       PORT(S)                      AGE
service/ingress-nginx-controller             LoadBalancer   10.97.74.96    192.168.219.240   80:31732/TCP,443:30729/TCP   49s
service/ingress-nginx-controller-admission   ClusterIP      10.104.2.135   <none>            443/TCP                      49s

NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ingress-nginx-controller   1/1     1            1           49s

NAME                                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/ingress-nginx-controller-5fd866c9b6   1         1         1       49s

NAME                                       COMPLETIONS   DURATION   AGE
job.batch/ingress-nginx-admission-create   1/1           3s         49s
job.batch/ingress-nginx-admission-patch    1/1           3s         49s
```

### (2) 결과 확인
```
$ kubectl apply -f test-apl/


$ kubectl get all,ingress
NAME                                          READY   STATUS    RESTARTS        AGE
pod/hello-world-deployment-6c54b87b6f-9g4xm   1/1     Running   0               4h44m
pod/hello-world-deployment-6c54b87b6f-9kqgk   1/1     Running   1 (4h25m ago)   4h44m
pod/hello-world-deployment-6c54b87b6f-dkg2j   1/1     Running   1 (4h30m ago)   4h44m
pod/hello-world-deployment-6c54b87b6f-fbskm   1/1     Running   1 (4h30m ago)   4h44m
pod/hello-world-deployment-6c54b87b6f-q844g   1/1     Running   0               4h44m

NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/hello-world-svc   NodePort    10.106.78.102   <none>        8080:31445/TCP   4h44m
service/kubernetes        ClusterIP   10.96.0.1       <none>        443/TCP          42d

NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/hello-world-deployment   5/5     5            5           4h44m

NAME                                                DESIRED   CURRENT   READY   AGE
replicaset.apps/hello-world-deployment-6c54b87b6f   5         5         5       4h44m

NAME                                            CLASS    HOSTS            ADDRESS          PORTS   AGE
ingress.networking.k8s.io/hello-world-ingress   <none>   abc.sample.com   192.168.219.12   80      4h44m


$ vim /etc/hosts
192.168.219.240     abc.sample.com


$ curl http://abc.sample.com
<html><head><title>HTTP Hello World</title></head><body><h1>Hello from hello-world-deployment-6c54b87b6f-9g4xm</h1></body></html
```