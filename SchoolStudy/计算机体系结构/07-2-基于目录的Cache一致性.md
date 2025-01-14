# 基于目录的Cache一致性

## 一、基于目录的协议

**目录协议对于监听协议的改进**

|               监听协议               |                      目录协议                       |
| :----------------------------------: | :-------------------------------------------------: |
|     监听协议通过内存总线广播请求     | 目录协议只向那些可能持有该Cache line的Cache发送消息 |
|    侦听协议难以扩展到大量的处理器    |                可以扩展到大量处理器                 |
| 需要使用额外的带宽缓存侦听请求的标记 |       需要额外的目录存储空间来跟踪可能的共享        |

- 每个存储行对于一个目录项
  - 记录有该存储行副本的处理器
  - 处理器对改行进行写时，根据目录项记录的内容传播数据
  - 只向持有此行的备份的处理器发送信号，避免了广播

### (1) MSI目录协议

- Cache状态: M、S、I
- 目录状态
  - Un: Uncached，所有处理器核都没有副本
  - Sh: Shared, 一个或多个处理器核具有读权限(S)
  - Ex: Exclusive, 只有一个处理器核具有读和写权限(M)

#### Cache状态迁移

**处理器访问产生的状态迁移**

![](./img/2022-06-14-10-29-32.png)

**目录请求产生的状态迁移**

![](./img/2022-06-14-10-30-50.png)

**evictions产生的状态迁移**

![](./img/2022-06-14-10-32-30.png)

**状态迁移图**

![](./img/2022-06-14-10-33-21.png)

#### 目录状态迁移

**数据请求产生的状态迁移**


- store操作会向目录发送 `ExReq`
  - 将 shares 设置为自己
- Sharers: 共享者集合

![](./img/2022-06-14-10-34-35.png)

**写回产生的状态迁移**

![](./img/2022-06-14-10-35-28.png)

### (2) 缺失状态保持寄存器

- MSHR: 在Cache外保持加载失败(load misses)和写入
  - 允许CPU在Cache miss后继续执行其他指令

## 二、目录结构

- 目录需要跟踪共享同一个Cache块的所有处理器核心
- 对于每个块，保存持有块的共享者所需的空间可能会随着共享者数量的增加而增加

### (1) Flat

- 基于内存的目录
  - 使用少量的主存空间来存储每一个Cache line的状态和共享者
  - 使用位向量来编码共享者

### (2) Full-Map

- 不需要记录系统中的每一个Cache line——只需要记录**私有缓存**
  - 将目录组织成一个Cache

**目录引发的无效**

- Full-Map只提供有限的关联性，当存在换出时，需要让当前entry的所有共享者失效，然后再将此entry用于新地址

**共享者集合的不精确表示**

- 粗粒度位向量
  - 如每四个处理器核心用1bit表示
- 指针
  - 保留有限共享者指针，在溢出时标记`all`并进行广播
- 允许出错

**协议竞争**

- 基于目录的一致性协议要求对同一地址的多个请求时序列化的
  - 相同地址请求排队或NACK并重试

### (3) In-Cache目录

- 通用的多核内存层次结构
- 将目录信息嵌入在共享的cache tags中

## 三、一致性协议面临的问题

### (1) 协议死锁

- 解决方案: 独立的虚拟网络
- 大多数协议需要至少两个虚拟网络(请求/应答)，通常需要两个以上

