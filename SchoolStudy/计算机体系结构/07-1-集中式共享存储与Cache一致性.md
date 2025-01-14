# 集中式共享存储与Cache一致性

- [集中式共享存储与Cache一致性](#集中式共享存储与cache一致性)
  - [一、多处理器体系结构](#一多处理器体系结构)
    - [(1) 体系结构选择](#1-体系结构选择)
    - [(2) 存储器结构模型](#2-存储器结构模型)
    - [(3) 通信模式](#3-通信模式)
    - [(4) 基于共享存储的MIMD计算机](#4-基于共享存储的mimd计算机)
    - [(5) 并行处理面临的挑战](#5-并行处理面临的挑战)
  - [二、Cache一致性问题](#二cache一致性问题)
    - [(1) 产生不一致的原因](#1-产生不一致的原因)
    - [(2) Cache 写机制](#2-cache-写机制)
  - [三、Cache一致性协议](#三cache一致性协议)
    - [(1) Snoopy & Directory](#1-snoopy--directory)
    - [(2) 基于监听的两种协议](#2-基于监听的两种协议)
  - [四、基于监听的Cache一致性协议](#四基于监听的cache一致性协议)
    - [(1) Valid/Invalid协议](#1-validinvalid协议)
    - [(2) MSI(Modified/Shared/Invalid)协议](#2-msimodifiedsharedinvalid协议)
  - [五、一致性面临的问题](#五一致性面临的问题)
    - [(1) 一致性和假共享](#1-一致性和假共享)
    - [(2) 一致性与同步](#2-一致性与同步)
    - [(3) 一致性和总线占用率](#3-一致性和总线占用率)

## 一、多处理器体系结构

### (1) 体系结构选择

- 按照Flynn分类法，可以将计算机分成
  - 单指令流单数据流（SISD）
  - 单指令流多数据流（SIMD） 
  - 多指令流单数据流（MISD）
  - 多指令流多数据流（MIMD）
- MIMD已成为多处理器体系结构的选择
  - MIMD灵活性高
  - MIMD可以充分利用商品化微处理器在性价比方面的优势

### (2) 存储器结构模型

- 共享存储(多处理器)
  - 物理上分离的多个存储器可作为一个逻辑上共享的存储空间进行编址
- 非共享存储(多计算机)
  - 整个地址空间由多个独立的地址空间构成，它们在逻辑上也是独立的，远程的处理器不能对其直接寻址 
  - 每一个处理器-存储器模块实际上是一个**单独的计算机**，这种机器也称为多计算机

### (3) 通信模式

- 共享存储通信
  - 单地址空间
  - 通过Load/Store指令的地址进行隐式通信
    - 数据
    - 控制信号: semaphores、locks、barriers
  - 编程模型: 多线程
- 消息传递通信
  - 地址空间分离
  - 通过send/receive进行显式通信
    - 数据
    - 控制信号: blocking msgs、barriers
  - 编程模型: 进程 + 进程间通信(eg: MPI)

**特点**

- 共享存储通信
  - 当处理器通信方式复杂或程序执行动态变化时易于编程，同时在简化编译器设计方面也占有优势
  - 通信数据量较小时，通信开销较低，带宽利用较好
  - 通过硬件控制的Cache减少了远程通信的频度，减少了通信延迟以及对共享数据的访问冲突
- 消息传递通信
  - 硬件较简单
  - 通信是显式的，从而引起编程者和编译程序的注意，着重处理开销大的通信

### (4) 基于共享存储的MIMD计算机

- 依据多处理器系统中存储器组织以及处理器个数的多少
  - 集中式共享存储器结构(SMP)
    - 也被称为UMA（uniform memory access）机器、对称式共享存储器结构
  - 分布式共享存储器结构(DSM)
    - 也可被称为NUMA（non-uniform memory access）机器
    - 每个结点包含：处理器、存储器、I/O及互连网络接口
    - 需要高带宽的互连
- 在许多情况下，分布式存储器结构优于采用集中式共享存储器结构

### (5) 并行处理面临的挑战

**阿姆达尔定律**

- 加速比
  - $Speedup =  \frac {time_{without-enhancement}} {time_{with-enhancement}}$
- 假定优化能够以加速比 S 加速本身占比 f 的部分
  - $time_{new} = time_{old} \times ((1-f) + \frac{f}{S})$
  - $S_{overall} = \frac{time_{old}}{time_{new}} = \frac{1}{(1-f) + \frac{f}{S}}$

- 对于并行处理而言
  - $理论加速比 = 并行核心数量$
  - $可加速部分 = 并行执行部分, 不可加速部分 = 串行执行部分$
  - 根据阿姆达尔定律可得到加速比为
    - $\frac{1}{(1-并行比例) + \frac{并行比例}{理论加速比}}$

**挑战与问题**

- 有限的并行性使机器要达到好的加速比十分困难
  - 解决方式: 通过采用并行性更好的算法来解决
- 多处理器中远程访问的较大延迟
  -  解决方式: 寻求更佳的体系结构和编程技术
- 存储器访问的次序问题
  - 存储一致性(Consistency)
    - 不同处理器发出的所有存储器操作的顺序问题
    - 所有存储器访问的全序问题
  - Cache一致性(Coherence)
    - 不同处理器访问相同存储单元时的访问顺序问题
    - 访问每隔Cache块的局部序问题
  - 解决方式: 一致性协议

## 二、Cache一致性问题

### (1) 产生不一致的原因

- I/O操作
  - Cache中的内容可能与由I/O子系统输入输出形成的存储器对应部分的内容不同
- 共享数据
  - 不同处理器的Cache都保存有对应存储单元的内容
  - 如何保持同一数据单元在Cache及主存中的多个备份的一致性，避免获取陈旧数据

**存储一致性定义**

- 如果对某个数据项的任何读操作均可得到其最新写入的值， 则认为这个存储系统是一致的（非正式定义）
- 如果存储系统行为满足条件
  - 处理器P对X写，在没有其他处理器写X时，读取的X为P写入的值
  - 对同一单元的写时顺序化的，即任意两个处理器对同一单元的两次写，对所有处理器来看顺序都相同


### (2) Cache 写机制

- Write-back：写回模式
  - 更新cache时，并不同步更新memory，只是在数据被替换出cache时，被修改的数据才更新到内存中
- Write-through：写直达模式
  - CPU向cache写入数据时，同时向内存写一份，使得cache和memory的数据保持一致
- Write-miss：写失效
  - 当所要写的数据的地址不在cache中
  - no write allocate policy
    - 将要写的内容直接写回memory
  - write allocate policy
    - 将要写的地址所在的块先从main memory(主存)调入cache中，然后写cache

## 三、Cache一致性协议

- 关键在于对于数据块状态的更新
- 主要协议
  - Snooping-based protocols（基于监听的协议）
    - 每个Cache除了包含物理存储器中块的数据拷贝之外，也保存着各个块的共享状态信息
  - Directory-based protocols（基于目录的协议）
  - 物理存储器中共享数据块的状态及相关信息均被保存在一个称为目录的地方

### (1) Snoopy & Directory

**Snoopy**

- 通过广播维护一致性
  - 写数的处理器把新写的值或所需的存储行地址广播出去
  - 其他处理器监听广播，当广播中的内容与自己有关时，接受新值或提供数据
  - 协议
    - Write Invalidate：写作废协议，使备份无效
    - Write Update：写更新协议，更新备份值
- 适合多个处理器通过总线相连的集中式共享存储系统
- 可扩展性有限
- 总线是一种独占性资源，延迟随处理器数目的增加而增加

**Directory**

- 为每一存储行维持一目录项，记录所有当前持有此行备份的处理器号以及此行是否已经被改写等信息
- 当某个处理器改写某行时，根据目录内容只向持有此行备份的处理器发送信号，避免了广播
- 适合采用通用互连网络连接的分布式系统

### (2) 基于监听的两种协议

- Write Invalidate(写作废)
  - 在一个处理器写某个数据项之前保证它对该数据项有唯一的访问权
  - 当一个处理器更新某共享单元（如存储行或存储页）时（之前或之后）
    - 通过某种机制使该共享单元的其它备份作废无效
    - 当其它处理器访问该共享单元时，访问失效，再取得该单元的新值
- Write Update(写更新)
  - 当一个处理器更新某共享单元时，把更新的内容传播给所有拥有该共享单元备份的处理器
  
**性能差别**

- 对同一个数据（字）的多个写操作且中间无读操作
  - Write Update协议需要进行多次写广播操作
  - Write Invalidate协议只需要一次失效操作
- 对同一个块中多个不同字进行写操作
  - Write Update协议对每个字的写均要进行一次广播
  - Write Invalidate协议仅在对本块第一次写时进行失效操作
- 一个处理器写到另一个处理器读之间的延迟
  - Write Update协议下通常较低
  - Write Invalidate协议中，需要读一个新的备份
- 在基于总线的多处理机中， Write Invalidate协议成为绝大多数系统设计的选择

## 四、基于监听的Cache一致性协议

- 基于监听协议、写使无效、写回Cache的实现技术
  - 用Cache中块的标志位实现监听
  - 给每个Cache块加一个特殊的状态位说明其共享
- 总线是广播媒介
  - 总线上的事务对所有Cache是可见的
  - 这些事务对所有处理器以同样的顺序可见
- Cache控制器监听(snoop)共享总线上的所有事务
  - 根据Cache块中的状态不同会产生不同的事务
  - 通过执行不同的总线事务来保证Cache一致性

**Cache控制器**

- Cache控制器接收两方面的请求输入
  - 处理器的请求(load/store)
  - 监听到的总线请求/响应
- Cache控制器根据这两方面的输入产生动作
  - 更新Cache块的状态
  - 提供数据
  - 产生新的总线事务

### (1) Valid/Invalid协议

- 总线事务

| Actions       |
| ------------- |
| 处理器读 PrRd |
| 处理器写 PrWr |
| 总线读 BusRd  |
| 总线写 BusWr  |

- 状态转换图
  - 发生 `BusWr` 时，将除当前处理器以外的其他处理的同一个地址Cache置`I`
  - 访问 `I` Cache时，必然触发`BusRd`
- 每次写入都需要更新主存
- 每次写入都需要广播和监听状态

![](./img/2022-06-13-21-14-49.png)

### (2) MSI(Modified/Shared/Invalid)协议

- 三种状态
  - Modified
    - 只有该数据块的备份是最新的，主存和其他处理器中的数据是陈旧的
  - Shared
    - 该块在此处理器中未被修改过，主存中的内容是最新的
  - Invalid
    - 该块是无效块
- 增加新的总线事务`BusRdx`
  - 总线排他读，得到独占的Cache数据块
  - 目的是修改数据块，使得其余备份都失效
- 对于`I`Cache的读写会触发miss(r/w)
  - 读miss会触发，`M`块的写回？

| Actions       |
| ------------- |
| 处理器读 PrRd |
| 处理器写 PrWr |
| 总线读 BusRd  |
| 总线读 BusRdx |
| 总线写 BusWB  |

- 状态转换
- PrRd
  - Cache miss -> 产生BusRd事务
  - Cache hit -> 无总线动作
- PrWr
  - 在非Modified状态时，产生总线`BusRdx`事务
    - 告知其余备份失效
  - 当在Modified状态时，无总线动作
    - 避免重复发布事务
- BusRd
  - 在Modified状态
    - 更新存储器和有需求的Cache
    - 引起总线事务的Cache块状态转变为Shared

![](./img/2022-06-13-21-29-27.png)


**特点**

- 允许Cache在不更新内存的情况下为写操作提供服务
- 主存中可能有陈旧的数据
- Cache必须覆盖来自主存的响应

**MESI协议**

- 增加一个`E`(Exclusive, unmodified)状态
  - 提高私有数据的读写性能
- 独占，没有其他处理器缓存了该数据备份，可以直接修改，不必马上同步到主存中
  - 否则需要发送`BusRdX`

![](./img/2022-06-13-23-07-55.png)

## 五、一致性面临的问题

### (1) 一致性和假共享

- Cache一致性是在块级别实现
  - 一个Cache块中包含多个数据字
- 假设处理器P1写字i，处理器P2写字k，且两个字有相同的块地址
  - 由于地址在同一块中，该块可能会多次不必要的失效（ ping-pong问题）

### (2) 一致性与同步

### (3) 一致性和总线占用率

- 将一条原子指令拆分成Load-reserve和Store-conditional