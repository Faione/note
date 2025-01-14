## 十、软件定义网络与网络功能虚拟化


### 1 SDN

#### 1.1 定义

- 数据面（data plane）与控制面（control plane）物理分离的网络
- 由（逻辑上）集中的控制面控制多个转发设备（如交换机）

##### (1) 网络的三个平面

- 数据面（Data Plane）：按照转发与处理规则，执行数据包处理与转发的平面，包括
  - 转发决策：根据规则与数据包头，形成转发与处理决策
  - 数据包处理：过滤、缓存、调度
- 控制面（control plane）：计算转发与处理规则
  - 转发规则计算：数据包如何转发与处理
  - 实现：路由、流量工程、失效检测/恢复等
- 管理面（ Management plane）：配置网络
  - 如通过设置路径权重，影响规则的计算，从而实现流量工程

#### 1.2 意义

##### (1) 传统网络弊端

- 缺乏模块化，大量任务定制化的控制机制
- 只能间接控制
  - 比如：改变权重才能改变路径，而不是直接改路径
- 缺乏统一协调的控制
  - 由于分布式路由，不能控制哪个路由器先更新

##### (2) OpentFlow

##### (3) P4

### 2. NFV

#### 2.1 定义

- NF：Network Function，网络功能
  - 防火墙、NAT、WAF等
- Virtualization：虚拟化
  - 一个物理实体虚拟为多个虚拟实体（类似台式机上的虚拟机）
  - 多个物理实体虚拟为一个虚拟实体（资源整合）
- 虚拟化也是云计算的核心技术之一

#### 2.2 小结

- 网络中存在大量的中间盒子（middlebox） 
- NFV：传统每个功能对应一个盒子->虚拟化多个功能放在一个物理盒子
- SDN与NFV天然互补，结合
- NFV由于虚拟化等特性带来性能、隔离性等挑战
- NFV在5G网络中可能有较大的作用
