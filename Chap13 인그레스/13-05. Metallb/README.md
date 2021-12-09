
# 1. MetalLB

+ 쿠버네티스의 서비스 타입에는 NodePort, LoadBalancer 등 다양하게 지원하며, 이때 LoadBalancer는 클라우드 서비스 사업자를 위한 것으로 AWS, GCP, Azure에서 제공하는 LoadBalancer를 위한 것이다.

+ 그렇기 때문에 온-프레미스(On-Premise) 환경에서 LoadBalancer를 지원하지 않았지만, 온-프레미스 환경에서도 LoadBalancer 타입의 ExternalIP를 제공해줄 수 있는 도구가 나왔고 그것이 바로 "MetalLB"이다.