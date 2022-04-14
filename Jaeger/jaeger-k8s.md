- [k8s](https://github.com/jaegertracing/jaeger-operator)


## 集群准备

- 启动配置
  - `--addons=ingress`

```shell
$ minikube start --kubernetes-version=v1.23.0 --memory=6g --bootstrapper=kubeadm --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook --extra-config=scheduler.bind-address=0.0.0.0 --extra-config=controller-manager.bind-address=0.0.0.0 --image-mirror-country='cn' --image-repository='registry.cn-hangzhou.aliyuncs.com/google_containers'  --insecure-registry=152.136.134.100:10048 --addons=ingress
```

- cert-manager
  - 提前下载配置文件

```shell
$ kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.6.3/cert-manager.yaml
```

## 安装 Jaeger Operator

- 提前下载配置文件
  - 如需要变更命名空间，需要对 yaml 文件中的 `observability` 进行替换

```shell
$ kubectl create namespace observability
$ kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.33.0/jaeger-operator.yaml -n observability
```

- 问题
  - 镜像 `gcr.io/kubebuilder/kube-rbac-proxy:v0.8.0` 无法拉取
  - 解决
    - 使用镜像 `docker pull xiaopp123/kubebuilder.kube-rbac-proxy:v0.8.0` 替代
    - 重新tag `docker tag xiaopp123/kubebuilder.kube-rbac-proxy:v0.8.0 gcr.io/kubebuilder/kube-rbac-proxy:v0.8.0`

