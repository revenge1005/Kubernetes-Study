
# 1. ExternalName

+ 내부 파드가 외부 특정 FQDN에 쉽게 접근하기 위한 서비스 타입

+ K8s 클러스터 외부의 DNS 이름을 서비스 이름으로 등록함으로써 접속하기 위한 외부 FQDN 주소가 변경되더라도, 서비스 이름은 그대로 유지할 수 있어 애플리케이션을 다시 작성하거나 빌드하지 않아도 된다.

----

# 2. ExternalName 매니페스트 (svc-ext.yml)

```
kind: Service
apiVersion: v1
metadata:
  name: apl-on-baremetal
spec:
  type: ExternalName
  externalName: www.google.com
```

----

# 3. ExternalName으로 등록한 서비스 연결

```
### ExternalName 타입의 서비스 배포
$ kubectl apply -f svc-ext.yml
service/apl-on-baremetal configured


### 서비스 목록, EXTERNAL-IP 주목
$ kubectl get service apl-on-baremetal
NAME               TYPE           CLUSTER-IP   EXTERNAL-IP      PORT(S)   AGE
apl-on-baremetal   ExternalName   <none>       www.google.com   <none>    52s


### 서비스 이름으로 연결 테스트
$ kubectl run -it busybox --restart=Never --rm --image=busybox sh
If you don't see a command prompt, try pressing enter.
/ # ping apl-on-baremetal
PING apl-on-baremetal (142.251.42.132): 56 data bytes
64 bytes from 142.251.42.132: seq=0 ttl=127 time=135.800 ms
64 bytes from 142.251.42.132: seq=1 ttl=127 time=136.907 ms
64 bytes from 142.251.42.132: seq=2 ttl=127 time=135.334 ms
64 bytes from 142.251.42.132: seq=3 ttl=127 time=135.571 ms
^C
--- apl-on-baremetal ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 135.334/135.903/136.907 ms
```