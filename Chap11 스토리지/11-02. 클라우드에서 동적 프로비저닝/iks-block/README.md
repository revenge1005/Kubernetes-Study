
# 1. IKS PVC 결과 확인

```
$ kubectl get node
NAME           STATUS  ROLES   AGE     VERSION
10.193.10.14   Ready   <none>  2d18h   v1.xx.x+IKS
10.193.10.58   Ready   <none>  2d18h   v1.xx.x+IKS

$ kubectl apply -f iks-pvc-block.yml
persistentvolumeclaim/bronze-blk  created

$ kubectl get pvc
NAME           STATUS  VOLUME       CAPACITY   ACCESS MODES    STORAGECLASS        AGE
bronze-blk     Bound   pvc-290ad8   20Gi       RWO             ibmc-block-bronze   3m57s

$ kubectl get pv
NAME           CAPACITY   ACCESS MODES    RECLAIM POLICY    STATUS  CLAIM
pvc-290ad8     20Gi       RWO             Delete            Bound   default/bronze-blk
```

----

# 2. GKE PVC 결과 확인

```
$ kubectl get node
NAME                                   STATUS  ROLES   AGE     VERSION
gke-gke-1-default-pool-4b8e4604-mlwr   Ready   <none>  18h     v1.xx.x-gke.xx
gke-gke-1-default-pool-4b8e4604-t0lq   Ready   <none>  18h     v1.xx.x-gke.xx

$ kubectl apply -f gke-pvc-block.yml
persistentvolumeclaim/bronze-blk  created

$ kubectl get pvc
NAME           STATUS  VOLUME        CAPACITY   ACCESS MODES    STORAGECLASS        AGE
bronze-blk     Bound   pvc-4aa4ee42  20Gi       RWO             standard            5s

$ kubectl get pv
NAME           CAPACITY   ACCESS MODES    RECLAIM POLICY    STATUS  CLAIM
pvc-4aa4ee42   20Gi       RWO             Delete            Bound   default/bronze-blk
```

----

# 3. 블록 디바이스를 마운트한 파드

```
$ kubectl apply -f deploy-1pod.yml

$ kubectl get deploy,pod
NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
deployment.extensions/dep1pod-blk   1/1     1            1           19s

NAME                                  READY   STATUS    RESTARTS   AGE
pod/dep1pod-blk-6989fcb9bf<F4>8z8rz   1/1     Running   0          2m

$ kubectl exec -it dep1pod-blk-6989fcb9bf<F4>8z8rz bash
root@dep1pod-blk-6989fcb9bf<F4>8z8rz:/# df -h
Filesystem                                       Size  Used Avail Use% Mounted on
overlay                                          1.8T  1.3G  1.7T   1% /
tmpfs                                             64M     0   64M   0% /dev
tmpfs                                             16G     0   16G   0% /sys/fs/cgroup
/dev/mapper/docker_data                          1.8T  1.3G  1.7T   1% /etc/hosts
shm                                               64M     0   64M   0% /dem/shm
/dev/mapper/3600a09803830446d445d4c3066664758     20G   44M   20G   1% /mnt
```

