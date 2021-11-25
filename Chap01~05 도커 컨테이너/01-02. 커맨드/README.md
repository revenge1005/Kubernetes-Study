# 1. 도커 커맨드 예제

## (1) 이미지 다운로드 (docker pull)

```
<pre><code>
$ docker pull centos:7
7: Pulling from library/centos
2d473b07cdd5: Pull complete 
Digest: sha256:9d4bcbbb213dfd745b58be38b13b996ebb5ac315fe75711bd618426a630e0987 
Status: Downloaded newer image for centos:7

$ docker images 
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    feb5d9fea6a5   2 months ago   13.3kB 
centos        7         eeb6ee3f44bd   2 months ago   204MB 
```

## (2) 컨테이너 실행 (docker run)

<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
옵션
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
-i
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
키보드 입력을 테이너의 표준 입력에 연결
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
-t
</td>
<td>
터미널을 통해 대화형 조작이 가능
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
-d
</td>
<td>
컨테이너 백그라운드 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
--name
</td>
<td>
컨테이너 이름 지정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
--rm
</td>
<td>
컨테이너가 종료하면 종료 상태의 컨테이너를 자동 삭제
</td>
</tr>
</table>

```
docker run -it --name test1 centos:7 bash
[root@af2b73b6a56d /]#
```

## (3) 컨테이너 상태 출력 (docker ps)

```
$ docker ps -a
CONTAINER ID   IMAGE                COMMAND    CREATED          STATUS                        PORTS     NAMES
af2b73b6a56d   centos:7             "bash"     5 minutes ago    Exited (127) 11 seconds ago             test1
3c2b66396b8a   hello-world:latest   "/hello"   29 minutes ago   Exited (0) 29 minutes ago               eloquent_haibt
```

## (4) 로그 출력 (docker logs)

컨테이너 실행중 발생한 표준 출력/에러 출력을 간직하고 있다.

"-f" 옵션을 사용하면 컨테이너가 실행 중인 상태에서 실시간으로 발생하는 로그를 불 수 있다.

```
$  docker ps -a
CONTAINER ID   IMAGE                COMMAND    CREATED          STATUS                        PORTS     NAMES
af2b73b6a56d   centos:7             "bash"     6 minutes ago    Exited (127) 50 seconds ago             test1
3c2b66396b8a   hello-world:latest   "/hello"   29 minutes ago   Exited (0) 29 minutes ago               eloquent_haibt

$ docker logs 3c2b66396b8a

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

## (5) 컨테이너 정지 (docker stop, docker kill)

### 실행 중인 컨테이너 정지 조건

### A. 컨테이너의 PID=1인 프로세스가 종료
```
# 커맨드 지정하지 않고 실행하여 컨테이너가 바로 종료되는 예 (기동하자마자 PID=1인 셸이 종료했기 때문)
$ docker run ubuntu
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
7b1a6ab2e44d: Pull complete
Digest: sha256:626ffe58f6e7566e00254b638eb7e0f3b11d4da9675088f4781a50ae288f3322
Status: Downloaded newer image for ubuntu:latest

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$  docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED         STATUS                     PORTS     NAMES
48e88ef72359   ubuntu    "bash"    8 seconds ago   Exited (0) 7 seconds ago             reverent_euclid
```
```
# 프로세스 종료에 의한 컨테이너 정지
# PID 값이 1인 bash가 기동되었음을 ps 명령어를 통해 확인 후 exit를 입력해 컨테이너를 종료 
$  docker run -it --name tom ubuntu bash

root@ff141a33bd2f:/# ps -ax
    PID TTY      STAT   TIME COMMAND
      1 pts/0    Ss     0:00 bash
     10 pts/0    R+     0:00 ps -ax

root@ff141a33bd2f:/# exit
exit

$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS                     PORTS     NAMES
ff141a33bd2f   ubuntu    "bash"    13 seconds ago   Exited (0) 3 seconds ago             tom
```

### B. 'docker stop <컨테이너명 | 컨테이너_ID>' 실행
```
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS          PORTS     NAMES
7b629ac52a20   ubuntu    "bash"    32 seconds ago   Up 32 seconds             tom

$ docker stop tom
tom

$ docker run -it --name tom ubuntu bash
root@7b629ac52a20:/# exit
$ 
```

### C. 'docker kill <컨테이너명 | 컨테이너_ID>' 실행
```
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS          PORTS     NAMES
7b629ac52a20   ubuntu    "bash"    32 seconds ago   Up 32 seconds             tom

$ docker kill tom
tom

$ docker run -it --name tom ubuntu bash
root@7b629ac52a20:/# exit
$ 
```

## (6) 컨테이너 재기동 (docker start)

```
docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS                     PORTS     NAMES
ef68a87d5131   ubuntu    "bash"    13 seconds ago   Exited (0) 6 seconds ago             tom

root@docker-vm:~# docker start -i tom

docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED              STATUS          PORTS     NAMES
ef68a87d5131   ubuntu    "bash"    About a minute ago   Up 48 seconds             tom
```

## (7) 컨테이너 변경 사항을 리포지터리에 저장 (docker commit)

```
$ yum -y update
Loaded plugins: fastestmirror, ovl
Determining fastest mirrors
 * base: mirror.navercorp.com
 * extras: mirror.navercorp.com
 * updates: mirror.navercorp.com
base                                                                         | 3.6 kB  00:00:00
<생략>

$ yum -y install git
Loaded plugins: fastestmirror, ovl
Loading mirror speeds from cached hostfile
 * base: mirror.navercorp.com
 * extras: mirror.navercorp.com
 * updates: mirror.navercorp.com
Resolving Dependencies
--> Running transaction check
<생략>

$ docker ps -a
CONTAINER ID   IMAGE      COMMAND   CREATED         STATUS                      PORTS     NAMES
09edfe96d324   centos:7   "bash"    2 minutes ago   Exited (0) 16 seconds ago             focused_noyce

$ docker commit 09edfe96d324 centos:7-git
sha256:ef597332e745288fadb96ca3f694d775d0256d9252944bdec734ce41e9d50ad5

$ docker images
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
centos        7-git     ef597332e745   3 seconds ago   532MB
centos        7         eeb6ee3f44bd   2 months ago    204MB
```

## (8) 이미지를 원격 리포지터리에 보관 (docker push)

### 1. 도커 허브에 로그인 (docker login)
```
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: shchoi94
Password:
Login Succeeded
```

### 2. 로컬 리포지터리에 원격 리포지터리의 이름과 태그 부여
```
$ docker tag centos:7-git shchoi94/centos:7-git
root@docker-vm:~# docker images
REPOSITORY        TAG       IMAGE ID       CREATED         SIZE
centos            7-git     ef597332e745   6 minutes ago   532MB
shchoi94/centos   7-git     ef597332e745   6 minutes ago   532MB
centos            7         eeb6ee3f44bd   2 months ago    204MB
```

### 3. 도커 허브 리포지토리에 등록
```
$ docker push shchoi94/centos:7-git
The push refers to repository [docker.io/shchoi94/centos]
d0d04bb698f3: Pushed
174f56854903: Layer already exists
```
