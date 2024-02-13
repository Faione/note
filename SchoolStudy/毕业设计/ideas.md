## Task Scheduling

### Shadow Thread(Link Thread)

Shadow Thread(Link Thread)
- 同一个 task 在SMT/CMP上的副本，拥有相同的调度状态(同时调度运行，同时调度退出)
- 用于在SMT/CMP之间共享调度状态，基于perCPU调度来模拟全局调度
- shadow thread性质类似于 idle，idle 也可以作为一种 shadow thread
- shadow thread本身不占用，或占用较少cpu, 主要作用为一种 barrier, 以限制/隔离 SMT/CMP 上的资源竞争
- shadow thread也可跨越机器，在分布式环境中模拟全局调度

shadow thread 的目标是提供一种调度对象的抽象，最大程度地复用当前成熟的调度器，向调度器传递更丰富的信息协助调度，而不是制造各种复杂的调度器

### delegated scheduling

delegated scheduling(委托调度)
- 允许n对1的调度委托，如CPU0将调度委托给CPU1，则CPU1同时维护 CPU0 与 CPU1 上的所有任务的调度
- 基于MuQSS
  - 用户指定，任意CPU可按委托关系构成一个CPU集合，调度此CPU集合中的任意一个task时，需要考虑整个集合的信息
  - 进程指定，可以指定委托`slibing`，`numa`, `socket`, 这将会根据进程存在于某个CPU上时，此CPU拓扑中按委托关系生成一个集合，并从此集合中决定进程的调度
- 基于ghOSt
  - 抽象调度信息为msg, 调度信息的传输通道为一个 msg 队列，符合生产者/消费者模型，且消息处理满足事务性
  - ghOSt原有设计已经能够做到delegated，可进一步要求虚拟机以mmap的形式将此队列只读地共享给宿主机，辅助宿主机进行调度决策

### Virutal Machine Async Scheduling 

虚拟化场景下的异步调度框架研究
- unikernel作为runtime
- 协调 unikernel 与 vcpu 的调度
- 以 core 为粒度的调控

## Resource Partition

### resource nice

一种基于多资源优先级的调控方法研究
- cpu/cache/mem b_w
- cpu nice 已经实现，cache/mem b_w 基于 RDT技术, 按可调节的 step 数量划分为百分比桶，根据nice值将task放入桶中，属于某个桶中的task获得的资源不会大于这个桶的上限
- 启动进程时可以为进程指定资源nice，也可以在进程运行过程中对于nice值进行修改
- 结合劣化监测手段实现精准的资源调控


面向节点侧QoS 运行时

基于标签化调度器的节点侧QoS保障研究
调度器创新
Qos保证策略
华为的工作，应用画像


## 开题报告

标签、节点侧解释
围绕一个点论述(相关性)
- 侧重于节点内调度
- 现有工作的问题 -> 课题优化目标
创新性
- 在线指标系统 -> 应用画像分析（增量：指标上的增量）
- 相关研究中的 典型案例分析 (前馈 - 反馈)