
# 1. NFS 서버 사용하는 경우의 구성



-----

# 2. PV(Persistent Volume)의 매니페스트 작성: nfs-pv.yml

```
apiVersion: v1  ## 「표1  PersistentVolume v1 core」참고
kind: PersistentVolume
metadata:       ## 표2 참고
  name: nfs-1
  labels:
    name: pv-nfs-1
spec:           ## 표3 참고
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteMany
  nfs:          ## 표4 참고
    server: 172.16.20.10  ## NFS서버 IP주소
    path: /export         ## NFS서버 공개 경로
```

