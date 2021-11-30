
# 1. MySQL 스테이트풀셋 배포 및 데이터베이스 작성

```
$ kubectl get nodes
NAME         STATUS   ROLES                  AGE   VERSION
k8s-master   Ready    control-plane,master   32d   v1.22.3
k8s-node01   Ready    <none>                 32d   v1.22.3
k8s-node02   Ready    <none>                 32d   v1.22.3

$ kubectl get all,sc,pvc,pv
NAME          READY   STATUS    RESTARTS   AGE
pod/mysql-0   1/1     Running   0          89m

NAME                                                             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/glusterfs-dynamic-4e5eae19-e8f9-4612-bfd2-6ada3681f568   ClusterIP   10.107.100.217   <none>        1/TCP      89m
service/kubernetes                                               ClusterIP   10.96.0.1        <none>        443/TCP    32d
service/mysql                                                    ClusterIP   None             <none>        3306/TCP   89m

NAME                     READY   AGE
statefulset.apps/mysql   1/1     89m

NAME                                         PROVISIONER               RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
storageclass.storage.k8s.io/gluster-heketi   kubernetes.io/glusterfs   Delete          Immediate           false                  89m

NAME                                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS     AGE
persistentvolumeclaim/pvc-mysql-0   Bound    pvc-4e5eae19-e8f9-4612-bfd2-6ada3681f568   2Gi        RWO            gluster-heketi   89m

NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                 STORAGECLASS     REASON   AGE
persistentvolume/pvc-4e5eae19-e8f9-4612-bfd2-6ada3681f568   2Gi        RWO            Delete           Bound    default/pvc-mysql-0   gluster-heketi            89m

$ kubectl exec -it mysql-0 bash
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.
root@mysql-0:/# mysql -u root -pqwerty

mysql> create database test1234;
Query OK, 1 row affected (0.02 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test1234           |
+--------------------+
5 rows in set (0.03 sec)
```

----

# 2. 임의로 장애를 발생시킨 후 서비스 복구될 때까지

```
$ while true; do date; kubectl get pod -o wide;echo; sleep 15;done
## k8s-node01 셧다운 완료
Tue 30 Nov 2021 05:39:17 PM KST
NAME      READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          92m   10.32.0.3   k8s-node01   <none>           <none>

## k8s-node01 정지 상태 시간 경과
Tue 30 Nov 2021 05:41:03 PM KST
NAME      READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          94m   10.32.0.3   k8s-node01   <none>           <none>

## k8s-node02에서 스테이트풀셋 파드가 복구
Tue 30 Nov 2021 05:41:18 PM KST
NAME      READY   STATUS              RESTARTS   AGE   IP       NODE         NOMINATED NODE   READINESS GATES
mysql-0   0/1     ContainerCreating   0          9s    <none>   k8s-node02   <none>           <none>

## k8s-node02에서 MySQL 서비스 제공 중
Tue 30 Nov 2021 05:41:33 PM KST
NAME      READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          24s   10.32.0.1   k8s-node02   <none>           <none>
```

----

# 3. 복구한 파드에서 퍼시스턴트 볼륨 확인

```
$kubectl get pod mysql-0 -o wide
NAME      READY   STATUS    RESTARTS   AGE     IP          NODE         NOMINATED NODE   READINESS GATES
mysql-0   1/1     Running   0          3m19s   10.32.0.1   k8s-node02   <none>           <none>


$ kubectl exec -it mysql-0 bash
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.
root@mysql-0:/# mysql -u root -pqwerty

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test1234           |
+--------------------+
5 rows in set (0.02 sec)
```