
# 1. NFS 서버 사용하는 경우의 구성

![NFS 서버를 사용하는 경우의 구성](https://user-images.githubusercontent.com/42735894/143775424-1f8c18a5-e92b-4ab8-978b-39381a5d12c6.PNG)

-----

# 2. PV(Persistent Volume)의 매니페스트 작성: nfs-pv.yml

https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-v1/

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

### (1) 표1 퍼시스턴트 볼륨 API
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
PersistentVolume 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
metadata
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
이름, 레이블 정보 기술 (표2)
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
spec
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
퍼시스턴트 볼륨 사양을 기술 (표3)
</td>
</tr>
</table>


### (2) 표2 메타데이터 
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
labels
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
PVC와 PV를 대응시키기 위하여 사용
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
name
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
필수 항목, 네임스페이스 내에서 유일한 이름을 지정
</td>
</tr>
</table>


### (3) 표3 퍼시스턴트 볼륨 사양
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
capacity
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
볼륨 용량 지정, (NFS에서도 값을 설정해야 하지만 의미는 없음)
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
accessMode
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
<a href="https://github.com/revenge1005/Kubernetes-Study/tree/main/Chap11%20%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80#3-%ED%91%9C3-%ED%8D%BC%EC%8B%9C%EC%8A%A4%ED%84%B4%ED%8A%B8-%EB%B3%BC%EB%A5%A8-%EC%9A%94%EA%B5%AC-%EC%82%AC%EC%96%91">PVC 사양 참고</a>
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
NFS
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
NFS를 사용하는 경우에는 파라미터를 설정 표 4 참고
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
GlusterFS / hostPath / local ...
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
스토리지 시스템별 파라미터를 기술은 쿠버네티스 API 내용 참고
</td>
</tr>
</table>


### (4) 표4 NFS 서버의 주소와 공개 경로
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
path
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
NFS 서버가 export하는 경로
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
server
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
NFS 서버의 DNS명 또는 IP 주소
</td>
</tr>
</table>

-----

# 3. PVC(Persistent Volume Claim)의 매니페스트 작성: nfs-pvc.yml

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-1
spec:
  accessModes:
  - ReadWriteMany
  storageClassName: "" ## PV를 라벨로 매치하기 위해 Null을 설정
  resources:
    requests:
      storage: "100Mi"
  selector:            ## 대응하는 PV의 라벨을 설정
    matchLabels:
      name: pv-nfs-1
```

### (1) PersistentVolumeClaimSpec 
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
storageClassName
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
스토리지 클래스가 없는 퍼시스턴트 볼륨을 사용하므로 문자열 ""을 설정. <br>
이 항목을 생략하면 디폴트의 스토리지 클래스가 사용되기 때문에 반드시 "" 설정이 필요
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
selector
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
접속할 PV의 metadata.labels와 일치해야 함
</td>
</tr>
</table>

----

# 4. 결과 확인 - NFS 서버와 마운트

```
$ kubectl apply -f  nfs-pv.yml
persistentvolume/nfs-1 created

$ kubectl apply -f  nfs-pvc.yml
persistentvolumeclaim/nfs-1 created

$ kubectl get pv,pvc
NAME                     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM           STORAGECLASS   REASON   AGE
persistentvolume/nfs-1   100Mi      RWX            Retain           Bound    default/nfs-1                           39s

NAME                          STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/nfs-1   Bound    nfs-1    100Mi      RWX                           35s
```

----

# 5. 결과 확인 - PVC의 볼륨을 마운트하는 디폴로이먼트

```
$ kubectl get pod
NAME                         READY   STATUS    RESTARTS   AGE
nfs-client-7ff95d88b-74mtp   1/1     Running   0          21s
nfs-client-7ff95d88b-rvgq2   1/1     Running   0          21s

$ kubectl exec -it nfs-client-7ff95d88b-74mtp bash
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.

root@nfs-client-7ff95d88b-74mtp:/# df -h
Filesystem                       Size  Used Avail Use% Mounted on
overlay                          9.8G  2.6G  6.8G  28% /
tmpfs                             64M     0   64M   0% /dev
tmpfs                            980M     0  980M   0% /sys/fs/cgroup
192.168.219.129:/home/share/nfs   29G  5.6G   22G  21% /mnt

root@nfs-client-7ff95d88b-74mtp:/# ls -lR > /mnt/test.dat

root@nfs-client-7ff95d88b-74mtp:/# md5sum /mnt/test.dat
2ffcda59cfc06e6af491a5e36c70256f  /mnt/test.dat

root@nfs-client-7ff95d88b-74mtp:/# exit

## 다른 파드에서 확인

$ kubectl exec -it nfs-client-7ff95d88b-rvgq2 bash
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.

root@nfs-client-7ff95d88b-rvgq2:/# df -h
Filesystem                       Size  Used Avail Use% Mounted on
overlay                          9.8G  2.4G  6.9G  26% /
tmpfs                             64M     0   64M   0% /dev
tmpfs                            980M     0  980M   0% /sys/fs/cgroup
192.168.219.129:/home/share/nfs   29G  5.6G   22G  21% /mnt

root@nfs-client-7ff95d88b-rvgq2:/# md5sum /mnt/test.dat
2ffcda59cfc06e6af491a5e36c70256f  /mnt/test.dat
```