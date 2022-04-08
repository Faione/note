# k8s 搭建

- [k8s 搭建](#k8s-搭建)
  - [一、启动集群](#一启动集群)
    - [(1) minikube启动](#1-minikube启动)
    - [(2) 查看集群信息](#2-查看集群信息)
  - [二、部署应用](#二部署应用)
  - [三、查看 pod 和工作节点](#三查看-pod-和工作节点)
    - [四、暴露Service](#四暴露service)
    - [五、运行应用的多个实例](#五运行应用的多个实例)
    - [六、应用更新](#六应用更新)
    - [七、配置Java微服务](#七配置java微服务)
    - [问题与理解](#问题与理解)
  - [理解](#理解)
  - [问题汇总](#问题汇总)

- [kubectl](https://kubernetes.io/zh/docs/tasks/tools/install-kubectl-linux/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubevirt](https://kubevirt.io/)

## 一、启动集群

- Master 负责管理整个集群
  - Master 协调集群中的所有活动，例如调度应用、维护应用的所需状态、应用扩容以及推出新的更新。

- Node 是一个虚拟机或者物理机
  - 它在 Kubernetes 集群中充当工作机器的角色 每个Node都有 Kubelet , 它管理 Node 而且是 Node 与 Master 通信的代理。 Node 还应该具有用于​​处理容器操作的工具，例如 Docker 或 rkt 。处理生产级流量的 Kubernetes 集群至少应具有三个 Node 。

- Master 管理集群，Node 用于托管正在运行的应用。
  - 在 Kubernetes 上部署应用时，您告诉 Master 启动应用容器。 Master 就编排容器在集群的 Node 上运行。 Node 使用 Master 暴露的 Kubernetes API 与 Master 通信。终端用户也可以使用 Kubernetes API 与集群交互
- 通过 k8s 或者 minikube启动一个k8s集群
  - Minikube 是一种轻量级的 Kubernetes 实现，可在本地计算机上创建 VM 并部署仅包含一个节点的简单集群
  - Minikube 会创建一个虚拟机，并根据配置在虚拟机中安装docker应用以及其他核心容器
    - 因而 image-mirror 指的是 minikube 虚拟机的镜像

### (1) minikube启动

```shell
# 下载二进制文件
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# 安装
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 赋予当前用户docker权限(minikube不推荐使用root启动)
$ sudo usermod -aG docker $USER && newgrp docker
```

- minikube启动成功后，会为当前用户创建 .kube 配置文件


```shell
# --image-mirror-country='cn' 自动选择国内的minikube镜像(配置打包在镜像中，而不是通过此命令配置仓库)
# --image-repository='registry.cn-hangzhou.aliyuncs.com/google_containers' 配置内部docker的默认拉取仓库
# --driver='docker' 默认会选择docker driver
# $ minikube start --driver='docker' --image-mirror-country='cn' --image-repository='registry.cn-hangzhou.aliyuncs.com/google_containers'

# minikube start --image-mirror-country='cn' --insecure-registry=152.136.134.100:10048  设置虚拟机中的docker使用私有库
$ minikube start --image-mirror-country='cn'

# 停止, 不会改变minikube镜像(minikube中的配置不变)
$ minikube stop

# 删除, 此时会删除集群及镜像, 重新启动则会再拉去新的minikube镜像
$ minikube delete
```

### (2) 查看集群信息

```shell
# 下载kubectl二进制包
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# 安装kubectl
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

```shell
# 查看所有nodes
$ kubectl get nodes

# 查看单个node信息
$ kubectl describe node <node_name>
```

## 二、部署应用

- Deployment 指挥 Kubernetes 如何创建和更新应用程序的实例。创建 Deployment 后，Kubernetes master 将应用程序实例调度到集群中的各个节点上。
- 创建应用程序实例后，Kubernetes Deployment 控制器会持续监视这些实例。 如果托管实例的节点关闭或被删除，则 Deployment 控制器会将该实例替换为群集中另一个节点上的实例。 这提供了一种自我修复机制来解决机器故障维护问题

```shell
# hhitzhl/kubernetes-bootcamp:v1, 404容器拉取不到，更换镜像即可
$ kubectl create deployment kubernetes-bootcamp --image=hhitzhl/kubernetes-bootcamp:v1
```

## 三、查看 pod 和工作节点

- Pod 是 Kubernetes 抽象出来的，表示一组一个或多个应用程序容器（如 Docker），以及这些容器的一些共享资源。这些资源包括:
  - 共享存储，当作卷
  - 网络，作为唯一的集群 IP 地址
  - 有关每个容器如何运行的信息，例如容器映像版本或要使用的特定端口

- Pod 为特定于应用程序的“逻辑主机”建模，并且可以包含相对紧耦合的不同应用容器。例如，Pod 可能既包含带有 Node.js 应用的容器，也包含另一个不同的容器，用于提供 Node.js 网络服务器要发布的数据。Pod 中的容器共享 IP 地址和端口，始终位于同一位置并且共同调度，并在同一工作节点上的共享上下文中运行。
- Pod是 Kubernetes 平台上的原子单元。 当我们在 Kubernetes 上创建 Deployment 时，该 Deployment 会在其中创建包含容器的 Pod （而不是直接创建容器）。每个 Pod 都与调度它的工作节点绑定，并保持在那里直到终止（根据重启策略）或删除。 如果工作节点发生故障，则会在群集中的其他可用工作节点上调度相同的 Pod

- Node 是 Kubernetes 中的参与计算的机器，可以是虚拟机或物理计算机，具体取决于集群。每个工作节点由主节点管理
  - 工作节点可以有多个 pod ，Kubernetes 主节点会自动处理在群集中的工作节点上调度 pod
  - 主节点的自动调度考量了每个工作节点上的可用资源
- 每个 Kubernetes 工作节点至少运行:
  - Kubelet，负责 Kubernetes 主节点和工作节点之间通信的过程; 它管理 Pod 和机器上运行的容器。
  - 容器运行时（如 Docker）负责从仓库中提取容器镜像，解压缩容器以及运行应用程序

```shell
# 查看 pods
$ kubectl get pods

# 查看详情
$ kubectl describe pods

# 查看log
$ kubectl logs <podname>

# pod执行命令
kubectl exec -it <podname> -- bash
```

### 四、暴露Service

- Kubernetes 的 Service 是一个抽象层，它定义了一组 Pod 的逻辑集，并为这些 Pod 支持外部流量暴露、负载平衡和服务发现
- Service 允许您的应用程序接收流量。Service 也可以用在 ServiceSpec 标记type的方式暴露
  - ClusterIP (默认)
    - 在集群的内部 IP 上公开 Service 。这种类型使得 Service 只能从集群内访问。
  - NodePort
    - 使用 NAT 在集群中每个选定 Node 的相同端口上公开 Service 。使用<NodeIP>:<NodePort> 从集群外部访问 Service。是 ClusterIP 的超集。
  - LoadBalancer
    - 在当前云中创建一个外部负载均衡器(如果支持的话)，并为 Service 分配一个固定的外部IP。是 NodePort 的超集。
  - ExternalName
    - 通过返回带有该名称的 CNAME 记录，使用任意名称(由 spec 中的externalName指定)公开 Service。不使用代理。这种类型需要kube-dns的v1.7或更高版本

- NodePort模式，集群外部能够通过任意NodeIP + Port的模式访问到服务(能够访问Node)
  - 即指能够在宿主机上，通过minikube ip 的方式访问到服务
- ClusterIP 模式，则只能在集群内部访问
  - 即只能在minikube虚拟机中，宿主机无法通过集群ip访问服务(kubectl 控制与访问服务在网络的使用上有所区别)

```shell
# deployment/kubernetes-bootcamp 与 deployment kubernetes-bootcamp 效果等同
$ kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080

# 查看服务信息
# $ kubectl get service/kubernetes-bootcamp
$ kubectl get service kubernetes-bootcamp

# minikube ip 获得 k8s集群ip, Node Port 为分配给Service的port
$ curl $(minikube ip):$NODE_PORT
```

### 五、运行应用的多个实例

扩缩 是通过改变 Deployment 中的副本数量来实现的
- 同时，由于 serive 暴露 pods 的集合，因而还存在负载均衡

查看 ReplicaSet 

```shell
$ kubectl get rs
```

扩容应用实例

```shell
$ kubectl scale deployments/kubernetes-bootcamp --replicas=4
```

查看应用，能够发现相关Pods变为4

```shell
# -o wide 显示更多的数据
$ kubectl get pods -o wide
```

### 六、应用更新

更新应用程序
用户希望应用程序始终可用，而开发人员则需要每天多次部署它们的新版本。在 Kubernetes 中，这些是通过滚动更新（Rolling Updates）完成的。 滚动更新 允许通过使用新的实例逐步更新 Pod 实例，零停机进行 Deployment 更新。新的 Pod 将在具有可用资源的节点上进行调度。

在前面的模块中，我们将应用程序扩展为运行多个实例。这是在不影响应用程序可用性的情况下执行更新的要求。默认情况下，更新期间不可用的 pod 的最大值和可以创建的新 pod 数都是 1。这两个选项都可以配置为（pod）数字或百分比。 在 Kubernetes 中，更新是经过版本控制的，任何 Deployment 更新都可以恢复到以前的（稳定）版本


```shell
# 通过改变 deployment 的镜像来进行升级
$ kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
```

回滚版本

```shell
$ kubectl rollout undo deployments/kubernetes-bootcamp
```

### 七、配置Java微服务

### 问题与理解

## 理解

kubectl -> 集群的 control panel
  - 依赖 .kube 中的配置

k8s集群 -> Node -> Service -> Pod -> Container

NodeIP: 理解为主机的IP(集群内/外均可访问)
PodIP: 理解为一组container集合的ip(集群内/Node内可访问)
ClusterIP: 理解为一组Pods的ip(抽象的ServiceIp, 集群内可访问，但必须指定端口)
## 问题汇总

1. 谷歌源无法访问
   - 替换aliyun源

```
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
```

2. minikube无法启动
   - minikube不允许使用root账户启动
     - 使用非root用户启动
   - minikube docker 驱动
     - 启动minikube的用户，必须在docker用户组中
   - 谁启动的了minikube，谁使用kubectl进行操作(root也不例外)
     - 这是因为minikube为创建它的用户设置kube config(~/.kube中)与密钥, 其中包括了minikube集群的控制入口，因而只有此用户能够使用kubectl控制minikube集群
       - 如果该用户使用 kubectl proxy, 则其他用户也可以使用 RESTful api 来向minikube集群发送控制命令
       - minikube kubectl 仍然是从当前主机发送命令，只不过集成在minikube中
         - kubectl后面增加 "--" 使得flag被kubectl识别而不是minikube

