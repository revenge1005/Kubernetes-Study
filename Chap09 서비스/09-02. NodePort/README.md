
```
$ kubectl get node -o wide
NAME         STATUS   ROLES                  AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
k8s-master   Ready    control-plane,master   29d   v1.22.3   192.168.219.10   <none>        Ubuntu 20.04.2 LTS   5.4.0-89-generic   docker://20.10.10
k8s-node01   Ready    <none>                 29d   v1.22.3   192.168.219.11   <none>        Ubuntu 20.04.2 LTS   5.4.0-89-generic   docker://20.10.10
k8s-node02   Ready    <none>                 29d   v1.22.3   192.168.219.12   <none>        Ubuntu 20.04.2 LTS   5.4.0-89-generic   docker://20.10.10
```

----

```
$  kubectl apply -f deploy.yml
deployment.apps/web-deploy created

$ kubectl apply -f svc-np.yml
service/web-service-np created
```

----

```
$  kubectl get service
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP        29d
web-service-np   NodePort    10.110.173.63   <none>        80:31058/TCP   6s
```

----

```
$ curl http://192.168.219.10:31058
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
...

$ curl http://192.168.219.11:31058
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
...

$ curl http://192.168.219.12:31058
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
...
```