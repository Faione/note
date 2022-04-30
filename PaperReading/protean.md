- [阅读记录](#阅读记录)
  - [Problem & Background](#problem--background)
    - [Workload Analysis](#workload-analysis)
  - [Challenges](#challenges)
  - [State-of-the-arts](#state-of-the-arts)
  - [Key insights/ideas/techniques](#key-insightsideastechniques)
    - [Rule-Based Allocation Agent](#rule-based-allocation-agent)
    - [Architecture](#architecture)
    - [Protean Implementation](#protean-implementation)
      - [Caching for Efficient Machine Selection](#caching-for-efficient-machine-selection)
      - [Conflict Detection and Reduction](#conflict-detection-and-reduction)
  - [Lessons learned from experiments](#lessons-learned-from-experiments)

## 阅读记录

- 题目
  - Protean: VM Allocation Service at Scale
- 作者
  - Ori Hadary
  - Microsoft Azure and Microsoft Research
- 会议
  - OSDI20


### Problem & Background


- 虚拟机分配器是云技术栈中的关键组件，次优的放置决策可能导致碎片化（反过来，不必要的物理资源过度配置）、性能影响和服务延迟，甚至拒绝传入请求和客户，导致分配失败。
  - Azure中，虚拟机是资源分配的主要单元，是客户能够利用Azure提供的丰富计算服务的手段

**The inventory**

- Azure
  - Regions
    - Zones(up to Three), typically heterogeneous inventory
      - DataCenter(one or more)
        - Cluster, homogeneous set of machines
          - Rack
            - Machine

**The Workload**

- 包含一个或多个VM的请求，被划分为一个 Tenant 组
  - 表达了VMs之间关系与对于这些VMs的限制
  - 一次分配只有当 Tenant 中所有VMs的请求都满足时才算成功

**Protean**

- Protean的主要作用是对于分配请求，基于底层服务模型中指定的明确要求和约束，以及其他内部操作考虑事项，为VM找到一个合适物理位置（物理机）


#### Workload Analysis


- 需求多样
  - VM 类型分布不同一，一些类型的VM占据多达50%的负载，其他类型的则占比较少
  - 大多数虚拟机需要少量的CPU核心，但有些则需要一半甚至整个服务器

- 后续请求类似
  - 选择某一类型的VM，后续请求超过80%仍然选择相同类型

- 虚拟机存续时间差异大
  - 大多数VM的寿命都很短，大约是几分钟。然而，一些虚拟机可以“永远”留在系统中——数周或几个月

- 需求呈峰值和日变化
  - 夜晚使用少
  - 请求能够达到每秒2000的峰值

- Tenant通常很小，但也可以非常大
  - 94% 1个VM
  - 99% 5个或5个以下VM
  - 极少的请求会包含上百个VMs

**总结**

- Scale and uncertainty
  - 必须考虑到极端的需求条件
  - 适应小的和大的区域，这需要灵活的配置

- Opportunity for caching 
  - 启发了对于位置评估逻辑的“缓存”，并在多个请求之间重用
    - 这个想法是设计的核心，并有助于扩展到大的区域和区域

- The packing challenge

### Challenges

- Azure的需求量达到每台数百万台虚拟机，因此满足如此高的请求频率，并快速响应和实现高的资源利用率，这对系统的设计与实现来说是一个挑战
  - 分配器需要管理一个充分大的资源，才能满足新用户的请求与已有用户的扩张请求
  - 但是，管理大规模的数据理所应当地会导致延迟

- 为提高系统的吞吐量，系统需要组合多个过程，这样并行化的分配逻辑，在维持高资源利用时同时又减小冲突，也是一个挑战

### State-of-the-arts

- 当前已有对应对这些挑战的技术，但是并没有在全球规模部署中的应用

### Key insights/ideas/techniques

> 一个 protean实例运行在一个大约1万到10万台虚拟机的可用区(zone)中
> 设计目标 鲁棒性、可扩展性、灵活性、优化的算法

#### Rule-Based Allocation Agent


**Allocation Rule**

- Protean中有两类分配规则
  - validator
    - 强约束
  - preference
    - 弱约束
- 集群与物理选择
  - 集群
    - validator
      - 过滤不符合VM请求的Cluster，如对于有GPU需求的VM，需要过滤没有GPU的集群
    - preference
      - 对合适的Cluster进行排序
        - 如偏好空的集群以平衡跨集群的可用容量
    - Protean基于上述规则，选择k个(可配置)cluster，一套物理选择规则基于这些集群中的物理机进行选择
  - 物理机
    - validator
      - 每个 validator rule 实现 IsValid(x, v) -> bool 方法，x可以是集群或物理机，v则是虚拟机，用来将备选object集合缩小为能够进行有效部署VM的子集
    - preference
      - prefrence规则量化了候选object对于VM的适合程度，$S_{r}(x, v)$ 计算评分(理解为距离，越近越好)，评分越低择越好
    - 对于物理机的选择同样有两类分配规则，对于最后得到的物理机集合，使用随机选择的方式从中用来创建VM

**Accounting for Multiple Rules**

- validate 规则序列可以依次进行过滤，但如何考虑多个preferejce规则对Protean的设计来说是一个挑战
  - 原则
    - compare method
      - 每个 preference 规则实现方法 Compare(x, y | v), 基于score进行比较，返回0(相同)，1(x < y, 即x更贴近)，-1(x > y)
    - 比较与排序
      - 每个 preference 规则都使用权重（或附加值）来表示其相对重要性
      - 两个 Object 基于每个规则的 compare method 的返回值与该rule的权重的乘积之和来进行比较
      - 使用两两比较，Protean根据总体偏好分数计算整个对象集的排序列表
        - 总体分数越大，说明 x比y 越适合，若此时存在一个z，其比y更适合，但值小于x，故可得排序 x 、z、y 
  - 权值设置
    - 尽管权值允许设置为任意的正值，但实际仍然采用了严格的设置方式以体现preference rule 之间的顺序
    - 规则根据一种保持顺序的编码来分配权重，不同规则之间的权值存在指数级别的差异，这使得任何规则都只能在权值比他更大的规则prefer的Object中体现自己的prefer，因此也可以视为是一个过滤的过程
  - 量化
    - 在偏好规则中有严格的优先级，需要“平滑”偏好规则，以便所有规则都能做出贡献

**Discussion**

#### Architecture

- Protean operation
  - 每台物理机上都运行一个进程，进程为每个AA创建线程
    - 每个 zone 中的AAs的数量根据zone中的瞬时峰值需求确定，而每台机器的AAs数量取决于每个AA的内存占用
  - 用户的请求通过负载均衡器路由到每个进程
    - 在进程中，请求存储在一个共享工作队列中，直到它们被空闲的AA接收和处理
  - 每个AA根据自己的库存视图做出分配决策，并在响应成功后，将结果提交到主从复制的存储中
  - 存储进行冲突检测，并序列化提交到相同的节点上，此外也存储被AA做出的VM部署决定所修改的库存信息
    - 存储作为最新位置相关库存状态的权威源，并通过发布-订阅（pub/sub）服务发布所有更改
  - 不受placement决策影响的库存中的变化，如机器健康状况或功能的变化，也会通过发布/订阅 服务发布。AAs主要通过 发布/订阅 服务产生的更新来了解库存的变化。此外，对于由于冲突导致的提交失败，他们将了解冲突机器的与最新位置相关的信息


- Service allocation workflow
  - 服务请求可以包含多个VM的请求，这些请求将被一个AA顺序处理
  - AA首先会将VM进行排序，为例减小请求被拒绝的风险
  - 之后，AA会启动一系列规则为VM分配物理机
  - 当AA为所有虚拟机分配好物理机之后，就会提交分配结果，如果任何VM的分配出现冲突，则提交失败，分配器状态将会回滚，请求也再次归队，并再次进行提交尝试(可配置)
    - 允许相对较高的重试次数（超过10次），以避免不必要的分配失败
    - 提交阶段与前面的阶段一起流水线化，因此AA在提交运行时可以自由地处理下一个请求

#### Protean Implementation

**Preliminaries**

- 为做出高质量的分配，初始情况下，AA将库存中的所有物理机作为候选
  - Cluster Selection
    - AA首先对集群进行过滤与排序
      - Zone中最多几百个集群，因此这个过程非常迅速(最多几毫秒)
    - 这个阶段的输出是最好的8到16个集群， 它们的机器(通常为10-15k)是物理机选择过程的候选对象
  - Machine selection
    - 通过一系列 validator 规则将候选集缩小为有效集
    - 再根据每台物理机托管虚拟机的适用性，构建一个基于比较的有效集中物理机的总排序
    - 最后，从一组最佳物理机中随机选择一个
    - 复杂度
      - $N\sum_{i=0}^{K_{1}} T_{v}(i) + N\log_{N}(\sum_{i=1}^{K_{2}}T_{p}(i))$
      - N: 候选物理机数量
      - $K_{1}$: validator rules 数量
      - $K_{2}$: preference rules 数量
      - $T_{v}(i)$: validator 算法 i 所用时间
      - $T_{p}(i)$: prefrence 算法 i 所用时间
    - AA每次都从请求开始进行计算，则开销很大
    - 如果AA试图为每个请求从头开始构建这个评估结果，那么它将超过几千台机器所需的延迟限制之和
  - Motivation for caching
    - 请求的局部性
      - 请求某VM之后，请求同类型VM概率非常大
    - 库存状态变化慢  
      - 在连续执行AA之间发生变化的机器主要是由于其他并行运行的AAs所作出的分配决策而导致其状态发生改变的机器
      - 这些特性将允许我们通过缓存和重用以前执行的评估“状态”来大幅减少在执行机器选择逻辑中执行的计算量

##### Caching for Efficient Machine Selection

**Caching Rule State**

- 缓存内部规则状态以实现高效执行
  - 使用缓存来提高每条规则的 IsValid 与 Compare method的执行速度
  - 每种 rule type 的实例化，称为 rule object，被缓存以供重用
  - 新创建的rule object在常数时间内计算并存储其用来执行IsValid或Compare Method所需的所有信息
    - 通常这些信息存储在每台机器上
- 规则状态的用时更新
  - 每当缓存的rule object被使用时，都需要在执行方法时将其内部的状态更新到最新
  - 每个规则都实现了 Update(x1,..., xm) 方法，用来更新其保存的状态，Update 在 rule被调用前启用
    - 参数(x1，...，xm)表示从上次更新对象时起已发生更改的机器的最新状态
  - 应用最新变化进行状态更新后，每条规则都在常量时间内执行IsValid与Compare Method方法
- 将规则的状态划分为多个对象
  - 考虑若请求需要类型1的VM，那么rule只需要知道该类型VM的容量，更新其他VM类型容量开销很大
  - 因此，不是为所有请求创建单个rule object(包含各种特征的信息，根据请求来switch)，而是根据需要为每种VM type创建一个规则对象（1对1），再将请求根据相关的特征值划分为不同等价类，单个规则对象可以处理属于一个VM type 的所有请求
    - 对于依赖于多个请求特征的规则，每个特征值的唯一组合都为该规则定义了一个新的请求等价类（该 rule object 包含了组合中的全部信息）
    - 对于规则不依赖于任何请求特征的特殊情况，所有请求都用一个规则对象
- rule object 缓存
  - rule object引用存储在一个固定大小的池中
    - 池的大小是根据内存占用和命中率考虑来确定的
  - rule object 由 rule type 与此object关联的特征值的组合来进行索引
  - 如果规则对象已满(遵循标准的LRU驱逐策略)，或者达到某个年龄，则从池中驱逐
    - 基于年龄的驱逐使我们能够在低负载期间减少内存占用

**Caching Rule Evaluation State**

- rule evaluation object 
  - 保存了对于特定特征值向量的评估状况
    - 包括评估结果(物理机排序序列)
    - 对相关rule object的引用，其特征值与整个特征值向量中的各自值相匹配
  - 完成对新的特征值向量的评估结果后，将创建一个rule evaluation object，该向量作为该对象的标识符。然后，该对象将被映射到此标识符的所有请求重用

- r e o 更新
  - 与 rule object 类似，reo在使用之前会进行状态的更新
    - 不同于 rule object， reo使用了一种通用的更新方法(ro是对于不同的type)，基于变化了的物理机对评估结果进行更新
      - 缓存的rule object使用UPDATE方法进行更新
      - 被修改的物理机从evaluation结果中被移出
      - validator rules 决定被移出的机器中那些是valid
      - valid物理机被重新插回到有序机物理机序列的新位置中
    - 插入的时间复杂度为 $\log N$, 总时间复杂度为 $M\log N$
      - M是被修改的机器数量
      - 由于 $M << N$, 因此能够大大降低时间复杂性
    - reo缓存在另一个恒定大小的内存池中，使用LRU驱逐策略

**Additional Cache Hierarchies**

- 多个rule经常依赖同一状态，因此可以将这个状态保存在 Shared-Cache中，并能够被多个rule访问到
- 一个缓存对象可能依赖于其他缓存对象，rule selection engine 会保证在rule 对象使用前，所有依赖项都会更新


**Efficiently Updating the Cache**

- 跟踪和更新机制
  - 为了方便无缝更新，每个AA都有一个日志，可以跟踪对库存中任何物理机的更改
    - journal包含一个全局的版本号，跟随每次更新而递增
    - 只保存为每台物理机保存最新的状态
    - 每个 缓存的对象 都保存它所见过的最高的版本号，对应与它的消耗所带来的库存的更新
    - 每个 缓存对象 通过读取最高版本的日志来进行更新
      - 因此，更新的复杂度取决于修改的物理机数量，而不是整个库存的大小
- 后台更新
  - 因此，当AA没有要处理的请求时，它会适时地更新缓存
    - 从reo开始，然后递归地进行


**discussion**

- Global rule
  - 将机器分解为单元格，每个单元格由一个机器子集组成，从所有全局规则的角度来看，它们被认为是相同的
  - 将复杂度从 $N\log N$ 缩小为 $N_{c} \log N_{c}$, 由于 $N_{c} << N$, 因此复杂性降低


##### Conflict Detection and Reduction

- 偶尔的请求峰值会使得AA全负载工作，这会使得因冲突增加而导致的提交失败几率增加

- 细粒度冲突检测
  - 设计一种冲突检测机制，允许AA基于旧的库存视图做出分配决策时的提交成功
    - 该逻辑验证新的放置决策不会过度提交机器资源或违反其他反托管约束
      - 如果满足，则合并新决策
- 降低分配之类来减少冲突
  - 由于AA分配逻辑类似，因此在高负载下，对于各自的请求，AA所选择的最适合的机器集合之间高度重合，由于集合规模小，因此即便使用随机选择的策略，也可能产生较高的冲突概率
    - 为此，AA在决策的最后阶段，使用混合的策略
      - 低负载时，从最合适的机器中进行选择
      - 高负载时，使用更宽松的冲突避免方案
        - 从 topn0的机器中随机选择一台机器，其中n0是一个可配置的参数

### Lessons learned from experiments

- 模拟实验中
  - 缓存命中/命中使用伯努利随机变量确定
  - 从生产中获得平均命中率(p=0.9)
  - 命中导致14ms延迟，而未命中导致更高的延迟88ms

- Cache延迟
  - 鉴于高命中率，每次分配的总体平均延迟接近 20 毫秒
  - 缓存未命中仍然使用许多较低的级缓存，因此延迟通常为 70-80 毫秒
- 内存
  - 通过回归得到的拟合线显示，内存增长是次线性的(∼x0.73)，这有助于保持内存大小在规模上的可管理性