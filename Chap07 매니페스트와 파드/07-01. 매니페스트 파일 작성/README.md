
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
```