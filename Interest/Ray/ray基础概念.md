# Ray 基础概念

- [Ray相关论文](https://www.likecs.com/show-204452721.html)
- [Ray相关博客](https://www.cnblogs.com/fanzhidongyzby/p/7901139.html)
- [Ion Stoica riselab blog](https://rise.cs.berkeley.edu/blog/author/istoica/)
- [Ion Stoica anyscale blog](https://www.anyscale.com/blog?author=ion-stoica)
- [架构解读](https://xie.infoq.cn/article/d2073061a8c516ffa9dff7b81)
- [源码解析](https://bbs.huaweicloud.com/blogs/detail/247559)
- [Ray 1.0 Architecture whitepaper](https://docs.google.com/document/d/1lAy0Owi-vPz2jEqBSaHNQcy2IBSDEHyXNOQZlGuj93c/preview)
- [Ray Design Patterns](https://docs.google.com/document/d/167rnnDFIVRhHhK4mznEIemOtj63IOhtIPvSYaPgI4Fg/edit)
- [Ray 框架介绍](https://zhuanlan.zhihu.com/p/111340572)
- [Ray分布式框架详解](https://zhuanlan.zhihu.com/p/460600694)
- [Ray架构解析](https://zhuanlan.zhihu.com/p/357182462)
- [remote function解析](https://zhuanlan.zhihu.com/p/341217169)

## 一、初步认识

- 为什么使用ray框架
  - 提供了简单、通用的API来进行分布式应用的构造
  - 程序可以单机运行，也可以部署在集群上运行
- 高性能的实现
  - 并行计算
- 如何实现并行计算
- ray集群计算

- 简单认识
  - 高性能分布式执行框架，提供了简单、通用的API来进行分布式应用的构造
      - 为构建和运行分布式应用程序提供简单的原语
      - 使最终用户能够并行化单个机器代码，而代码更改几乎为零
      - 在核心 Ray 之上包括一个由应用程序、库和工具组成的大型生态系统，以支持复杂的应用程序
  - UC Berkeley RISELab
  - remote函数是Ray分布式计算抽象中的核心概念
    - 为开发者提供动态定制计算依赖的能力
      - 动态定制能够根据函数之间的调用关系生成Dag，无需提前设定Dag
- 系统框架

- 用户视角的ray功能
  - 方便的多进程创建(方法装饰器)
    - 进程创建的封装
  - 方便的进程通信
    - 利用共享内存(ObjectStore), 如单节点上的Redis数据库
    - master节点维护全局的Object Table, 以提供跨节点的进程通信

- object id
  - 如何获得 object id
- object table

## 二、ray核心api

## 三、ray集群架构

- Ray遵循了分布式系统典型的Master-Slave的设计：Master负责全局协调和状态维护，Slave执行分布式计算任务，但和传统的分布式计算系统不同，Ray使用了混合任务调度的思路
  - 混合任务调度

- GlobalScheduler
  - Master上启动了一个全局调度器，用于接收本地调度器提交的任务，并将任务分发给合适的本地任务调度器执行
- RedisServer
  - Master上启动了一到多个RedisServer用于保存分布式任务的状态信息（ControlState），包括对象机器的映射、任务描述、任务debug信息等
- LocalScheduler
  - 每个Slave上启动了一个本地调度器，用于提交任务到全局调度器，以及分配任务给当前机器的Worker进程
- Worker
  - 每个Slave上可以启动多个Worker进程执行分布式任务，并将计算结果存储到ObjectStore
- ObjectStore
  - 每个Slave上启动了一个ObjectStore存储只读数据对象，Worker可以通过共享内存的方式访问这些对象数据，这样可以有效地减少内存拷贝和对象序列化成本
    - ObjectStore底层由- Apache Arrow实现
- Plasma
  - 每个Slave上的ObjectStore都由一个名为Plasma的对象管理器进行管理，它可以在Worker访问本地ObjectStore上不存在的远程数据对象时，主动拉取其它Slave上的对象数据到当前机器。


## 四、Ray编程模型

