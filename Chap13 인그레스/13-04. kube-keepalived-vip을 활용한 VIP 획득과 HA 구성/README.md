----
> # 1. VIP 획득과 HA 구성

+ NGINX 인그레스 컨트롤러는 Virtual IP(VIP)를 노드 간 공유하는 기능을 가지고 있지 않는다.

+ 퍼블릭 클라우드 환경에서는 인그레스와 VIP를 연결하는 기능이 있어 그대로 사용하면 되지만, 온프레미스 환경에서는 인그레스에 VIP를 설정하기 위한 작업이 필요하다.


![123](https://user-images.githubusercontent.com/42735894/144849076-bbfb71df-3179-46eb-a0d3-d6d3f4bb10d7.PNG)


+ kube-keepalived-vip 파드는 VRRP(Virtaul Router Redundancy Protocol)에 따라 멤버의 존재를 확인하고 멤버 중 한 노드에게 VIP를 부여함

+ 이 VIP를 받은 노드가 요청을 받아서 인그레스 컨트롤러에 전달한다.

+ 그림에서와 같이 인그레스 컨트롤러가 동작하는 노드와 VIP를 가지는 노드가 같을 필요는 없다.

+ 노드가 달라도 파드 네트워크를 통해 요청은 전달되며 만약 VIP를 가지는 노드가 오프라인이 되면 남은 노드가 VIP를 이어받는다.

<br>
----

> # 2. 클라이언트 요청이 VIP를 통해 파드에 전달되는 과정
<br>

![1234](https://user-images.githubusercontent.com/42735894/144851156-ff28fafe-39e3-4336-a58f-e9cf7b67fec2.PNG)

<br>
----

> # 3. 환경 구축

### 1) Nginx 인그레스 컨트롤러 YAML 파일 다운로드 후, 일부 수정

https://kubernetes.github.io/ingress-nginx/deploy/#bare-metal-clusters

```
$ wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.0/deploy/static/provider/baremetal/deploy.yaml


$ tree ingress-keepalived/
ingress-keepalived
├── deploy.yaml
├── vip-configmap.yml
├── vip-daemonset.yml
└── vip-rbac.yml

$ vim deployment

<중략>

#### (A) 인그레스 서비스 수정 및 추가
# Source: ingress-nginx/templates/controller-service.yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:
    helm.sh/chart: ingress-nginx-4.0.10
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.1.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx-controller
  namespace: ingress-nginx
spec:
  type: LoadBalancer        ## "NodePort -> LoadBalancer 변경"
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
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/component: controller
  externalIPs:             ##  "externalIPs 추가 IP 주소는 각 환경에 맞게 수정할 것"
    - 192.168.219.99       ##  kube-keepalived-vip의 VIP와 일치할 것

<중략>

#### (B) 인그레스 컨트롤러 디플로이먼트 수정 및 추가
# Source: ingress-nginx/templates/controller-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:

<중략>

    spec:
      dnsPolicy: ClusterFirst
      containers:
        - name: controller
          image: k8s.gcr.io/ingress-nginx/controller:v1.1.0@sha256:f766669fdcf3dc26347ed273a55e754b427eb4411ee075a53f30718b4499076a
          imagePullPolicy: IfNotPresent
          lifecycle:
            preStop:
              exec:
                command:
                  - /wait-shutdown
          args:
            - /nginx-ingress-controller
            - --election-id=ingress-controller-leader
            - --controller-class=k8s.io/ingress-nginx
            - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
            - --validating-webhook=:8443
            - --validating-webhook-certificate=/usr/local/certificates/cert
            - --validating-webhook-key=/usr/local/certificates/key
            - --publish-service=$(POD_NAMESPACE)/ingress-nginx-controller       ## "해당 부분 추가"
            ## 윗 부분 내용은 인그레스 컨트롤러의 서비스(ingress-nginx-controller) 타입 LoadBalancer의 External IP 주소를 설정한다.
            ## 해당 환겨엥서 타입 LoadBalancer의 서비스는 k8s 클러스터 외부의 로드밸런서와 연동하지 않는다.
            ## 대신에 외부용 IP (External IP)로 온 요청을 Nginx 인그레스 컨트롤러에 전달한다.
          securityContext:
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
            runAsUser: 101

<중략>

```

----
 
### 2) kube-keepalived-vip의 컨피그맵 작성 (vip-configmap.yml)

+ 공인 IP 주소를 인그레스 컨트롤러의 서비스에 전송하는 설정이다

+ 공인 IP 주소는 외부에서 접근할 수 있어야 한다.

```
$ cat vip-configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: vip-configmap
  namespace: ingress-nginx
data:
  192.168.219.99: ingress-nginx/ingress-nginx-controller
```

----
 
### 3) kube-keepalived-vip의 서비스 어카운트 작성과 RBAC 설정 (vip-rbac.yml)

+ kube-keepalived-vip의 서비스 어카운트와 클러스터 롤을 작성하여 매핑하는 매니페스트

```
$ cat vip-rbac.yml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kube-keepalived-vip
  namespace: ingress-nginx
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kube-keepalived-vip
rules:
- apiGroups: [""]
  resources:
  - pods
  - nodes
  - endpoints
  - services
  - configmaps
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kube-keepalived-vip
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kube-keepalived-vip
subjects:
- kind: ServiceAccount
  name: kube-keepalived-vip
  namespace: ingress-nginx
```

----

### 4) kube-keepalived-vip의 데몬셋 배포 (vip-daemonset.yml)

+ kube-keepalived-vip의 파드를 각 노드에 배포하기 위한 매니페스트

```
$ vip-daemonset.yml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-keepalived-vip
  namespace: ingress-nginx
spec:
  selector:
    matchLabels:
      name: kube-keepalived-vip
  template:
    metadata:
      labels:
        name: kube-keepalived-vip
    spec:
      hostNetwork: true
      serviceAccount: kube-keepalived-vip
      containers:
        - image: k8s.gcr.io/kube-keepalived-vip:0.11
          name: kube-keepalived-vip
          imagePullPolicy: Always
          securityContext:
            privileged: true
          volumeMounts:
            - mountPath: /lib/modules
              name: modules
              readOnly: true
            - mountPath: /dev
              name: dev
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          # to use unicast
          args:
          - --services-configmap=ingress-nginx/vip-configmap ### "인그레스의 네임스페스"/"vip-configmap.yml의 이름"
          - --use-unicast=true ### 테스트한 환경이 가상 네트워크를 사용하고 있기 때문에 유니캐스트 옵션을 사용했다.
          #- --vrrp-version=3
      volumes:
        - name: modules
          hostPath:
            path: /lib/modules
        - name: dev
          hostPath:
            path: /dev
```

<br>
----

> # 4. 결과 확인