# Kubelet 

- [kubelet源码阅读](https://guidao.github.io/kubelet.html)
- [pod 实现机制](https://www.infoq.cn/article/xyxNdh6OiooK75vo4ZiE)
- [pause 容器实验](https://www.cnblogs.com/lfl17718347843/p/14458085.html.)

## 一、简介

- kubelet 是在每个 Node 节点上运行的主要 “节点代理”
  - 它可以使用以下之一向 apiserver 注册： 主机名（hostname）；覆盖主机名的参数；某云驱动的特定逻辑。

- kubelet 是基于 PodSpec 来工作的
  - 每个 PodSpec 是一个描述 Pod 的 YAML 或 JSON 对象
  - kubelet 接受通过各种机制（主要是通过 apiserver）提供的一组 PodSpec，并确保这些 PodSpec 中描述的容器处于运行状态且运行状况良好
  - kubelet 不管理不是由 Kubernetes 创建的容器。

## 二、Pod实现机制

- Pod 是一个抽象概念，其对应于一组容器
  - Pod的职责在于提供一个隔离环境，其中所有的容器共享相同的存储、网络以及配置信息
  - 因而，Pod的实现也基于容器网络共享与容器存储共享两个目的

- 网络共享
  - Infra Container(Pause Container) 
    - Infra container 是一个非常小的镜像，大概 100~200KB 左右，由汇编语言编写，且永远处于"暂停"状态
    - 其他所有容器都会通过 Join Namespace 的方式加入到 Infra container 的 Network Namespace 中
  - Pod的ip地址即Infra container的 IP 地址，而其他所有网络资源，都是一个 Pod 一份，并且被 Pod 中的所有容器共享
  - 整个 Pod 中，Infra container 第一个启动，且整个 Pod 的生命周期等同于 Infra container 的生命周期，与其他容器无关
    - 因而在 Kubernetes 中允许去单独更新Pod中的某一个容器镜像，在这个操作中整个 Pod 不会重建，也不会重启
- 存储共享
  - 在 Pod 中实际上就是把 volume 变成了 Pod level，因此所有同属于一个 Pod 的容器，共享该 volume