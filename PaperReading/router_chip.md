## 阅读记录

- 题目
  - Microarchitecture of a High-Radix Router
- 作者
  - John Kim
- 会议
  - IEEE

### Problem & Background

- 互联网络被广泛用于多处理器中的处理器与内存的连接
  - 网络的延迟和带宽在很大程度上建立了远程内存访问的延迟和带宽

- 大多数实现都是通过增加每个端口的带宽来增加芯片外的带宽，而不是增加芯片上的端口的数量。然而，随着芯片外带宽的持续增加，通过增加端口的数量来利用这个带宽——构建具有薄通道的高半径路由器——比通过构建具有肥通道的低半径路由器更有效

- 多数实现都通过增加单个端口的带宽来增加芯片外的带宽，而不是增加端口的数量
  - 随片外带宽的持续增加，通过构建薄而多的路由比肥而少的路由更有效

### Challenges



### State-of-the-arts

- 能扩展到high radix的分布式分配器微体系结构
- 使用中间缓存的方式，进行了high radix中的crossbar实现
- 使用分层交叉开关

#### Switch Allocation

#### Virtual Channel Allocation



### Key insights/ideas/techniques



### Lessons learned from experiments
