# 1. Dockerfile 치트 시트


### 2-1. 컨테이너 환경 표시
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

</td>
</tr>
</table>

