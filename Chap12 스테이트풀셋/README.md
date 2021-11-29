
# 1. 스테이트풀셋(StatefulSet)

+ 스테이트풀셋은 퍼시스턴트 볼륨과 파드를 함께 조합하여 제어하기에 적합한 컨트롤러다.

+ 컨테이너나 파드는 태생적으로 데이터를 보관하는 것이 어렵기 때문에 파드와 퍼시스턴트 볼륨을 조합하여 실행해야 한다.

+ 이러한 요구사항을 위해 쿠버네티스에서는 스테이트풀셋이라는 컨트롤러를 제공한다.

+ 이 컨트롤러는 파드와 퍼시스턴트 볼륨의 대응 관계를 엄격하게 관리하며, 퍼시스턴트 볼륨의 데이터 보간을 우선시하여 동작한다.

----

# 2. 디플로이먼트와의 차이점
<br>
 
### (a) 파드/퍼시스턴트 볼륨의 이름

+ 스테이트풀셋도 지정한 리플리카 수에 해당하는 파드를 파드 템플릿에 기술한 내용에 따라 기동되며 **스테이트풀셋에서는 파드와 퍼시스턴트 볼륨을 하나의 단위로 취급하여 동일한 번호가 이름**에 부여되며, 디플로리오먼트의 경우 해시가 붙는다.
<br>
 
### (b) 서비스와의 연결 및 이름 해결

+ 스테이트풀셋 관리하의 파트의 요청을 전송하기 위한 서비스는 **대표 IP를 가지지 않는 ClusterIP의 헤드리스 모드를 사용해야 한다.**

+ 클라이언트가 서비브의 이름으로 IP 주소를 해결하면 스테이트풀셋 관리하의 파드의 IP 주소가 랜덤하게 반환된다.
<br>
 
### (c) 파드 분실 시 동작

+ 스테이트풀셋 관리하의 **파드가 노드 장애 등으로 없어진 경우, 동일한 이름으로 새롭게 파드가 기동되며, 이때 기존 파드가 사용했던 퍼시스턴트 볼륨을 이어서 사용**한다.

+ 주의할 점은, 파드의 이름이 같아도 파드의 IP 주소는 변한다 그래서 스테이트풀셋 관리하의 파드에 접속하는 경우, 반드시 내부 DNS를 사용해서 이름을 해결해야 한다.
<br>
 
### (d) 노드 정지 시의 동작

+ 스테이트풀셋은 **데이터를 분실하지 않도록 설계되어 있지만 H/W, 네트워크 장애로 특정 노드가 연결이 끊어졌을 때 스테이트풀셋은 새로운 파드를 기동하지 않는다.**

+ 가령, 노드의 상태를 관리하는 kublet과 마스터와의 통신이 일시적으로 끊겼지만 파드는 계속해서 돌아가고 있는 경우, 마스터가 대체 파드를 기동하여 퍼시스턴트 볼륨을 마운트하게 되면 오히려 데이터가 파손될 수 있기 때문이다.

+ 파드가 퍼시스턴트 볼륨을 마운트할 때는 엑세스 모드로 여러 노드에서 읽고 쓰기가 가능한 ReadWriteMany(RWX)와 하나의 노드에서만 읽고 쓸 수 있는 ReadWriteOnce (RWO)를 사용할 수 있지만, 이들은 외부 스토리지 시스템에 종속된 파라미터라, NFS와 같이 공유 가능한 퍼시스턴트 볼륨에 RWO를 설정한다고 해도 새로운 파드가 기동되는 것을 억제할 수는 없다.
 
+ **다음 중 한 가지 경우에만 스테이트풀셋이 분실된 파드를 다른 노드에서 다시 기동**한다.

  (1) 장애 노드를 K8s 클러스터의 맴버에서 제외한다.

  (2) 문제가 있는 파드를 강제 종료한다.

  (3) 장애로 인해 정지한 노드를 재기동한다.
<br>

### (f) 파드 순번 제어 

+ 스테이트풀셋의 **파드 이름에 붙는 번수는 파드의 기동과 정지뿐만 아니라, 롤링 업데이트의 순서에도 사용**된다.

  (1) 시작할 때는 파드와 PV 짝지어 차례대로 기동, 정지할 때는 번호가 큰 순서로 정지

  (2) 레플리카 값을 줄이면 파드 이름의 번호가 큰 것부터 삭제

  (3) 롤링 업데이트할 때도 파드의 이름에 붙은 번호에 따라 갱신

+ 한편, 디플로이먼테에서의 파드명은 디폴리이먼트의 이름 뒤에 해시 문자열이 붙으며 파드의 기동 순서는 랜덤하게 적용된다.
<br>

---- 

# 3. 스테이트풀셋 매니페스트 작성법

https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/stateful-set-v1/

```
### mysql-sts.yml

apiVersion: v1
kind: Service
metadata:
  name: mysql        ## 이 이름이 k8s내 DNS에 등록됨.
  labels:
    app: mysql-sts
spec:
  ports:
  - port: 3306
    name: mysql
  clusterIP: None    ## 특징1 헤드리스 서비스 설정
  selector:
    app: mysql-sts   ## 후술하는 스테이트풀셋과 연결시키는 라벨
---
## MySQL 스테이트풀셋
#
apiVersion: apps/v1         ## 표1 스테이트풀셋 참고
kind: StatefulSet
metadata:
  name: mysql
spec:                       ## 표2 스테이트풀셋 사양
  serviceName: mysql        ## 특징2 연결할 서비스의 이름 설정
  replicas: 1               ## 파드 기동 개수
  selector:
    matchLabels:
      app: mysql-sts
  template:                 ## 표3 파드의 템플릿
    metadata:
      labels:
        app: mysql-sts
    spec:
      containers:
      - name: mysql
        image: mysql:5.7    ## Docker Hub MySQL 리포지터리 지정
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: qwerty
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:       ## 특징3 컨테이너상의 마운트 경로 설정
        - name: pvc
          mountPath: /var/lib/mysql
          subPath: data     ## 초기화 시 빈 디렉터리가 필요
        livenessProbe:      ## MySQL 기동 확인
          exec:
            command: ["mysqladmin","-p$MYSQL_ROOT_PASSWORD","ping"]
          initialDelaySeconds: 60
          timeoutSeconds: 10
  volumeClaimTemplates:     ## 특징4 볼륨 요구 템플릿
  - metadata:
      name: pvc
    spec:                   ## 표4 퍼시스턴트볼륨 요구 스펙
      accessModes: [ "ReadWriteOnce" ]
      ## 환경에 맞게 선택하여, sotrage의 값을 편집
      #storageClassName: ibmc-file-bronze   # 용량 20Gi IKS
      storageClassName: gluster-heketi      # 용량 12Gi GlusterFS
      #storageClassName: standard           # 용량 2Gi  Minikube/GKE
      resources:
        requests:
          storage: 2Gi
```

### (1) 스테이트풀셋 API

|항목|설명|
|------|---|
|apiVersion|apps/v1 설정|
|kind|StatefulSet 설정|
|metadata|name에 이름 설정|
|spec|스테이트풀셋의 사양 (표2참고)|

### (2) 스테이트풀셋의 사양

|항목|설명|
|------|---|
|serviceName|헤드리스 서비스의 이름|
|replicas|파드 템플릿을 사용해서 기동하는 파드 수를 지정|
|selector.matchLabels|본 컨트롤러 제어하의 파드를 관리하기 위해 matchLabels의 라벨을 사용|
|template|본 컨트롤러가 기동하는 파드 템플릿을 기술 (표 3 참조)|
|volumeClaimTemplates|파드가 마운트하는 볼륨의 템플릿을 기술 (표 4참조)|

### (3) 파드 템플릿

|항목|설명|
|------|---|
|metadata.lables|이 라벨은 표 2의 실렉터와 같은 라벨 설정 필요|
|containers|파드의 컨테이너에 대해 기술|

### (4) 퍼시스턴트 볼륨 요구

|항목|설명|
|------|---|
|metadata.name|파드 수에 맞는 PVC가 작성되며 이 이름은 PVC명의 접두어가 됨|
|spec|볼륨의 사양을 기술|