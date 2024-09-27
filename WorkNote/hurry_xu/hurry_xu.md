## Semantics
- 系统对于应用不可见，提供通用的功能
- 应用程序、Runtime、编译器、内核 做一个协同设计，传递语义

## 数据中心的资源浪费
- 负载的潮汐效应 -> 混合部署
- 资源分配的碎片化 -> 动态调度

MapReduce(Google) -> Cloud 

## 数据中心资源利用
![](./img/image-1.png)

## 应用的多样需求
- ![](./img/image.png)

## 服务器资源有限，调度的处理困难，容易造成资源分配的碎片化
- ![](./img/image-2.png)
- ![](./img/image-3.png)
- ![](./img/image-4.png)

>GPU分配率40%、50%（区别不同部门）

## 硬件解耦合，不是单纯的通用芯片的划分，而注重片上资源的分配
- CPU Server上的硬件设计时注重CPU
- Memory Server上硬件的设计注重MMU
- 系统软件的设计不拘泥现状，而能够通过参数实现足够通用的系统软件栈

## 资源解耦合的数据中心
- 从Storage开始（Hadoop、HDFS） -> Memory -> Compute
- Challenge：解耦合CPU与Memory
- ![](./img/image-6.png)

> binpacking -> 碎片化问题

## 远程访问开销（软件、硬件）
- ![](./img/image-7.png)
- ![](./img/image-8.png)

## 硬件开销、软件开销
- ![](./img/image-10.png)
- ![](./img/image-12.png)

## 总是存在通信的开销
- ![](./img/image-13.png)

## 现状，remote access占比过多
- ![](./img/image-14.png)

## 在此背景下还能进行的工作，减少每次访存的开销，并同时减少访存的次数
- ![](./img/image-15.png)

> 语义：GC做指针内存访问

## 丰富的语义
- ![](./img/image-16.png)
- CIS：将一个APP中的task放到不同特性的Server上运行
- APS：Prefetch
- 程序员知道应用中不同部分的资源使用，需要让操作系统也知道这些语义，并针对性地调度

## 寻找应用中的不同语义
- ![](./img/image-17.png)
- ![](./img/image-18.png)

![](./img/image-19.png)

## 程序语言中的manage runtime（go runtime）
- ![](./img/image-20.png)
- 程序员无法控制这部分的内容（不同与C语言中的内存控制）

## 引发的问题
- ![gc问题](./img/image-23.png)
- gc需要查看堆数据，但在分离式系统中，堆内存并不一定在本地
- ![gc的弱局部性](./img/image-24.png)
- 局部性越低，访问remote/非cache越多
- ![gc带来的资源竞争](./img/image-25.png)

## 解决方式
- ![](./img/image-26.png)
- Memliner将APP与GC对内存的访问放在一起
- Mako将GC放到Memory Server上

## Memliner
- ![](./img/image-27.png)
- 拉近APP与GC对于内存的访问，从而减少访问远程内存的次数
- 如何拉近：修改次序（无法改变APP，但是可以修改GC的次序）

## Memliner图示
- ![](./img/image-28.png)
- 合并访问

## Memliner实现
- ![](./img/image-29.png)
- ![](./img/image-30.png)
- ![](./img/image-31.png)
- ![](./img/image-32.png)

## Memliner Evaluation
- ![](./img/image-33.png)

## Mako
- ![](./img/image-34.png)
- 让GC放到Memory Server上，引发一致性问题
- ![](./img/image-35.png)
- ![](./img/image-36.png)
- Global Heap，不同段放到不同的机器上
- HIT Server处理同步问题（作为锁）

## Mako效果
- ![](./img/image-37.png)

## Memory Disaggregation
- ![](./img/image-38.png)
- ![](./img/image-39.png)

> DSM 时 DSC（Compute）的前提，DSM中的同步开销太大

## 存在的问题
- 分布式系统中，软件实现一致性，开销太大
- ![](./img/image-41.png)
- 问题在于，不清楚APP在做什么，而是期望提供通用的逻辑

## 核心观点
- ![](./img/image-44.png)

## 挑战
- ![](./img/image-45.png)

## DRust
- DRust(Distrubuted Rust)
- ![](./img/image-46.png)
- ![](./img/image-47.png)

## DRust实现
- ![](./img/image-48.png)
- Global Heap
- ![](./img/image-49.png)
- DRust调度Rust程序的不同部分到分离式系统中
  - 库的替换（Link过程DRust）
  - DRust Runtime

## DRust过程
- ![](./img/image-50.png)
- ![](./img/image-51.png)
- ![](./img/image-52.png)
- ![](./img/image-53.png)
  - 借用 mut reference 时，在Global Heap上替换一个新地址
  - 由于地址替换，因此owner不必通知所有Cache失效，只是读写的时候，发现地址变换
  - 存在地址翻译的开销 -> 论文中有很多优化技巧
![](./img/image-54.png)

## DRust示例
- ![](./img/image-55.png)
- Local Cache中存在RC，并进行GC
- ![](./img/image-57.png)

## 实验结果
- ![](./img/image-58.png)
- 线性的Scalability
- ![](./img/image-59.png)
- ![](./img/image-60.png)

## Talk
- 快速有效地构建分布式系统
  1. 先有需求 -> 构建系统
  2. 提供基础 -> 将已有的转化为分布式

### DRust实现
- OpenSource，Rust+C
- [](https://github.com/uclasystem/DRust)
- 只用到了ownership
- Rack Scale
- DevOps工作（Logging、Charging）

### System Fundation
- Resource Pool
  - H：是一个重要概念
  - X：What is Pool？
  - H：类似于Set的数据结构，但有更多的细节
  - H：Set是Dynamic Scale，Pool存在一个upper bound
  - X：是否是一个iterator
  - H：iterator与Set紧密结合，Pool Size存在Bound，有就使用，没有则是否
- Management Runtime
  - X：必须存在？
  - H：必须存在
  - W：微软发现Rust没有Runtime，所以存在较大的Fragmentation

### 代码、库、Supporting Env获取信息并利用
- X：使用语义解决上述问题，能否将非Pool的内容转化为Pool
- H：通过语义扩大池化，通过编译器池化。池化与Bound需要结合再一起，不能随意的New，需要存在回收

Programming Language
- Monaca？