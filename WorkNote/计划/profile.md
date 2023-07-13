项目名称(职位) 时间
项目描述:
主要工作:
项目难点:
个人收获:


## 项目经历


2021.04-09      基于nats消息总线的RPC

nats消息中间件提供了 request 和 reponse 方法, 用以提供基础的 rpc 功能, 但为每个 rpc 请求设置一个 topic 非常浪费 nats server 端资源, 因此我选择为每个通信端点设置一个 uuid 作为 topic, 同时仿照Http设置一个基本的RPC协议, 通信端点基于 topic 进行消息发送/接收, 上层协议进行处理并将请求按照路由设置分发给各个 handle 函数, 这样能够大大减少系统中的 topic 数量并充分利用 go 语言的多线程处理能力

2021.09-12      集群控制代理

项目需要远程对docker, k8s集群进行操作, 同时要求插入中间逻辑来满足业务定制. 为避免对外部软件的依赖, 我选择对 docker / k8s / helm client 进行进一步封装来初步实现控制功能, 并在上层包装一层 Service 层来实现各个业务, 之后通过一个 Route 层来提供灵活的服务暴露方式, 能够根据需要设置 RPC / Http 等多样的方式, 也可以通过其他web框架插入各种中间件来进一步拓展功能

2022.01-05      k8s全栈监控

项目要求对k8s中业务进行全栈监控, 考虑业界需求, 将具体监控目标分为 metric, log, trace 三类, 在 metric 上, 我选用 Prometheus 高可用监控栈, 针对 k8s 场景启用 Node Exporter, Kube State Metric来进行节点级\Pod级别的数据采集, 而在 log 上, 选用性能较高的 Vector 来进行日志转发, 在数据后台搭建 ElasticSearch 来管理日志, 并通过 Kibana 进行可视化. 在 trace 上, 业内尚未有较完善的方案, 对于插装应用, 选用 Jaeger Operator 进行 trace 数据的采集与分析, 而对于常规应用, 则选择 Cilium Service Mesh 系统来实现无侵入的网络观测

2022.06-09      集群网络管理

项目中需要在南京/北京两地内网进行跨内网的通信, 消息中间件能够解决数据传输的问题, 但无法处理服务访问. 我选择在开源的反向代理工具Frp的基础上开发Frp Operator, 在集群中增加 FrpService 资源来表示一个公网可访问的 Frp Server, 以及 ServiceProxy 用来表示期望进行反向代理的服务, 使得只需要对这两种资源进行配置, 就可以动态地创建/修改所需要反向代理的服务, 以方便进行管理

项目中需要对不同用户的业务进行网络上的隔离, 而在K8s中默认不会对网络访问进行限制, 但允许通过定义 Network Policy 进行实现, Cilium 提供了一个网络策略控制器, 我在其基础上进一步封装, 通过若干条网络策略, 实现了不同 namespace 之间的访问隔离, 同时允许用户在同一 namespace 下定义个多个不同的 groupLabel 以进一步进行网络的分组划分

2022.10-12      Exporter拓展

业务中有定制采集指标的需求, 我基于Prometheus Client 封装了 EasyExporter 框架, 提供同步与异步两种采集方案, 前者在每次Prometheus采集时才触发, 后者则会以协程的形式运行, 采集模式类似于Push Gateway, 基于此框架我开发了ServerExporter, 能够采集服务器硬件信息\端口统计\登陆用户统计\容器统计\ssh记录统计等信息

而为解决Cilium自带的Metric信息不足的问题, 我开发了CiliumExporter, 通过hubble提供的gRpc接口查询相关Flow数据, 并将转化对应的指标信息提供给Prometheus, 并在通过后续对于flow metric的处理, 生成对应的服务拓扑并保存

2023.01-03      项目CI/CD

由于项目人员扩张, 需要CI/CD来强化项目管理, 我在开发集群中搭建了 Gitlab 并编写了相关代码编译/测试/部署脚本, 过程中为解决 Gitlab 与 Gitee 仓库的同步问题, 通过添加 Drone 作为第三方应用, 在两者之间进行代码的同步, 并触发对应的CICD流程, 同时搭建 Harbor 作为内部镜像仓库, 以加快构建部署速度




## 项目经历

1. 测调系统课题项目

测调系统服务于信息高铁，提供监控数据采集、远程控制等服务，底层基于kubernetes。

我在测调系统项目中负责边端代理agent的相关工作。主要工作分为三部分，为解决以容器为粒度的服务全场景监控，参考业内常用Prometheus监控系统，选用面向k8s的Prometheus Stack实现容器性能指标监控。其次在日志采集上选用主流ElasticSearch作为日志分析核心，而在边端上采用Vector作为容器日志采集组建。考虑到k8s中部署的服务多以微服务的形式存在，单单点监控很难反映出整体服务状态，因此采用基于cilium作为QOS网络监控组建，对微服务进行拓扑描述，并监控实施的QOS。

采用开源项目能够解决大部分场景下的监控目标，而对于项目中一些特殊需求，我独立开发了 Server Exporter 来解决服务器基础详细的采集问题，并能够通过auth记录监控当前系统的中的出入情况。同时，为解决cilium自带metric指标不够详细，hubble ui本身很难与其他开源项目交互的问题，开发了 Cilium Exporter, 通过gRPC直接与hubble进行交互，并能够完全自定义指标形式，以满足对TCP/HTTP链接更细致的信息如API,延迟等采集。并且为了将传统性能监控工具与云原生进行结合，独立开发了 Perf Exporter, 通过管道文件桥接perf输出，并将其转化为 Prometheus Metric 从而与 Prometheus生态进行结合，提供更丰富的监控手段

边端代理除监控功能以外，还需要对网络proxy以便于对边端服务进行访问与调试，同时还集成了kubernetes sdk, docker sdk以便直接对k8s或者docker进行远程控制。而为解决跨局域网访问的问题，项目中采用nats解决网络通信问题，我则基于nats的C-S模式进一步封装上层RPC框架，使得边端代理的所有服务即能够在局域网内通过http服务暴露，也可以通过部署在公网中的nats server, 为所有nats client访问

2. 开源操作系统训练营

训练营致力提供基于risc-v和rust语言的系统开发教学，我参与了2023年春季的开源操作系统训练营，并完成了第一阶段中的所有任务

TODO: 100 syscall

3. 开源社区项目

TODO: 解决使用rust编写的容器运行时youki对于Podman的适配

4. 应用QOS分析项目

TODO: 受到cilium的启发，基于ebpf技术开发面向云的内核信息采集系统

4. 基于k8s的ebpf程序部署

TODO: 

5. 开源之夏

TODO: 
