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

> 一个 protean实例运行在一个大约1万到10万台虚拟机的可用区中
> 设计目标 鲁棒性、可扩展性、灵活性、优化的算法

#### Rule-Based Allocation Agent




### Lessons learned from experiments