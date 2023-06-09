# Intro

## CRD

k8s 允许用户增加 CRD 以扩展k8s功能， CRD 除了用于k8s管理的通用部分， 其他都完全由用户定义，而对于 CRD 的CRUD会被 API server 写入 etcd，在这一阶段， CR 可以认为只是一份配置文件，用来描述用户期待的 CR， 随后在 k8s Reconcile loop 中, 会不断轮询 api server 以同步 CR 的状态，当 CR 状态变化时便会通知给对应的 Controller。Controller 中可获取用户所配置的 CR，然后就是按照预定义的逻辑，依据 CR 当前的状态触发不同的处理(CRUD)

对CR的处理完全是由用户决定的， 用户可以在其中引用 k8s 的内置资源， 将其与 CR 进行绑定， 也可以与自己设定的其他服务进行交互


## Build Operator

完成一个 Operator 需要使用到很多k8s相关的库，从原理上来说， Operator 只需要不停的与 Api Server 通信以进行状态同步/控制，就可以实现对CRD的管理

### client go

通过 `client go` 客户端可以直接与 k8s api server 进行交互， 对 k8s 中的定义的各种资源进行控制. 使用 `client go` 就能够完成 operator 的开发，然而依赖这种方式需要手动编写所有样板代码，相对复杂

### informer

`informer` 是 `client go` 中提供的一种 cache 机制， 开发者使用 `client go` 周期性地访问 api server 以同步最新的状态, 这种周期性的同步会加重 api server 的负担，并且当集群稳定时，这种轮询也显的多余，因此在 `client go` 种引入了 informer 机制

在 `informer` 中在首次运行时，会获取目标资源的所有对象，随后与 api server 建立长链接，监听目标资源种对象的变更事件， 并触发对应的回调

## Controller runtime

使用 `client go` 需要自己完成各个组件的启动与管理，其中多数代码都是可复用的。`controller runtime` 本身也是一个库，提供了对于 `client go` 在更高层的封装， 开发者不必手动去初始化各个组件，而是将配置交给 `controller runtime` 去处理。`controller runtime` 中提供了两个重要抽象

`controller`: 定义在 `pkg/internel/controller/contoller.go`中， 启动时以协程运行，主体是一个无限循环`#235`，读取事件队列并触发 `Reconcile` 函数

`manager`: 定义在 `pkg/manager/internal.go` 中， 所有的 controller 以及各种依赖组件都以 `Runnable`接口的形式注册到 `controllerManager` 的 `runnables` 字段中， 而在 manager 的 `Start` 函数中会调用这些 `Runnable` 接口， 来进行 controller 运行环境的初始化

## Kubebuilder

即便 `Controller runtime` 提供了更高层的抽象，但仍然需要用户去定义 CRD 配置文件， 编写 `manager` 与 `controller` 逻辑， 以及提供对应的配置文档等

`kubebuilder` 本身是一个二进制工具，提供了许多命令来生成脚手架，即样板代码，使得开发者只需要关注 CRD 中的关键字段以及 controller 中的 `Reconcile` 逻辑，其余都通过生成脚手架代码的形式来进行



[^1]: [controller_manager_工作原理](https://blog.yingchi.io/posts/2020/7/k8s-cm-informer.html)
[^2]: [client_go_informer](https://herbguo.gitbook.io/client-go/informer)
[^3]: [client_go_informer](https://cloudnative.to/blog/client-go-informer-source-code/#deltafifo) 
[^4]: [controller_runtime](https://maao.cloud/2021/02/26/Kubernetes-Controller%E5%BC%80%E5%8F%91%E5%88%A9%E5%99%A8-controller-runtime/)
[^5]: [operator](https://developers.redhat.com/articles/2021/06/22/kubernetes-operators-101-part-2-how-operators-work#the_kubernetes_architecture)
[^6]: [writing_controllers](https://vivilearns2code.github.io/k8s/2021/03/11/writing-controllers-for-kubernetes-custom-resources.html)
