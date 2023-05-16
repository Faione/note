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
