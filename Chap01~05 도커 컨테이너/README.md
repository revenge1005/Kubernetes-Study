# 1. 도커 컨테이너 라이프 사이클


# 2. 도커 커맨드 치트 시트


### 2-1. 컨테이너 환경 표시
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 실행
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
docker version
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
도커 클라이언트와 서버 버전 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker info
</td>
<td>
구체적인 환경 정보 표시
</td>
</tr>
</table>


### 2-2. 컨테이너의 3대 기능

#### (1) 컨테이너 이미지 빌드
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 실행
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
docker build -t 리포지터리:태그 <br> docker image build -t 리포지터리:태그
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
현 디렉터리에 있는 Dockerfile을 바탕으로 이미지를 빌드
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker images <br> docker images ls 
</td>
<td>
로컬 이미지 목록
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker build -t 리포지터리:태그 <br> docker image build -t 리포지터리:태그
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
현 디렉터리에 있는 Dockerfile을 바탕으로 이미지를 빌드
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker rmi 이미지 <br> docker image rm 이미지
</td>
<td>
로컬 이미지 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker rmi -f \`docker images -aq` <br> docker image prune -a
</td>
<td>
로컬 이미지 일괄 삭제
</td>
</tr>
</table>

#### (2) 이미지의 이동과 공유
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 실행
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
docker pull 원격_리포지터리[:태그] <br> docker image pull 원격_리포지터리[:태그]
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
원격 리포지터리의 이미지를 다운로드
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker tag 이미지[:태그] 원격_리포지터리[:태그] <br> docker image tag 이미지[:태그] 원격_리포지터리[:태그]
</td>
<td>
로컬 이미지에 태그를 부여
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker login 레지스트리_서버_URL
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
레지스트리 서비스에 로그인
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker rmi 이미지 <br> docker image rm 이미지
</td>
<td>
로컬 이미지 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker save -o 파일명 이미지 <br> docker image load -i 파일명
</td>
<td>
이미지를 아카이브 형식 파일로 기록
</td>
</tr>
</table>

#### (3) 컨테이너 실행
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 실행
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
docker run --rm -it 이미지 커멘드 <br> docker container run --rm -it 이미지 커멘드
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
- 대화형 컨테이너를 기동해서 커맨드를 실행 <br> - 종료 시 컨테이너를 삭제 <br> - 커맨드에 bash를 지정하면 대화형 셸로 lunux 명령어 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker run -d -p 5000:80 이미지 <br> docker container run -d -p 5000:80 이미지
</td>
<td>
- 백그라운드로 컨테이너를 실행 <br> - 컨테이너 내 프로세스의 표준 출력/에러 출력은 로그에 보존 <br> - 보존된 로그의 출력은 'docker logs'를 참조 <br> - '-p'는 포트 포워딩으로 '호스트_포트:컨테이너_포트'로 지정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker run -d --name 컨테이너명 -p 8000:80 이미지 <br> docker container run -d --name 컨테이너명 -p 8000:80 이미지
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
컨테이너에 이름을 지정하여 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker run -v /html:/nginx/html -d -p 8080:80 nginx <br> docker container run -v /html:/nginx/html -d -p 8080:80 nginx
</td>
<td>
- 컨테이너의 파일 시스템에 디렉터리를 마운트하면 실행 <br> - '-v'는 '로컬_절대_경로:컨테이너_내_경로'
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker exec -it <컨테이너명 | 컨테이너_ID> sh <br> docker container exec -it <컨테이너명 | 컨테이너_ID> sh
</td>
<td>
실행 중인 컨테이너에 대해서 대화형셸을 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker ps -a <br> docker container ls -a
</td>
<td>
정지된 컨테이너도 포함하여 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker stop <컨테이너명 | 컨테이너_ID> <br> docker container stop <컨테이너명 | 컨테이너_ID>
</td>
<td>
컨테이너의 주 프로세스에 SIGTERM을 전송하여 종료 요청 <br> 타임 아웃 시 강제 종료 진행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker kill <컨테이너명 | 컨테이너_ID> <br> docker container kill <컨테이너명 | 컨테이너_ID>
</td>
<td>
컨테이너 강제 종료
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker rm <컨테이너명 | 컨테이너_ID> <br> docker container rm <컨테이너명 | 컨테이너_ID>
</td>
<td>
종료한 컨테이너를 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker rm `docker ps -a -q` <br> docker container rm `docker ps -a -q`
</td>
<td>
종료한 컨테이너 일괄 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker commit <컨테이너명 | 컨테이너_ID> 리포지터리:[태그] <br> docker container commit <컨테이너명 | 컨테이너_ID> <br> 리포지터리:[태그]
</td>
<td>
컨테이너를 이미지로서 리포지터리에 저장
</td>
</tr>
</table>

  
### 2-3. 디버그 관련 기능
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 실행
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
docker log <컨테이너명 | 컨테이너_ID>
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
컨테이너 로그를 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker logs -f <컨테이너명 | 컨테이너_ID>
</td>
<td>
컨테이너 로그를 실시간으로 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker ps -a <br> docker container ls -a
</td>
<td>
컨테이너 목록 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker exec -it <컨테이너명 | 컨테이너_ID> 커맨드 <br> docker container exec -it <컨테이너명 | 컨테이너_ID> 커맨드
</td>
<td>
실행 중인 컨테이너에 대해서 대화형으로 커맨드를 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker inspect <컨테이너명 | 컨테이너_ID> <br> docker container inspect <컨테이너명 | 컨테이너_ID>
</td>
<td>
상세한 컨테이너의 정보를 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker stats <br> docker container stats
</td>
<td>
컨테이너 실행 상태를 실시간으로 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker attach --sig-proxy=false <컨테이너명 | 컨테이너_ID> <br> docker container attach --sig-proxy=false <br> <컨테이너명 | 컨테이너_ID>
</td>
<td>
컨테이너 표준 출력 화면에 표시
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker pause <컨테이너명 | 컨테이너_ID> <br> docker container pause <컨테이너명 | 컨테이너_ID>
</td>
<td>
컨테이너 일시 정지 
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker unpause <컨테이너명 | 컨테이너_ID> <br> docker container unpause <컨테이너명 | 컨테이너_ID>
</td>
<td>
컨테이너 일시 정지 해제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker start -a <컨테이너명 | 컨테이너_ID> <br> docker container start -a <컨테이너명 | 컨테이너_ID>
</td>
<td>
정지된 컨테이너 실행 <br> 이때, 표준 출력/에러 출력을 터미널에 
</td>
</tr>
</table>
  
  
### 2-4. 쿠버네티스와 중복되는 기능

#### (1) 네트워크 관련
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 실행
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
docker network create 네트워크명
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
컨테이너 네트워크 작성
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker network ls
</td>
<td>
컨테이너 네트워크 목록 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker network rm 네트워크명
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
컨테이너 네트워크 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker network prune
</td>
<td>
미사용 컨테이너 네트워크 삭제
</td>
</tr>
</table>

#### (2) 퍼시스턴트 볼륨 관련
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 실행
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
docker volume create 볼륨명
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
퍼시스턴트 볼륨 작성
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker volume ls
</td>
<td>
퍼시스턴트 볼륨 목록 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker volume rm 볼륨
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
퍼시스턴트 볼륨 삭제
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker volume prune
</td>
<td>
미사용 퍼시스턴트 볼륨 삭제
</td>
</tr>
</table>

#### (3) docker compose 관련
<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 실행
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
docker-compose up -d
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker-compose.yml을 사용해서 복수의 컨테이너 기능
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker-compose ps
</td>
<td>
docker-compose 관리하에 실행 중인 컨테이너 목록 출력
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker-compose down
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
docke-compose 관리하의 컨테이너 정지
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
docker-compose down --rmi all
</td>
<td>
docker-compose 관리하의 컨테이너 정지와 이미지도 삭제
</td>
</tr>
</table>
