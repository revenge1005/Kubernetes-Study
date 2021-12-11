----

> # 1. 네임스페이스

+ 네임스페이스는 K8s 클러스터를 논리적으로 분할하는 사용한다.

+ 'Chap 12'에서도 명령어가 적용되는 범위를 한정하기 위해 네임스페이스를 사용했었다.

+ 네임스페이스를 사용하여 논리적으로 구분할 수 있는 대상은 '명령어의 적용 범위' 뿐만 아니라 CPU 시간과 메모리 용량 등의 리소스 할당 그리고 파드 네트워크 통신의 접근제어도 구분하여 설정할 수 있다.

+ 이와 같이 네임스페이스는 하나의 물리적 K8s 클러스터를 가상화하여 여러 개의 K8s 클러스터가 있는 것처럼 사용이 가능하다.

----

+ 네임스페이스를 만들면 서비스 어카운트 default와 그에 대응하는 시크릿이 만들어 진다.

```
## prod라는 네임스페이스 작성
$ kubectl create namespace prod
namespace/prod created

## prod 네임스페이스의 서비스 어카운트 목록 확인
$  kubectl get sa -n prod
NAME      SECRETS   AGE
default   1         18s

## 서비스 어카운트의 시크릿도 만들어짐
$ kubectl get secrets -n prod
NAME                  TYPE                                  DATA   AGE
default-token-57fjd   kubernetes.io/service-account-token   3      31s

## kubectl describe secrets default-token-57fjd -n prod
Name:         default-token-57fjd
Namespace:    prod
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: default
              kubernetes.io/service-account.uid: 9263b76d-1769-4df8-8531-c013866584f7

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1099 bytes      ## 클라이언트 인증서
namespace:  4 bytes         ## 네임스페이스명
token:      eyJhbG<생략>    ## 서비스 어카운트 토큰
```

+ "시크릿"에는 클라이언트 인증서, 네임스페이스 이름, 서비스 어카운트의 토큰이 들어 있다.

+ "시크릿"은 이 네임스페이스에 있는 파드의 컨테이너에 마운트되어 사용된다.

```
## 네임스페이스 prod에 파드가 기동되면, 서비스 어카운트의 시크릿이 자동으로 마운트되어
## 파드는 이 서비스 어카운트에 부여된 액세스 권한을 얻게 된다.

$ kubectl run -it test --image=ubuntu:16.04 --restart=Never --rm -n prod /bin/bash

root@test:/# df -h
Filesystem                   Size  Used Avail Use% Mounted on
overlay                      9.8G  1.8G  7.5G  20% /
tmpfs                         64M     0   64M   0% /dev
tmpfs                        980M     0  980M   0% /sys/fs/cgroup
/dev/mapper/ubuntu--lvm-var  9.8G  1.8G  7.5G  20% /etc/hosts
shm                           64M     0   64M   0% /dev/shm
tmpfs                        1.9G   12K  1.9G   1% /run/secrets/kubernetes.io/serviceaccount
tmpfs                        980M     0  980M   0% /proc/acpi
tmpfs                        980M     0  980M   0% /proc/scsi
tmpfs                        980M     0  980M   0% /sys/firmware

## 시크릿이 마운트되어 있음
root@test:/# ls /run/secrets/kubernetes.io/serviceaccount/
ca.crt  namespace  token
```

----

+ 하나의 K8s 클러스터에 운영 환경과 테스트 환경을 같이 돌리고 싶은 경우가 있다.

+ 이때 하나의 네임스페이스 내에서는 중복된 오브젝트의 이름이 허용되지 않기 때문에 매니페스트를 수정하여 오브젝트의 이름을 변경해야 하는 번거로움이 있다.

+ 이런 경우에는 각 환경별로 네임스페이스를 만들어 관리하는 것이 좋다.

    - 즉, 네임스페이스가 다르면 같은 이름의 오브젝트를 만들 수 있어 매니페스트를 관리하기 용이해진다.

    - 네임스페이스에 배포된 서비스는 기본적으로 같은 네임스페이스의 파드에서 서비스의 이름만으로 접근할 수 있다.

    - 그리고 네임스페이스에 배포된 컨피그맵과 시크릿도 같은 네임스페이스의 파드에서 접근할 수 있다.

    - 그래서 네임스페이스별로 바뀌는 정보들은 네임스페이스에 보관하는 것이 좋다.



