
# 1. 온프레미스 환경에서 SDS에 의한 동적 프로비저닝

+ 퍼블릭 클라우드에서는 PVC를 만들면 자동으로 PV가 만들어져 컨테이너로부터 이용할 수 있다.

+ 하지만 온프레미스 환경에서 K8s 클러스터를 구축한 경우, 일일이 수작업으로 NFS 서버와 연동하는 것은 큰 부담이 된다.

+ 이 문제는 쿠버네티스와 SDS(Software Defined Storage)를 연동하면 해결되며, PV의 동적 프로비저닝을 실현할 수 있다.

+ 이 실습에서는 SDS로 자주 사용디는 GlusterFS를 사용하며, 쿠버네티스와의 연동을 위해 REST로 GlusterFS를 조작하는 Heketi라는 오픈 소스를 깃허브으로 공개하고 있다.

+ (GlusterFS와 Heketi 구성된 상태로 가정하고 진행한다)

----

# 2. 결과 확인 - GlusterFS 스토리지 시스템 마운트 확인

```
$ kubectl apply -f gfs-sc.yml
storageclass.storage.k8s.io/gluster-heketi created

$ kubectl apply -f gfs-pvc.yml
persistentvolumeclaim/gvol-1 created

$ kubectl get sc,pvc,pv
NAME                                         PROVISIONER               RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
storageclass.storage.k8s.io/gluster-heketi   kubernetes.io/glusterfs   Delete          Immediate           false                  3m50s

NAME                           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS     AGE
persistentvolumeclaim/gvol-1   Bound    pvc-ddfacba8-af3a-4800-97b8-fa4d16547e55   10Gi       RWO            gluster-heketi   3m47s

NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM            STORAGECLASS     REASON   AGE
persistentvolume/pvc-ddfacba8-af3a-4800-97b8-fa4d16547e55   10Gi       RWO            Delete           Bound    default/gvol-1   gluster-heketi            3m42s
```

----

# 3. 결과 확인 - GlusterFS을 적용한 파드 기동

```
$ kubectl get pod
NAME                          READY   STATUS    RESTARTS   AGE
gfs-client-6557c98dbd-cpqwd   1/1     Running   0          6s
gfs-client-6557c98dbd-vznk2   1/1     Running   0          6s


## 첫 번째 파드
$ kubectl exec -it gfs-client-6557c98dbd-cpqwd bash
root@gfs-client-6557c98dbd-cpqwd:/# df -h
Filesystem                                            Size  Used Avail Use% Mounted on
overlay                                               9.8G  2.6G  6.8G  28% /
tmpfs                                                  64M     0   64M   0% /dev
tmpfs                                                 980M     0  980M   0% /sys/fs/cgroup
192.168.219.201:vol_d97ad92869bbafbfb71d2e5e3210d21e   10G  207M  9.8G   3% /mnt
/dev/mapper/ubuntu--lvm-var                           9.8G  2.6G  6.8G  28% /etc/hosts
shm                                                    64M     0   64M   0% /dev/shm
tmpfs                                                 1.9G   12K  1.9G   1% /run/secrets/kubernetes.io/serviceaccount
tmpfs                                                 980M     0  980M   0% /proc/acpi
tmpfs                                                 980M     0  980M   0% /proc/scsi
tmpfs                                                 980M     0  980M   0% /sys/firmware

root@gfs-client-6557c98dbd-cpqwd:/# ls -lR / > /mnt/test.dat

root@gfs-client-6557c98dbd-cpqwd:/# md5sum /mnt/test.dat
fb22dcbcde6b282e21bf77784a99bf5b  /mnt/test.dat



## 두 번째 파드
$ kubectl exec -it gfs-client-6557c98dbd-vznk2 bash
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.
groups: cannot find name for group ID 2000
root@gfs-client-6557c98dbd-vznk2:/# df -h
Filesystem                                            Size  Used Avail Use% Mounted on
overlay                                               9.8G  2.4G  6.9G  26% /
tmpfs                                                  64M     0   64M   0% /dev
tmpfs                                                 980M     0  980M   0% /sys/fs/cgroup
192.168.219.202:vol_d97ad92869bbafbfb71d2e5e3210d21e   10G  207M  9.8G   3% /mnt
/dev/mapper/ubuntu--lvm-var                           9.8G  2.4G  6.9G  26% /etc/hosts
shm                                                    64M     0   64M   0% /dev/shm
tmpfs                                                 1.9G   12K  1.9G   1% /run/secrets/kubernetes.io/serviceaccount
tmpfs                                                 980M     0  980M   0% /proc/acpi
tmpfs                                                 980M     0  980M   0% /proc/scsi
tmpfs                                                 980M     0  980M   0% /sys/firmware

root@gfs-client-6557c98dbd-vznk2:/# md5sum /mnt/test.dat
fb22dcbcde6b282e21bf77784a99bf5b  /mnt/test.dat
```