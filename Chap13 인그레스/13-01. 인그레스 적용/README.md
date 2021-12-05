
# 1. 컨트롤러 설치 (nginx 사용)

https://kubernetes.io/ko/docs/concepts/services-networking/ingress-controllers/

```
$ kubectl get all -n ingress-nginx
NAME                                            READY   STATUS      RESTARTS   AGE
pod/ingress-nginx-admission-create--1-jc47r     0/1     Completed   0          13m
pod/ingress-nginx-admission-patch--1-pnvmc      0/1     Completed   0          13m
pod/ingress-nginx-controller-5fd866c9b6-kmc4n   1/1     Running     0          13m

NAME                                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
service/ingress-nginx-controller             NodePort    10.100.151.240   <none>        80:32209/TCP,443:30257/TCP   13m
service/ingress-nginx-controller-admission   ClusterIP   10.109.248.125   <none>        443/TCP                      13m

NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ingress-nginx-controller   1/1     1            1           13m

NAME                                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/ingress-nginx-controller-5fd866c9b6   1         1         1       13m

NAME                                       COMPLETIONS   DURATION   AGE
job.batch/ingress-nginx-admission-create   1/1           2s         13m
job.batch/ingress-nginx-admission-patch    1/1           3s         13m
```

----

# 2. 예제

```
$ kubectl apply -y application1.yml

$ kubectl apply -y application2.yml

$ kubectl apply -y application3.yml

$ kubectl apply -y ingress.yml


$ kubectl get svc,deploy,ingress
NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/helloworld-svc   NodePort    10.103.48.33    <none>        8080:31445/TCP   99s
service/java-svc         ClusterIP   10.111.169.43   <none>        9080/TCP         95s
service/kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP          37d
service/nginx-svc        ClusterIP   10.106.125.99   <none>        9080/TCP         97s

NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/helloworld-deployment   1/1     1            1           99s
deployment.apps/java-deployment         1/1     1            1           95s
deployment.apps/nginx-deployment        3/3     3            3           97s

NAME            CLASS    HOSTS                           ADDRESS          PORTS   AGE
hello-ingress   <none>   abc.sample.com,xyz.sample.com   192.168.219.11   80      7m38s


$ kubectl describe ingress
Name:             hello-ingress
Namespace:        default
Address:          192.168.219.11
Default backend:  default-http-backend:80 (<error: endpoints "default-http-backend" not found>)
Rules:
  Host            Path  Backends
  ----            ----  --------
  abc.sample.com
                  /       helloworld-svc:8080 (10.40.0.2:80)
                  /apl2   nginx-svc:9080 (10.32.0.3:80,10.32.0.5:80,10.40.0.3:80)
  xyz.sample.com
                  /   java-svc:9080 (10.40.0.4:9080)
Annotations:      kubernetes.io/ingress.class: nginx
                  nginx.ingress.kubernetes.io/rewrite-target: /
Events:
  Type    Reason  Age                From                      Message
  ----    ------  ----               ----                      -------
  Normal  Sync    18s (x2 over 46s)  nginx-ingress-controller  Scheduled for sync
```

# 3. 결과 확인

### 윈도우10(windows) -> C:\Windows\System32\drivers\etc\hosts
### 리눅스(Linux) -> /etc/hosts

```
192.168.219.11  abc.sample.com xyz.sample.com
```
![1](https://user-images.githubusercontent.com/42735894/144744511-470f113a-3906-4815-a597-8cb09abb3027.PNG)

![2](https://user-images.githubusercontent.com/42735894/144744512-6945a699-280a-4c10-9127-21e4f297cc22.PNG)

![3](https://user-images.githubusercontent.com/42735894/144744513-7b258922-7bc0-4936-8b1e-28e0d1625c42.PNG)
