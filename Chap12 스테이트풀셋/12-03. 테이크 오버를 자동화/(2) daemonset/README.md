
# 1. 클러스터 구성 변경 자동 대응

+ 데몬셋은 쿠버네티스를 구성하는 모든 노드에서 파드를 실행하기 위해 존재하는 컨트롤러이다.

+ 데몬셋 관리하의 파드는 K8s 클러스터의 모든 노드에서 실행되며, 클러스터에서 노드가 하나 삭제되면 데몬셋 관리하의 파드도 그 노드에서 제거된다.

+ 그리고 데몬셋 컨트롤러가 삭제되면, 그 관리하의 파드는 모든 노드에서 삭제된다.

+ 데몬셋을 사용하여 전체 노드가 아닌 일부 노드에만 파드를 배치하고 싶은 경우에는 노드 셀렉터를 설정하면 된다.

----

# 2. 매니페스트 작성 : daemonset.yml

```
apiVersion: apps/v1        # 표1
kind: DaemonSet
metadata:
  name: liberator
  namespace: tkr-system    # 시스템 전용 네임스페이스
spec:                      # 표2
  selector:
    matchLabels:
      name: liberator
  template:                # 표3
    metadata:
      labels:
        name: liberator
    spec:                  # 표4
      serviceAccountName: high-availability # 권한을 가진 서비스 어카운트
      containers:          # 표5
      - name: liberator
        image: maho/liberator:0.1
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
```

### 데몬셋 API 표1
|항목|설명|
|------|---|
|apiVersion|apps/v1 설정|
|kind|DaemonSet 설정|
|metadata|+ name : 데몬셋의 이름 <br> + namespace : 네임스페이스 이름|
|spec|데몬셋의 사양 (표2)|

### 데몬셋 사양 표2
|항목|설명|
|------|---|
|selector|템플릿으로 작성되는 파드와의 대응을 위해 필수적으로 설정|
|template|파드를 만들기 위한 사양 (표3)|

### 파드 템플릿 사양 표3
|항목|설명|
|------|---|
|metadata|[표(서비스 어카운트와 클러스터 롤의 대응)](https://github.com/revenge1005/Kubernetes-Study/tree/main/Chap12%20%EC%8A%A4%ED%85%8C%EC%9D%B4%ED%8A%B8%ED%92%80%EC%85%8B/12-03.%20%ED%85%8C%EC%9D%B4%ED%81%AC%20%EC%98%A4%EB%B2%84%EB%A5%BC%20%EC%9E%90%EB%8F%99%ED%99%94#2-3-%EC%84%9C%EB%B9%84%EC%8A%A4-%EC%96%B4%EC%B9%B4%EC%9A%B4%ED%8A%B8%EC%99%80-%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0-%EB%A1%A4%EC%9D%98-%EB%8C%80%EC%9D%91-%ED%91%9C4)의 selector과 대응하는 라벨을 설정|
|spec|파드의 사양 (표4)|

### 파드 사양 표4
|항목|설명|
|------|---|
|serviceAccountName|액세스 권한을 부여하기 위한 서비스 어카운트명|
|containers|컨테이너 사양을 기술 (표5)|
|nodeSelector|라벨과 일치하는 노드에 파드를 스케줄|

### 컨테이너의 각종 설정과 기동 조건 표5
|항목|설명|
|------|---|
|name|액세스 권한을 부여하기 위해 서비스 어카운트명을 설정|
|image|컨테이너 사양을 기술|
|resources|컨테이너의 CPU시간과 메모리 요구량(requests)과 상한(limits)을 설정|

----

# 3. 적용 결과 확인

```
$ kubectl apply -f daemonset.yml
daemonset.apps/liberator created

## 데몬셋 관리하의 파드 기동 상태
$ kubectl get ds -n tkr-system
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
liberator   2         2         0       2            0           <none>          25s

## 기동 완료 상태
$ kubectl get pod -n tkr-system -o wide
NAME              READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
liberator-2zjq6   1/1     Running   0          67s   10.40.0.2   k8s-node02   <none>           <none>
liberator-nszcq   1/1     Running   0          67s   10.32.0.4   k8s-node01   <none>           <none>

## 데몬셋 상태
$ kubectl get ds -n tkr-system
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
liberator   2         2         2       2            2           <none>          87s
```

