
# 1. 서버 이중화의 과제

+ 브라우저에서 사용하는 HTTP는 무상태 프로토콜(Stateless Protocol)이어서 서버와 클라이언트 간의 통신을 유지할 수 없다.

    - 그래서 애플리케이션은 브라우저를 식별하기 위해 쿠키(Cookie)를 HTTP 프로토콜의 헤더에 포함시켜 전송한다.

    - 브라우저는 쿠키를 보관해 뒀더가 같은 URL에 접근할 때는 기억해 둔 쿠기를 HTTP 헤더에 기재항여 전송한다.

+ 웹 애플리케이션의 서버가 한 대만 있으면 괜찮지만 여러 대의 서버를 두고 그 앞에 로드밸런서를 두는 경우에는 또 다른 문제가 발생한다.

    - 로드밸런서가 세션 정보를 가지고 있지 않은 서버에 요청을 전달해 버리면, 올바른 처리를 수행할 수 없게 되기 때문이다.

    - 그러면 로그인을 했는데 다시 로그인 화면이 뜨는 일이 벌어질 것이다.

+ 이 문제를 해결하기 위한 기능으로 로드밸런서에는 세션 어피니티(=sticky session)가 있다.

    - 브라우저에서의 요청을 언제나 동일한 서버의 프로세스에 전달한다. (즉, 세션 정보를 가지고 있는 애플리케이션 프로세스에 전송해 주는 것이다.)

+ 한편, The Twelve Factor Apps에서는 세션 정보를 외부 캐시에 보관하는 것을 추천한다. 
    
    - 이에 따라 쿠버네티스도 세션 정보를 파드 외부의 캐시에 보관하는 것을 가정하고 있다.

    - 서비스 컨트롤러의 부하분산 기능을 요청을 파드들에게 랜덤하게 전송할 뿐이다.

    - 하지만 인그레스는 세션 어피니티 기능을 제공하며, 이를 통해 기존 애플리케이션의 코드 수정을 최소화 할 수 있다.

![111](https://user-images.githubusercontent.com/42735894/144751653-0c6fbea5-e55b-4f65-8305-915fc91e9773.PNG)

<br>

# 2. 세션 어피니티 기능 사용

```
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: hello-ingress
  annotations:
    kubernetes.io/ingress.class: 'nginx'
    nginx.ingress.kubernetes.io/affinity: 'cookie'   # (1) 세션 어피니티 활성화
spec:
  rules:
  - host: abc.sample.com
    http:
      paths:
      - path: /
        backend:
          serviceName: session-svc
          servicePort: 9080
```

### (1) 테스트 환경 구성

```
$ kubectl get all,ingress
NAME                                      READY   STATUS    RESTARTS   AGE
pod/session-deployment-55b4fb777f-4gfq2   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-4h8hw   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-5bxgz   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-7lsqz   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-g9p9w   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-kpt26   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-lwm2d   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-mrq9z   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-q9j9r   1/1     Running   0          3m28s
pod/session-deployment-55b4fb777f-xv946   1/1     Running   0          3m28s

NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/kubernetes    ClusterIP   10.96.0.1       <none>        443/TCP    38d
service/session-svc   ClusterIP   10.102.76.166   <none>        9080/TCP   3m28s

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/session-deployment   10/10   10           10          3m28s

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/session-deployment-55b4fb777f   10        10        10      3m28s

NAME                                      CLASS    HOSTS            ADDRESS          PORTS   AGE
ingress.networking.k8s.io/hello-ingress   <none>   abc.sample.com   192.168.219.11   80      6m39s
```


### (2) 세션 어피니티를 사용하지 않은 경우 

+ curl -c 옵션 : 요청을 보내고, 응답 쿠키를 파일에 저장

+ curl -b 옵션 : 저장한 쿠키를 헤더에 추가해서 요청

+ 매번 요청이 전달되는 파드가 달라져서 카운트 값이 증가하지 않는다.

```
$ curl -c cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-4gfq2<br>
1th time access.

$ curl -b cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-4h8hw<br>
1th time access.

$ curl -b cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-5bxgz<br>
1th time access.

$ curl -b cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-q9j9r<br>
1th time access.

$ curl -b cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-7lsqz<br>
1th time access.
```


### (3) 세션 어피니티를 사용한 경우

+ 쿠키 값에 따라 파드가 결정되어 카운트 값이 증가한 것을 알 수 있다.

```
$ curl -c cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-f99dx<br>
1th time access.

$ curl -b cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-f99dx<br>
2th time access.

$ curl -b cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-f99dx<br>
3th time access.

$ curl -b cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-f99dx<br>
4th time access.

$ curl -b cookie.dat http://abc.sample.com:32209
Hostname: session-deployment-55b4fb777f-f99dx<br>
5th time access.
```