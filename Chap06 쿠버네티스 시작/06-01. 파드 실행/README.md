
# 쿠버네티스 클러스터 구성 확인

```
$ kubectl get node -o wide

NAME         STATUS   ROLES                  AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
k8s-master   Ready    control-plane,master   28d   v1.22.3   192.168.219.10   <none>        Ubuntu 20.04.2 LTS   5.4.0-89-generic   docker://20.10.10
k8s-node01   Ready    <none>                 28d   v1.22.3   192.168.219.11   <none>        Ubuntu 20.04.2 LTS   5.4.0-89-generic   docker://20.10.10
k8s-node02   Ready    <none>                 28d   v1.22.3   192.168.219.12   <none>        Ubuntu 20.04.2 LTS   5.4.0-89-generic   docker://20.10.10
```

# 파드 실행

```
kubectl run hello-world --image=hello-world -it --restart=Never
```

<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
값
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
설명
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
kubectl
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
K8s 클러스터를 조작하기 위해 사용되는 커맨드
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
run 
</td>
<td>
컨테이너 실행을 명령하는 서브 커맨드
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
hello-world
</td>
<td>
쿠버네티스 오브젝트의 이름 (파드나 컨트롤러 등)
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
--image=hello-world
</td>
<td>
컨테이너의 이미지, 쿠버네티스에서는 파드 단위로 컨테이너가 기동되며 <br> 리포지터리명이 생략된 경우에는 도커 허브를 사용
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
-it
</td>
<td>
도커에서의 -it와 마찬가지로 -i는 키보드를 표준 입력으로 연결, -t는 터미널과 연결하여 대화 모드 설정. <br> 옵션 '--restart=Never'인 경우에만 유효하며, 그 외에는 백그라운드로 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
--restart=Never
</td>
<td>
이 옵션에 따라 파드의 기동 방법이 변경 <br> Never는 직접 파드가 기동되며, Always나 OnFailure는 컨트롤러를 통해 파드가 기동
</td>
</tr>
</table>

```
$  kubectl run hello-world --image=hello-world -it --restart=Never

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

# 파드 목록 확인
```
$ kubectl get pod

NAME          READY   STATUS      RESTARTS   AGE
hello-world   0/1     Completed   0          102s
```

# 종료한 파드를 지우고 재실행
```
$ kubectl delete pod hello-world
pod "hello-world" deleted

$  kubectl run hello-world --image=hello-world -it --restart=Never

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

# 파드 종료 후 자동으로 삭제하는 옵션 --rm 사용 예
```
kubectl run hello-world --image=hello-world -it --restart=Never --rm
```

