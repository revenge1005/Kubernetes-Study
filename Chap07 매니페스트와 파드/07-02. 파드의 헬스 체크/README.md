
# 1. 헬스 체크 기능

+ 파드의 컨테이너에는 애플리케이션이 정상적으로 기동 중인지 확인하는 기능, 헬스 체크 기능을 설정할 수 있으며 이상이 감지되면 컨테이너를 강제 종료를 하고 재시작시킬 수 있다.

+ kubelet의 헬스 체크는 두 종료의 프로브를 사용하여 실행 중인 파드의 컨테이너를 검사한다.



### 활성 프로브 (Liveness Probe)

+ 컨테이너의 애플리케이션이 정상적으로 실행 중인 것을 검사한다.

+ 검사에 실패하면 파드상의 컨테이너를 강제로 종료하고 재시작한다.

+ 이 기능을 사용하기 위해서는 매니페스트에 명시적으로 설정해야 한다.



### 준비 상태 프로브 (Readiness Probe)

+ 컨테이너의 애플리케이션이 요청을 받을 준비가 되었는지 아닌지를 검사한다.

+ 검사에 실패하면 서비스에 의한 요청 트래픽 전송을 중지한다.

+ 파드가 기동하고 나서 준비가 될 때까지 요청이 전송되지 않기 위해 사용한다.

+ 이 기능을 사용하기 위해서는 매니페스트에 명시적으로 설정해야 한다.



# 2. 프로브 대응 핸들러의 종류

<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
핸들러 명칭
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
exec
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
컨테이너 내 커맨드를 실행 <br> Exit 코드 0으로 종료하면 진단 결과는 성공으로 간주
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
tcpSocket
</td>
<td>
지정한 TCP 포트번호로 연결할 수 있다면, 진단 결과는 성겅으로 간주
</td>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
httpGet
</td>
<td>
지정한 포트와 경로로 HTTP GET 요청이 정기적으로 실행 <br> HTTP 상태 코드가 200 이상, 400 미만이면 성공으로 간주 <br> 지정된 포트가 열려 있지 않은 경우도 실패로 간주
</td>
</tr>
</table>