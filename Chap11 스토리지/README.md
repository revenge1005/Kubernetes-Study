
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