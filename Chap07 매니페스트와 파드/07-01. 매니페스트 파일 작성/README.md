
# 파드의 동작 확인

```
cat <<EOF > nginx.pod.yml
apiVersion: v1               
kind: Pod
metadata:
    name: nginx
spec:                        
    containers:              
        - name: nginx
          image: nginx:latest
EOF
```

### 1. 매니페스트의 적용과 확인

```
$ kubectl apply -f nginx-pod.yml

$ kubectl get pod
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          109s
```


### 2. 파드의 IP 주소와 파드가 배포된 노드 표시

```
$ kubectl get pod nginx -o wide
NAME    READY   STATUS    RESTARTS   AGE   IP          NODE         NOMINATED NODE   READINESS GATES
nginx   1/1     Running   0          12s   10.40.0.1   k8s-node02   <none>           <none>
```