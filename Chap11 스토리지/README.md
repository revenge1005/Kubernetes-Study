
# 1. 스토리지의 종류와 클러스터 구성

![스토리지의 종류와 클러스터 구성](https://user-images.githubusercontent.com/42735894/143768109-d62ad050-0eb1-493e-b2d1-add5726bf426.PNG)

----

# 2. 스토리지 시스템의 방식

https://kubernetes.io/ko/docs/concepts/storage/volumes/

+ OSS(오픈 소스 소프트웨어)는 별도로 시스템을 구성해야 하는데, 온프레미스 환경과 클라우드 환경 모두에서 사용할 수 있다.

+ 또한, ReadWrite 열의 Once는 ReadWrite 모드로 마운트할 수 있는 노드의 수가 하나임을 의미한다.

+ 한편, Many의 경우는 여러 노드상의 컨테이너에서 마운트하여 쓸 수 있음을 의미한다.

|스토리지 종류|분류|액세스 범위|ReadWrite|
|------|---|---|---|
|hostPath|K8s 노드|노드|Once|
|local|K8s 노드|노드|Once|
|iSCSI|OSS|클러스터|Once|
|NFS|OSS|클러스터|Many|
|GlusterFS|OSS|클러스터|Many|
|awsElasticBlockStore|클라우드 서비스|클러스터|Once|
|azureDisk|클라우드 서비스|클러스터|Once|
|azureFile|클라우드 서비스|클러스터|Many|
|gcePersistentDisk|클라우드 서비스|클러스터|Once|
|IBM Cloud Storage-File Storage|클라우드 서비스|클러스터|Many|
|IBM Cloud Storage-Block Storage|클라우드 서비스|클러스터|Once|

----

# 3. 스토리지의 추상화와 자동화

+ (A) 환경은, 퍼블릭 클라우드 환경의 방식으로 매니페스트에 스토리지 클래스를 기술하여 적용하면, 퍼시스턴트 볼륨이 동적으로 프로비저닝 된다.

+ 온프레미스 환경에서도 GlusterFS를 이용하면 동적으로 프로비저닝할 수 있다.

+ (B) '직접 스토리지를 설정하는 경우'에서는 프로비저너나 스토리지 클래스가 없어서, PVC의 매니페스트에 직접 PV명을 지정하고 있다.

+ 그리고 PV 작성과 스토리지 설정을 직접해야 한다.

+ 예를 들어 PV를 작성 매니페스트에 NFS 서버의 IP 주소나, export path 등 NFS에 접속하기 위한 설정을 기술해야 한다.

![스토리지 추상화와 자동화](https://user-images.githubusercontent.com/42735894/143769153-1113216a-ef8e-4ade-a96e-1329745c1bbf.PNG)

----

# 4. PVC(Persistent Volume Claim) 매니페스트: pvc.yml

![논리 볼륨을 동적으로 프로비저닝 하는 경우](https://user-images.githubusercontent.com/42735894/143770117-3669be76-a620-4e21-a8d2-ba64d498b19b.PNG)

----

# 3. PVC 매니페스트 작성 방법

https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-claim-v1/

```
### pvc.yml

apiVersion: v1  ##「표１PersistentVolumeClaim v1 core」
kind: PersistentVolumeClaim
metadata:       ##「표2 ObjectMeta v1 meta」
  name: data1
spec:           ##「표3 PersistentVolumeClaimSpec v1 core」
  accessModes:
  - ReadWriteOnce
  storageClassName: standard
  resources:    ##「표4」
    requests:
      storage: 2Gi
```

### (1) 표1 퍼시스턴트 볼륨 요구 API
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
apiVersion
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
v1 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kind
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
PersistentVolumeClaim 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
metadata
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
이름, 레이블, 주석 등의 정보 기술 (표2)
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
spec
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
스토리지 요구 사양을 기술 (표3)
</td>
</tr>
</table>


### (2) 표2 ObejctMeta v1 meta
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
annotations
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
스토리지 시스테에 념겨 주는 파라미터나 스토리지 클래스를 <br> 기술하기도 함
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
labels
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
IKS에서는 월 단위나 시간 단위의 과금을 클라우드의 스토리지 <br> 시스템에 부여하기 위해 사용
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
name
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
오브젝트를 특정하기 위한 필수 항목으로 네임스페이스 내에서 <br> 유일한 이름이어야 함
</td>
</tr>
</table>


### (3) 표3 퍼시스턴트 볼륨 요구 사양
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
accessModes
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
+ ReadWriteOnce: 단일 노드에서만 read/write 액세스 허용 <br> + ReadOnlyMany: 복수 노드의 read 액세스 허용 <br>
+ ReadWriteMany: 복수 노드의 read/write 액세스 허용
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
storageClassName
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
생략하면 디폴트 스토리지 클래스가 선택됨 선택 가능한 스토리지 <br> 
클래스의 목록  kubectl get storageclass로 확인 가능
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
resources
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
스토리지 용량 설정 (표4)
</td>
</tr>
</table>


### (4) 표4 자원 요구 사항
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
requests
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
퍼시스턴트 볼륨의 용량을 지정
</td>
</tr>
</table>


```
### pod.yml

apiVersion: v1
kind: Pod
metadata:
  name: pod1
spec:
  volumes:               ##「표5 Volume v1 core」참고
  - name: pvc1
    persistentVolumeClaim:
      claimName: data1   ## <-- PVC의 이름 설정
  containers:
  - name: ubuntu
    image: ubuntu:16.04
    volumeMounts:        ## 「표6 VolumeMount v1 core」참고
    - name: pvc1
      mountPath: /mnt    ## <-- 컨테이너 상 마운트 경로
```

### (5) 표5 볼륨 설정
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
name
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
볼륨명
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
persistentVolumeClaim
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
PVC 이름
</td>
</tr>
</table>


### (6) 컨테이너 내의 마운트 경로 지정
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
항목 
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
name
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
파드 스펙에 기재한 볼륨 이름을 기술
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
mountPath
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
PV의 컨테이너 내 마운트 경로
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
subPath
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
PV의 특정 디렉토리에 마운트하고 싶은 경우 이 옵션을 지정 <br>
생략하면 PV의 루트에 마운트 설정, 클라우드에서 PV 수를 정략하고 싶을 때 사용
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
readOnly
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
읽기 전용으로 하고 싶은 경우 true로 설정
</td>
</tr>
</table>

----

# 4. PV 매니페스트 작성 방법