----

> # 15-01 kubectl 커맨드의 네임스페이스 설정

+ kubectl을 사용할 때 네임스페이스를 지정하려면 **"-n <네임스페이스명>"**을 사용한다.

+ 이러한 옵션을 지정하지 않고 kubectl의 기본으로 사용하는 네임스페이스를 바꾸려면 **"kubectl config"**를 사용하면 된다.

+ 그러면 여러 개의 k8s 클러스터 중에서 조작할 클러스터와 그 네임스페스를 지정할 수 있다.

|커맨드|설명|
|------|---|
|kubectl get namespce|네임스페이스 목록 출력|
|kubectl config view|config 파일에 등록된 정보 출력|
|kubectl config get-contexts|Context 목록 출력|
|kubectl config set-context|Context 설정|
|kubectl config set-context \<Context명\> --namespace=\<네임스페이스명\> <br> --cluster=\<클러스터명\> --user=\<유저명\> |K8s 클러스터명, 네임스페이스, 유저를 조합하여 Context 작성|
|kubectl config current-context|현재 사용 중인 Context 표시|

<br>

----

> # 15-02 조작할 k8s 클러스터와 네임스페이스를 교체

+ kubectl config는 마스터에 대한 접근 정보를 기반으로 하며, kubectl이 마스터에 대한 정보를 얻는 방법은 다음과 같다.

    - ① 실행 시 옵션으로 지정 '-kubeconfig <config_파일_경로>'

    - ② 홈 디렉토리 밑의 '.kube/config' 참조

    - ③ 환경 변수 KUBECONFIG에 지정된 경로 참조

----

## (1) 실습 환경

![01](https://user-images.githubusercontent.com/42735894/145680011-3b6d9cd3-7c22-4f07-9246-375b1d0b98c9.PNG)

----

## (2) k8s 클러스터 컨텍스트 변경과 kubectl을 통한 multi-cluster 접속


