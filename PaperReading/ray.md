## 阅读记录

- [阅读记录](#阅读记录)
  - [Problem & Background](#problem--background)
    - [Background](#background)
  - [Challenges](#challenges)
  - [State-of-the-arts](#state-of-the-arts)
  - [Key insights/ideas/techniques](#key-insightsideastechniques)
    - [Motivation](#motivation)
    - [Programming and Computation Model](#programming-and-computation-model)
    - [Architecture](#architecture)
      - [Application Layer](#application-layer)
      - [System Layer](#system-layer)
  - [Lessons learned from experiments](#lessons-learned-from-experiments)

- 题目
  - Ray: A Distributed Framework for Emerging AI Applications
- 作者
  - Philipp Moritz
- 会议
  - osdi18

### Problem & Background

#### Background

> 过去二十年中，许多组织收集并期望利用大量的数据，这促进了各式各样分布式数据分析框架的发展，如 batch、streaming、graph等数据处理系统，这些框架的成功使得组织进行大数据的分析成为可能，并引领了大数据时代

- 强化学习
  - 机器学习应用程序必须越来越多地在动态环境中运行，对环境的变化做出反应，并采取一系列行动，而不是只提供单一的预测
  - 强化学习就是用来处理在不确定环境中学习以能够持续操作的框架
  - 强化学习与传统有监督学习的差异
    - RL app 依赖模拟来探索可能的状态并得出行动的后果
      - 模拟器可以包含电子游戏的规则、牛顿力学、虚拟环境的混合动力学
    - RL app 的计算图是异构地(组成元素不同)，且在动态变化
    - 许多 RL app要求应对环境变化时的快速响应
    - 而为做出最佳的行动，RL app还可能需要实时地进行更多的模拟
  - 强化学习的系统要求
    - 总之，需要一个支持 异构 和 动态计算图 的计算框架，同时每秒处理数 百万 个具有 毫秒级 延迟的任务
    - 并且透明地容错

- 强化学习系统
  - 包含 environment、agent、state、action与reward
  - agent不断与environment交互，目的在与学习到一个 policy，使得一些 reward 最大
    - policy 是 state 到 action 的映射
      - 即输入一个状态，得到该进行的步骤，按照这种方式，可以驱动交互的不断进行
  - 学习过程
    - 典型的流程是
      - 评估当前的policy
      - 改进当前的policy
    - Rollout算法
      - 一种评估Policy的算法
      - 一次 Rollout 产生一组 rollouts
        - 一个rollout是对于 state 和 reward 的trajectory
          - 一次 trajectory 从状态机开始，到状态机结束，例如游戏从开始 -> 失败或者 开始 -> 成功
      - 使用所有的trajectory 来完成对Policy的更新


### Challenges



### State-of-the-arts

- 当前主要的集群计算框架，MapReduce、Spark等，无法同时支持RL应用所需的吞吐量和延迟
  - 使用中心化的调度器, 虽然能够简化设计,但是不利于伸缩性
- 而深度学习框架如TensorFlow，Naiad等通常假定计算图是静态的

### Key insights/ideas/techniques

- Ray 架构
  - 将所有控制状态存储在一个 global control state 中
    - 使得系统中的其他组件能够是无状态的，从而让这些组件能够进行横向扩展，且在出错时重新启动
    - global control state 可以通过分片来进行扩展，并通过复制来实现容错能力
  - 引入了一个 bottom-up distributed scheduler
    - 计算任务被worker与drivers提交到本地的调度器(每个节点上有一个)
    - 本地调度器可以调度任务到本地执行，或者将任务提交给全局调度器的副本
      - 允许本地决策能够降低任务的延迟，并通过减少全局调度器的负担来提升系统的吞吐量

#### Motivation

**RL APP的需求**

- 灵活性
  - 并发执行任务的异构性
    - 功能
      - 如机器人中，包含多种传感器，要求同时允许这些任务，并且每个任务使用不同的计算方法
    - 周期
      - 计算trajectory的时间变化明显
        - 如游戏中，几步就可能导致失败，但成功可能需要上百步
    - 源类型
      - 大多数计算使用深度学习模型，因此需要GPU，而其时间里，多数计算都由CPU完成
  - 执行图的通用性和动态性
    - Rollouts的计算完成，与Policy的更新无法预测，因此计算的执行图并非是静态地
- 性能
- 开发友好
  - 简化开发过程至关重要
    - 确定性重放和容错性
      - 确定性重放简化了debug过程 
      - 透明容错无需用户显式处理故障
      - 允许用户使用廉价的可抢占资源，降低成本
  - 对已有算法轻松地并行化
    - 对语言的支持
    - 对三方库的支持

#### Programming and Computation Model

**Programing Model**

- Remote Function
  - 无状态且无副作用，输出仅由输入决定
  - 意味着幂等性，能够在故障时重新执行函数来简化容错
  - 灵活性、性能、开发与友好
    - 提供 `ray.wait()`, `ray.get()` 方法，用来进行并发控制
    - 允许用户声明资源需求，从而使得Ray调度器能够充分管理资源
      - 为 remote function 声明的资源，仅在方法执行时分配
    - 允许嵌套的 remote function
    - 提供 actor 抽象
      - 一个 Actor 是一个有状态的进程，暴漏一组可作为remote function 调用的方法，并串行地执行

**Computation Model**
 
- Dynamic task graph computation model
  - 当remote function 与 actor method的输入可用时，系统会自动触发并执行 
- 计算图
  - Node
    - data objects、task
  - Edge
    - data edges, control edges(task之间), stateful edge(actor，捕获调用顺序)
      - 引入 stateful edge
        - 方便将Actor嵌入无状态的计算图中
        - 维持数据谱系，方便重建丢失的数据


#### Architecture

##### Application Layer

- Driver
  - 执行用户程序的进程
- Worker
  - 无状态进程，执行driver或其他worker调用的task
  - 自动启动，并由系统层分配task
  - 当一个 remote function 被声明时，该function自动发布给所有的worker
  - worker中的 task 串行执行
- Actor
  - 有状态的进程，执行被调用的其暴漏的方法
  - 不同与worker，actor被一个worker或driver显示的实例化
  - actor中的 method 串行执行

##### System Layer

> 性能与容错目标

**Global Control Store**

- 存储系统中最新的 元数据 与 控制状态
  - 每个 task 的说明
  - 每个 remote function 的代码
  - 计算图
  - 所有 object 的当前位置
  - 任何调度事件
- GCS同时还提供 pub-sub 基础设施, 用来进行组件之间的通信
- 通过集中的方式进行控制状态的存储和控制, 使得其他组件无状态化
- 使用分片的方式进行GCS的扩展
  - 关联伪随机ID与GCS中实际的每个数据条目, 在多个分片上进行负载均衡相对容器
  - 为每个分片提供热副本, 从而实现容错

**Bottom-Up Distributed Scheduler**

- 提升调度器可扩展性的方式
  - 批调度
    - 调度器想worker以批的粒度提交task, 从而能够均摊固定开销
  - 分层调度
    - 全局的调度器将任务图划分给每个局部调度器
  - 并行调度
    - 多个全局调度器在全部节点上同时进行task调度
  - 对于 Ray 来说都不可行

- 自底向上的分布式调度
  - 与分层调度类似, 存在一个 global scheduler 以及在每个节点上的 local scheduler
- 具体流程
  - 节点上创建的 task 首先被提交到 local scheduler, 而不是 global scheduler
  - local scheduler 本地调度task, 除非
    - 节点过载
      - 为了确定负载，本地调度程序将检查其任务队列的当前长度, 如果长度超过了某个可配置的阈值，则认为节点过载
      - 可配置的阈值使得 scheduler 从中心化变得分布式
    - 无法满足 task 的需求
    - task 的输入为 remote
  - 当 local scheduler 无法进行 task 调度时, 就会将 task 提交给 global task
  - 每个 local scheduler 发送带有负载信息的周期性心跳给GCS
    - GCS 保存这些信息, 并转发给 global scheduler
    - 在接收到一个任务后，全局调度器使用来自每个节点的最新的加载信息以及任务输入的位置和大小(来自GCS的对象元数据)来决定将任务分配给哪个节点
  - 如果 global scheduler 出现瓶颈, 则可以实例化多个副本, 让 local scheduler 随机选择一个进行 task 的提交
 

### Lessons learned from experiments