# Kube Prometheus

- [kube prometheus](https://github.com/prometheus-operator/kube-prometheus)

- [serviceMonitor](https://stackoverflow.com/questions/68085831/add-podmonitor-or-servicemonitor-outside-of-kube-prometheus-stack-helm-values)

## 部署

**Minikube**

```shell
#! /bin/bash

K8S_VERSION=v1.23.0

NODEs=4
# per node
CPUs=4
MEMORY=6g

# for gluenet
INSECURE_REGISTRY=39.101.140.145:10048


minikube start \
--kubernetes-version=$K8S_VERSION \
--cpus=$CPUs \
--memory=$MEMORY \
--nodes $NODEs \
--bootstrapper=kubeadm \
--image-mirror-country='cn' \
--insecure-registry=$INSECURE_REGISTRY \
```


- 不允许master调度

```shell
$ kubectl taint node k8s-master node-role.kubernetes.io/master="":NoSchedule
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

```shell
$ docker pull 152.136.134.100:10048/kube-state-metrics:1.9.8

$ docker tag 152.136.134.100:10048/kube-state-metrics:1.9.8 k8s.gcr.io/kube-state-metrics/kube-state-metrics:v1.9.8
```

```shell
$ docker pull v5cn/prometheus-adapter:v0.9.1

$ docker tag v5cn/prometheus-adapter:v0.9.1 k8s.gcr.io/prometheus-adapter/prometheus-adapter:v0.9.1
```
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


## NameSpace删除

- [apiservice失败导致apiserver卡死](https://cloud.tencent.com/developer/article/1802531)

## 调研

- kube-prometheus组件
  - The Prometheus Operator
  - Highly available Prometheus
  - Highly available Alertmanager
  - Prometheus node-exporter
  - Prometheus Adapter for Kubernetes Metrics APIs
  - kube-state-metrics
  - Grafana

- 修改 Prometheus 镜像，使其默认发送数据到agent
  - manager 通过数据的发送者来区分集群，分开数据的存储
  - agent负责启动 kube-prometheus
  - agent之间传递 jaeger collector 配置
