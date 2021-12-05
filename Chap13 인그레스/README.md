----

> # 1. 인그레스 (ingress)

+ k8s 클러스터 외부에서의 요청을 k8s 클러스터 내부의 애플리케이션에 연결하기 위한 API 오브젝트

+ 디플로이먼트 관리하의 애플리케이션을 외부 공개용 URL과 매칭하여 인터넷에 공개하는데 사용

+ 인그레스 컨트롤러는 다른 컨트롤러와 달리 마스터상의 Kube-controller-manager의 일부로 실행되지 않는다.

+ 다양한 인그레스 컨트롤러가 있는데, 그중에서도 Nginx 인그레스 컨트롤러가 대표적이다.

![인그레스](https://user-images.githubusercontent.com/42735894/144570087-86f4557c-93e9-4eb5-ae58-67b0dcae763f.png)

----

> # 2. 인그레스 기능 

+ 기존의 로드밸런서나 리버스 프록시를 대체, 공개 URL과 애플리케이션 매핑

+ 복수의 도메인 이름을 가지고 가상 호스트 기능

+ 클라이언트의 요청을 여러 파드에 분산

+ SSL/TSL 암호화 통신 HTTPS

+ 세션 어피니티

----

> # 3. 인그레스 주의

+ 인그레스 컨트롤러의 구현에 따라 인터넷 공인 IP를 취득하는 기능이 포함되지 않을 수도 있다.

 - 그래서 퍼블릭 클라우드의 K8s 관리 서비스는 클라우드의 기능과 인그레스를 연동하여 공인 IP 주소를 연결한다.

+ 온프레미스에서 k8s 클러스터를 구축하는 겨웅에는 공인 IP 주소(이하, VIP)를 노드 간에 공요하는 기능을 추가해야 한다.

 - 이 기능을 위해 kube-keepalived-vip가 깃헙에 공개되어 있다.

 - kube-keepalived-vip는 쿠버네티스의 소스 코드에는 포함되지 않지만, CNCF 쿠버네티스 프로젝트의 깃헙에 등록되어 있다.

----

> # 4. 공개 URL과 애플리케이션의 매핑

+ 인그레스를 사용하면 공개 URL의 경로 부분에 복수의 애플리케이션을 매핑할 수 있다.

```
"http://abc.sample.com/reservation" (예약 애플리케이션 파드에 전송)
"http://abc.sample.com/order" (주문 애플리케이션 파드에 전송)
```

+ 그러면 사용자 입장에서는 하나의 URL이지만 내부적으로 애플리케이션이 적절히 분리되어 있어 마이크로 서비스 처럼 애플리케이션을 분할하고 느슨하게 연결함으로써 각 모듈의 변경에 의한 영향을 최소화할 수 있고 개발 생산성에도 유리하다.

![예시](https://user-images.githubusercontent.com/42735894/144582635-a1851e47-5e62-47be-b177-4d8279abe3c6.PNG)

----

> # 5. 가상 호스트와 서비스를 매핑하는 매니페스트 기술

+ 인그레스의 매니페스트에서는 메타데이터와 어노테이션이 중요한 역할을 수행한다.

+ 어노테이션에 키와 값을 기재하여, 인그레스 컨트롤러에 명령을 전달한한다고 볼 수 있다.

 - kubernetes.io/ingress.class: 'nginx'

    + 여러 인그레스 컨트롤러가 K8s 클러스터에서 동작 중인 경우에는 이 어노테이션을 명시적으로 지정할 필요학 있다.

 - nginx.ingress.kubernetes.io/rewrite-target: / 

    + URL 경로를 바꾸도록 하는 어노테이션

    + 이 설정이 없으면 클라이언트로부터의 요청 경로를 파드에게 그대로 전송하여 File NotFound 에러로 연결될 수 있다.

----

> # 6. 컨피그맵(ConfigMap)

+ 컨피그맵이란 설정 파일을 네임스페이스에 저장하는 오브젝트

+ 파드는 컨피그맵을 디스크처럼 마운트할 수 있다 예를 들면, 미들웨어의 설정 파일을 컨피그맵으로 저장하면 파드가 네임스페이스에서 읽어 들일 수 있다.

----

> # 7. 가상 호스트와 서비스의 매핑

https://kubernetes.io/docs/reference/kubernetes-api/service-resources/ingress-v1/

```
apiVersion: networking.k8s.io/v1                        ## 표1
kind: Ingress
metadata:
  name: hello-ingress
  annotations:                                          ## 인그레스 컨틀롤러 설정
    kubernetes.io/ingress.class: 'nginx'
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:                                                   ## 표2
  rules:                                                ## 표3
  - host: abc.sample.com                                 # 도메인 1
    http:
      paths:                                            ## 표4
      - path: /                                         ## 표5
        pathType: Prefix
        backend:                                        ## 표6
          service:
            name: helloworld-svc
            port:
              number: 8080
      - path: /pay                                  # URL 패스 2
        pathType: Prefix
        backend:                                         # 대응하는 서비스명과 포트 번호
          service:
            name: nginx-svc
            port:
              number: 9080
  - host: xyz.sample.com                                 # 도메인 2
    http:
      paths:
      - path: /                                          # 도메인 2의 패스
        pathType: Prefix
        backend:
          service:
            name: java-svc                          # 도메인 2 패스에 대응하는 서비스
            port:
              number: 9080
```

### (1) 표1 인그레스 API 

|항목|설명|
|------|---|
|apiVersion|networking.k8s.io/v1 설정|
|kind|Ingress 설정|
|metadata.name|인그레스 오브젝트의 이름|
|metadata.annotations|인그레스 컨트롤러 설정에 사용|
|spec|표2 참고|

### (2) 표2 인그레스의 사양

|항목|설명|
|------|---|
|rules|DNS명과 백엔드 서비스를 대응시키는 규칙 목록 (표3 참고)|
|tls|표7 참고|

### (3) 표3 인스레스 규칙

|항목|설명|
|------|---|
|host|FQDN(Fully Qualified Domain Name) 설정|
|http|표4 참고|

### (4) 표4 URL 경로와 백엔드 서비스의 대응 배열

|항목|설명|
|------|---|
|paths|URL의 경로와 백엔드 서비스를 대응시키기는 목록을 기술 (표5 참고)|

### (5) 표5 URL 경로와 백엔드 서비스 대응

|항목|설명|
|------|---|
|path|URL 주소의 경로 부분을 기재|
|backend|요청이 전달될 서비스와 포트번호 기재 (표6 참고)|

### (6) 표6 전송될 서비스의 이름과 포트번호

|항목|설명|
|------|---|
|service.name|서비스 이름|
|service.port.number|서비스 포트번호|

### (7) 표7 전송될 서비스의 이름과 포트번호

|항목|설명|
|------|---|
|hosts|도메인명 목록|
|serviceName|서버 인증서 시크릿의 이름, 시크릿은 네임스페이스 내에 보안이 필요한 데이터를 보존하는 오브젝트로 컨테이너에서 볼륨으로 마운트 가능|