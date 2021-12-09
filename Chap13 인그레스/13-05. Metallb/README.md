----

> # 1. MetalLB

+ 쿠버네티스의 서비스 타입에는 NodePort, LoadBalancer 등 다양하게 지원하며, 이때 LoadBalancer는 클라우드 서비스 사업자를 위한 것으로 AWS, GCP, Azure에서 제공하는 LoadBalancer를 위한 것이다.

+ 그렇기 때문에 온-프레미스(On-Premise) 환경에서 LoadBalancer를 지원하지 않았지만, 온-프레미스 환경에서도 LoadBalancer 타입의 ExternalIP를 제공해줄 수 있는 도구가 나왔고 그것이 바로 "MetalLB"이다.

<br>

----

> # 2. NodePort, LoadBalancer 서비스 타입과 MetalLB 동작 과정 비교

### (1) NodePort

![nodeport](https://user-images.githubusercontent.com/42735894/145426933-f77ea90e-0b5d-471c-bdd7-a5c7ff172137.PNG)

----

### (2) LoadBalancer (Cloud)

![cloud_loadbalancer](https://user-images.githubusercontent.com/42735894/145426952-21a9330e-faba-4999-8e83-3b6c1a191b77.PNG)

----

### (3) MetalLB

+ **MetalLB Controller : 작동 방식 (프로토콜)을 정의하고, External-IP 부여하여 관리한다.**

+ **MetalLB speaker : 정해진 프로토콜 (L2/ARP, L3/BGP)에 따라 경로를 만들 수 있게 네트워크 정보를 광고하고 수집해 각 파드의 경로를 제공**

![metallb](https://user-images.githubusercontent.com/42735894/145426946-9f727058-13b4-4cbf-b714-7e6cd83c91a0.PNG)

<br>

----

> # 3. NodePort, LoadBalancer 서비스 타입과 MetalLB 동작 과정 비교