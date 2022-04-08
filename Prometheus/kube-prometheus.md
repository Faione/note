# Kube Prometheus

- [kube prometheus](https://github.com/prometheus-operator/kube-prometheus)

## 部署

**Minikube**

```shell
# 部署可监控的k8s集群
$ minikube start --kubernetes-version=v1.23.0 --memory=6g --bootstrapper=kubeadm --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook --extra-config=scheduler.bind-address=0.0.0.0 --extra-config=controller-manager.bind-address=0.0.0.0 --image-mirror-country='cn' --image-repository='registry.cn-hangzhou.aliyuncs.com/google_containers'  --insecure-registry=152.136.134.100:10048
```
clone 项目

```shell
# 安装组件
$ kubectl apply --server-side -f manifests/setup
$ kubectl apply -f manifests/
```

- 问题
  - 无法拉取 "k8s.gcr.io/kube-state-metrics/kube-state-metrics:v1.9.8" 镜像
  - 解决
    - 从 dockerhub 拉取镜像 "bitnami/kube-state-metrics:1.9.8"
    - `docker tag bitnami/kube-state-metrics:1.9.8 k8s.gcr.io/kube-state-metrics/kube-state-metrics:v1.9.8`

## 使用

- 使用 k8s port-forward 将服务通过本机端口进行暴漏

**Prometheus**

```shell
# --address=0.0.0.0, 指定所有地址，否则默认 localhost 访问
$ kubectl --namespace monitoring port-forward --address=0.0.0.0 svc/prometheus-k8s 9090
```

**Grafana**

- grafana 默认账户: admin, 默认密码: admin

```shell
$ kubectl --namespace monitoring port-forward --address=0.0.0.0 svc/grafana 3000
```

**AlertManager**


```shell
$ kubectl --namespace monitoring port-forward --address=0.0.0.0 svc/alertmanager-main 9093
```
