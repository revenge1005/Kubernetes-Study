# 1. Dockerfile 치트 시트

<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
커맨드 
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
FROM <이미지>[:태그]
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
컨테이너 베이스 이미지 지정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
RUN <커맨드> <br> RUN ["커맨드","파라미터1", "파라미터2"]
</td>
<td>
FROM의 베이스 이미지에서 커맨드 실행
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
ADD <호스트_파일_경로> <컨테이너_내_경로> <br> ADD ["호스트_파일_경로", ..."<컨테이너_내_경로>"]
</td>
<td>
소스(파일, 디렉토리, tar 파일, URL)를컨테이너 내 경로에 복사
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
COPY <호스트_파일_경로> <컨테이너_내_경로> <br> COPY ["호스트_파일_경로",.."<컨테이너_내_경로>"]
</td>
<td>
파일, 디렉토리를 컨테이너 내 경로에 복사
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
ENTRYPOINT ["실행하고_싶은_명령", "파라미터1", "파라미터2"] <br> ENTRYPOINT 실행하고_싶은_명령 파라미터1 파라미터2
</td>
<td>
컨테이너가 실행하는 파일을 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
CMD ["실행하고_싶은_명령", "파라미터1", "파라미터2"] <br> CMD 실행하고_싶은_명령 파라미터1 파라미터2
</td>
<td>
컨테이너 기동 시 실행될 커맨드를 지정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
ENV <key> <value> <br> ENV <key>=<value>
</td>
<td>
환경 변수 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
EXPOSE <port> [<port>...]
</td>
<td>
공개 포트 설정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
USER <유저명> | <UID>
</td>
<td>
RUN, CMD, ENTRYPOINT 실행 유저 지정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
VOLUME ["/path"]
</td>
<td>
공개 가능한 볼륨을 마운트
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
WORKDIR /path
</td>
<td>
RUN, CMD, ENTRYPOINT, COPY, ADD의 작업 디렉토리 지정
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
ARG <이름>[=<디폴트 값>]
</td>
<td>
빌드할 때 넘길 인자를 정의 <br> --build-arg <변수명>=<값>
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
LABEL <키>=<값> 
</td>
<td>
이미지의 메타데이터에 라벨을 추가
</td>
</tr>
</table>

# 2. Dockerfile 예제

### 1. 이미지에 포함시킬 파일들을 모을 디렉토리를 준비
```
mkdir test
cd test
```

### 2. Dockerfile 작성
```
cat <<EOF > Dockerfile
FROM alpine:latest
RUN apk update && apk add figlet
ADD ./message /message
CMD cat /message | figlet
EOF
```

### 3. 컨테이너에서 실행할 애플리케이션 코드 작성
```
echo "Hello World" > message
```

### 4. 이미지 빌드
```
docker build --tag hello:1.0 .
```

### 5. 결과 확인
```
docker run hello:1.0
```