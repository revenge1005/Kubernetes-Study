
# 1. 테이크 오버를 자동화

+ GKE에서는 정지한 노드를 대신해 다른 노드를 기동시켜 자기 회복 한다.

+ 온프레미스에서 구성한 경우에도 노드가 장애로 정지했을 때 파드를 빠르게 다른 노드로 옮겨서 서비스를 재개하고 싶을 것이다.

+ 온프레미스 환겨에서 정지한 노드를 클러스터에서 자동으로 제외해 해당 노드에서 실행되던 파드를 다른 노드로 옮겨 서버스가 재개될 수 있도록 할 것이다.

![자동 테이크오버](https://user-images.githubusercontent.com/42735894/143897790-4890c965-e6aa-4c5d-930e-b6e9421347d3.PNG)

----

# 2. 기능 구현에 고려해야할 점

### (1) K8s API 라이브러리를 사용하여 프로그램 개발
kubectl을 사용하지 않으며, 파드상의 컨테이너에서 돌아가는 프로그램에서 K8s API를 직접 호출하여 K8s 클러스터의 상태 변화에 대한 처리를 자동화한다.
<br>

### (2) K8s 클러스터에 대한 조작 권한을 파드에 부여
+ kubectl의 마스터에 접속하기 위해서는 인증 정보(KUBECONFIG)가 필요하다

+ 마찬가지로 파드상의 컨테이너가 K8s 클러스터를 조작하기 위해서는 권한 부여가 필용하다
<br>

### (3) 네임스페이스 분리
+ 애플리케이션용 파드와 시스템을 위한 파드는 담당자나 책임 부서가 다르기 마련이다.

+ 쿠버네티스의 네임스페이스는 관리 범위를 명확하게 분리하는 수단으로 적합하며, 여기서 개발하는 파드는 전용 네임스페이스로 배포할 것이다.
<br>

### (4) K8s 클러스터의 구성 변동에 자동 대응
+ 이 자동화 컨테이너는 노드의 정지/추가/변동에 대응해야 한다.

+ 여기서는 쿠버네티스의 데몬셋 컨트롤러를 사용하여 파드를 기동할 것이다.

---- 

# 3. RBAC 권한 부여 매니페스트 작성

+ RBAC(Role-Based Access Control)은 역할 기준의 접근 제어로, k8s 클러스터 내에 역할(Role)을 설정하고 그 역할에 접근 가능한 권한을 정의하는 접근 제어 방식

+ 쿠버네티스에서 RBAC로 정의한 역할은 서비스 어카운트와 매핑된다.

  - 유저 어커운트는 개인을 식별하는 계정

  - 서비스 어카운트는 개인을 식별하는 것이 아니라 파드로 동작하는 컨테이너를 식별하며 네임스페이스별로 유일하다.

+ 서비스 어카운트를 통해 필요한 최소한의 권한을 컨테이너에 부여한다.

+ 쿠버네티스는 서비스 어카운트의 개념을 도입하여 유저가 소속된 조직 데이터베이스와의 동기화, 복잡한 워크플로우, 조직 변경에 대한 대응 등 문제를 피하고 있다.

+ 하지만 클라우드 서비스나 소프트웨어 제품에서는 개인별 유저 관리가 필수이기 때문에 유저 어카운트와 서비스 어카운트가 대응 될 수 있도록 구현하고 있다.

### (1) service-account.yml
```
apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: tkr-system
  name: high-availability
```
### (1-1) service account v1 core 표1

https://kubernetes.io/docs/reference/kubernetes-api/authentication-resources/service-account-v1/

|항목|설명|
|------|---|
|apiVersion|v1 설정|
|kind|ServiceAccount 설정|
|metadata|+ name : 서비스 어카운트의 이름 <br> + namespace : 서비스 어카운트가 배치될 네임스페이스|

### (2) role-based-access-ctl.yml

https://kubernetes.io/docs/reference/kubernetes-api/authorization-resources/cluster-role-v1/

https://kubernetes.io/docs/reference/kubernetes-api/authorization-resources/cluster-role-binding-v1/

```
# 클러스터 롤
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nodes
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["list","delete"]
---
# 클러스터롤과 서비스 어카운트의 바인딩
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nodes
subjects:
- kind: ServiceAccount
  name: high-availability  # 서비스 어카운트 이름
  namespace: tkr-system    # 네임스페이스 지정은 필수
roleRef:
  kind: ClusterRole
  name: nodes
  apiGroup: rbac.authorization.k8s.io
```

### (2-1) 클러스터 롤 표2
|항목|설명|
|------|---|
|apiVersion|rbac.authorization.k8s.io/v1|
|kind|ClusterRole 설정|
|metadata|+ name : 클러스터 롤의 이름|
|rules|복수의 규칙 기술 가능 (표3 참조)|

### (2-2) 대상 자원과 허가 행위 규칙 표3
|항목|설명|
|------|---|
|apiGroups|리소스를 포함한 APIGroup 이름의 배열 <br> [""]의 경우는 core 그룹을 가리크며, core 외의 예를 들면 deployment는 ["apps"]가 됨|
|resources|롤을 적용하는 리소스 목록|
|verbs|허가할 동사의 목록 설정 가능한 Resources(자원)와 Verb(동사)의 관계는 "kubectl describe clusterrole admin -n kube-system"으로 확인|

### (2-3) 서비스 어카운트와 클러스터 롤의 대응 표4 
|항목|설명|
|------|---|
|apiVersion|rbac.authorization.k8s.io/v1|
|kind|ClusterRoleBinding 설정|
|metadata|+ name : 클러스터 롤 바인딩의 이름|
|subjects|서비스 어카운트의 이름과 소속된 네임스페이스를 기재 (표9)|
|roleRef|subject에서 지정한 서비스 어카운트가 참조할 클러스터 롤을 설정 (표10)|

### (2-4) 연결 대상의 서비스 어카운트 등의 지정 표5
|항목|설명|
|------|---|
|kind|ServiceAccount 설정|
|name|서비스 어카운트 이름|
|namespace|서비스 어카운트가 속하는 네임스페이스 설정|

### (2-5) 연결 롤 표6
|항목|설명|
|------|---|
|kind|ClusterRole 설정|
|name|참조하는 롤의 이름|
|apiGroup|rbac.authorization.k8s.io 설정|