
# 1. 매니페스트 적용

```
$ tree k8s-rbac/
k8s-rbac/
├── namespace.yml
├── role-base-access-ctl.yml
└── service-account.yml

0 directories, 3 files
 
$ kubectl apply -f k8s-rbac/
namespace/tkr-system created
clusterrole.rbac.authorization.k8s.io/nodes created
clusterrolebinding.rbac.authorization.k8s.io/nodes created
serviceaccount/high-availability created
```

### > GKE로 실행 할 경우, 다음 명령어를 통해 롤 작성 권한을 GCP의 유저에게 부여해야 한다.

```
### 여기서 USER_ACCOUNT는 유저의 메일 주소를 입력
kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user USER_ACCOUNT
```