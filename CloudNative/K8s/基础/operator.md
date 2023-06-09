# Operator

Operator是K8s的软件扩展，它利用自定义资源来管理应用程序及其组件。Operator同样遵循k8s的原则，尤其是控制循环

## Reconcile 


1. k8s支持那些资源?

通过命令 `kubectl api-resources` 可以查看当前系统中支持的所有资源类型， 通过 `kubectl create --help` 可以查看当前系统中可创建的所有资源类型， 通过命令 `kubect get crds` 可以查看当前系统中的所有crd

2. 一个基础类型（Pod/Service）是如何被创建的？

用户通过 `kubectl` apply 一个 pod yaml， 该请求首先被 api server 处理，其中会对 yaml 中的数据格式进行校验，验证无误后会将 pod yaml 存储到 etcd 中

与 api server 建立了长连接的 controller manager 会收到这一事件，并出发 pod controller 中的 event handler。在 handler 中， 首先会获取到 pod yaml，并进一步进行验证，如是否符合容器要求和限制，所需节点是否存在等，随后会分配IP地址给Pod，并按需求注入其他容器到yaml中。完成这些工作后得到了一个新的 pod yaml, controller 会将其同步到 etcd 中， 并将其状态设置为 `Pending`

Scheduler 会定期通过 api server 获得未被调度的 pod 列表, Scheduler 会找到符合pod调度需求的节点，并向 api server 提交一个绑定请求，将此pod绑定到选择的节点中

kubelet 与API server 保持连接并获取Pod清单，对于每个以被调度的 Pod ，kubelet 会按照 Pod 清单中的定义启动对应的容器，一旦容器启动完毕，kubelet 会向Api server 发送消息以修改 Pod 的状态为 `Running`。随后 kubelet 会持续探测容器的状态，如果容器出现了故障或者异常，则会将Pod的状态修改为 `Failed` 并尝试重新启动该 Pod

3. 一个复杂类型(Deployment)是如何被创建和维护的?

与pod的部署类似，deploy 部署时，除了PodController会追踪Pod状态外，还会有RelicaController追踪Pod的数量，以保证集群中有足够数量的pod

4. k8s中的 Reconcile 主循环是什么样的？

controller 协程启动后，会不断得从队列中目标资源对象的变化信息，并进行相应的操作

5. Reconcile循环的驱动因素是什么？

目标资源的变化

6. operator 是如何工作的？

与controller类似， 通过与 api server 连接来获取集群中目标资源的变化

7. operator/controller 是如何在Reconcile循环中作用的？

获取目标资源变化的事件，触发对应的回调

8. CRD 是如何被定义的？

CRD本身也是一种资源，类型为 `CustomResourceDefinition`， spec中会定义该资源spec字段中各数据的类型，说明与取值范围

9.  CRD yaml做了什么工作？

创建了一种 `CustomResourceDefinition`， 并在 api server 中进行扩展



