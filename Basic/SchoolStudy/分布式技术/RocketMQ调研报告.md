# RocketMQ 调研报告

- [RocketMQ 调研报告](#rocketmq-调研报告)
  - [调研内容](#调研内容)
  - [RocketMQ特性](#rocketmq特性)
    - [消息顺序](#消息顺序)
    - [消息过滤](#消息过滤)
    - [*消息可靠性](#消息可靠性)
    - [RocketMQ与Kafka适用的应用场景](#rocketmq与kafka适用的应用场景)
  - [RocketMQ架构](#rocketmq架构)
    - [RocketMQ架构与Kafka有何异同](#rocketmq架构与kafka有何异同)
  - [RocketMQ消息序列化与反序列化](#rocketmq消息序列化与反序列化)
    - [FastJson消息序列化](#fastjson消息序列化)
  - [RocketMQ底层网络通信](#rocketmq底层网络通信)
    - [协议与编码](#协议与编码)
    - [消息通信方式](#消息通信方式)
  - [RocketMQ的持久化](#rocketmq的持久化)
    - [存储架构](#存储架构)
    - [页缓存与内存映射](#页缓存与内存映射)
    - [消息刷盘](#消息刷盘)

- [RocketMQ](https://github.com/apache/rocketmq/tree/master/docs/cn)
- [RocketMQ与Kafka比较](https://www.cnblogs.com/ynyhl/p/11320797.html)
- [RocketMQ与kafka异同](https://cloud.tencent.com/developer/article/1729586)
- [RocketMQ消息序列化](https://www.jianshu.com/p/d5da161efc33)

## 调研内容

- RocketMQ是阿里巴巴开源的分布式消息中间件,具有高性能、高可靠、高实时、 分布式等特点
- 调研内容包括: 
  - RocketMQ与Kafka适用的应用场景？
  - RocketMQ架构与Kafka有何异同？
  - RocketMQ的消息序列化与反序列化是如何设计的？
  - RocketMQ底层网络通信是如何设计的？
  - RocketMQ的持久化是如何设计的？ 
- 报告格式要求: 
  - Word格式
  - 时间要求：3月29日前上交调研报告，邮件发送至liuxiaodong@ict.ac.cn


## RocketMQ特性

- [RocketMQ特性](https://github.com/apache/rocketmq/blob/master/docs/cn/features.md)

### 消息顺序

- 消息顺序
  - 消息有序指的是一类消息消费时，能按照发送的顺序来消费
  - 例如：
    - 一个订单产生了三条消息分别是订单创建、订单付款、订单完成
    - 消费时要按照这个顺序消费才能有意义，但是同时订单之间是可以并行消费的
  - RocketMQ可以严格的保证消息有序

- 全局顺序消息与分区顺序消息
  - 全局顺序是指某个Topic下的所有消息都要保证顺序, 部分顺序消息只要保证每一组消息被顺序消费即可
    - 全局顺序 对于指定的一个 Topic，所有消息按照严格的先入先出（FIFO）的顺序进行发布和消费
      - 适用场景：性能要求不高，所有的消息严格按照 FIFO 原则进行消息发布和消费的场景
    - 分区顺序 对于指定的一个 Topic，所有消息根据 sharding key 进行区块分区。 同一个分区内的消息按照严格的 FIFO 顺序进行发布和消费。 Sharding key 是顺序消息中用来区分不同分区的关键字段，和普通消息的 Key 是完全不同的概念
      - 适用场景：性能要求高，以 sharding key 作为分区字段，在同一个区块中严格的按照 FIFO 原则进行消息发布和消费的场景

### 消息过滤

- RocketMQ的消费者可以根据Tag进行消息过滤，也支持自定义属性过滤。消息过滤目前是在Broker端实现的，优点是减少了对于Consumer无用消息的网络传输，缺点是增加了Broker的负担、而且实现相对复杂

### *消息可靠性

- RocketMQ支持消息的高可靠，影响消息可靠性的几种情况：
 1. Broker非正常关闭
 2. Broker异常Crash
 3. OS Crash
 4. 机器掉电，但是能立即恢复供电情况
 5. 机器无法开机（可能是cpu、主板、内存等关键设备损坏）
 6. 磁盘设备损坏
- 1)、2)、3)、4) 四种情况都属于硬件资源可立即恢复情况，RocketMQ在这四种情况下能保证消息不丢，或者丢失少量数据（依赖刷盘方式是同步还是异步）
- 5)、6)属于单点故障，且无法恢复，一旦发生，在此单点上的消息全部丢失
- RocketMQ在这两种情况下，通过异步复制，可保证99%的消息不丢，但是仍然会有极少量的消息可能丢失。通过同步双写技术可以完全避免单点，同步双写势必会影响性能，适合对消息可靠性要求极高的场合，例如与Money相关的应用
> 注：RocketMQ从3.0版本开始支持同步双写

### RocketMQ与Kafka适用的应用场景

- Kafka
  - 面向大数据，高吞吐场景
- RocketMQ
  - 面向快速响应，高可靠性场景

## RocketMQ架构

- RocketMQ架构上主要分为四个部分
  - Producer：消息发布的角色，支持分布式集群方式部署。Producer通过MQ的负载均衡模块选择相应的Broker集群队列进行消息投递，投递的过程支持快速失败并且低延迟。
  - Consumer：消息消费的角色，支持分布式集群方式部署。支持以push推，pull拉两种模式对消息进行消费。同时也支持集群方式和广播方式的消费，它提供实时消息订阅机制，可以满足大多数用户的需求。
  - NameServer：NameServer是一个非常简单的Topic路由注册中心，其角色类似Dubbo中的zookeeper，支持Broker的动态注册与发现。主要包括两个功能：Broker管理，NameServer接受Broker集群的注册信息并且保存下来作为路由信息的基本数据。然后提供心跳检测机制，检查Broker是否还存活；路由信息管理，每个NameServer将保存关于Broker集群的整个路由信息和用于客户端查询的队列信息。然后Producer和Conumser通过NameServer就可以知道整个Broker集群的路由信息，从而进行消息的投递和消费。NameServer通常也是集群的方式部署，各实例间相互不进行信息通讯。Broker是向每一台NameServer注册自己的路由信息，所以每一个NameServer实例上面都保存一份完整的路由信息。当某个NameServer因某种原因下线了，Broker仍然可以向其它NameServer同步其路由信息，Producer和Consumer仍然可以动态感知Broker的路由的信息。
  - BrokerServer：Broker主要负责消息的存储、投递和查询以及服务高可用保证，为了实现这些功能，Broker包含了以下几个重要子模块
    - Remoting Module：整个Broker的实体，负责处理来自Client端的请求
    - Client Manager：负责管理客户端(Producer/Consumer)和维护Consumer的Topic订阅信息
    - Store Service：提供方便简单的API接口处理消息存储到物理硬盘和查询功能
    - HA Service：高可用服务，提供Master Broker 和 Slave Broker之间的数据同步功能
    - Index Service：根据特定的Message key对投递到Broker的消息进行索引服务，以提供消息的快速查询

### RocketMQ架构与Kafka有何异同

- RocketMQ本身基于Kafka设计，因此在架构上，两者都比较类似，均包含有 Producer、Consumer、Broker以及注册中心四个部分，但在Kafka中，使用Zookeeper来协调节点，而rocketMQ则使用自研的NameServer
- 相较于Zookeeper，但因为NameServer的路由数据在每个副本上都保有，某个NameServer下线了，Broker仍然可以向其他NameServer同步路由信息

## RocketMQ消息序列化与反序列化


### FastJson消息序列化

- fastjson是阿里巴巴的开源JSON解析库，它可以解析JSON格式的字符串，支持将Java Bean序列化为JSON字符串，也可以从JSON字符串反序列化到JavaBean


## RocketMQ底层网络通信

### 协议与编码

- 在Client和Server之间完成一次消息发送时，需要对发送的消息进行一个协议约定，因此就有必要自定义RocketMQ的消息协议。同时，为了高效地在网络中传输消息和对收到的消息读取，就需要对消息进行编解码。在RocketMQ中，RemotingCommand这个类在消息传输过程中对所有数据内容的封装，不但包含了所有的数据结构，还包含了编码解码操作

### 消息通信方式

- 在RocketMQ消息队列中支持通信的方式主要有同步(sync)、异步(async)、单向(oneway) 三种。其中“单向”通信模式相对简单，一般用在发送心跳包场景下，无需关注其Response。这里，主要介绍RocketMQ的异步通信流程

## RocketMQ的持久化


### 存储架构

- 消息存储架构图中主要有下面三个跟消息存储相关的文件构成。

- (1) CommitLog：消息主体以及元数据的存储主体，存储Producer端写入的消息主体内容,消息内容不是定长的。单个文件大小默认1G, 文件名长度为20位，左边补零，剩余为起始偏移量，比如00000000000000000000代表了第一个文件，起始偏移量为0，文件大小为1G=1073741824；当第一个文件写满了，第二个文件为00000000001073741824，起始偏移量为1073741824，以此类推。消息主要是顺序写入日志文件，当文件满了，写入下一个文件；

- (2) ConsumeQueue：消息消费队列，引入的目的主要是提高消息消费的性能，由于RocketMQ是基于主题topic的订阅模式，消息消费是针对主题进行的，如果要遍历commitlog文件中根据topic检索消息是非常低效的。Consumer即可根据ConsumeQueue来查找待消费的消息。其中，ConsumeQueue（逻辑消费队列）作为消费消息的索引，保存了指定Topic下的队列消息在CommitLog中的起始物理偏移量offset，消息大小size和消息Tag的HashCode值。consumequeue文件可以看成是基于topic的commitlog索引文件，故consumequeue文件夹的组织方式如下：topic/queue/file三层组织结构，具体存储路径为：$HOME/store/consumequeue/{topic}/{queueId}/{fileName}。同样consumequeue文件采取定长设计，每一个条目共20个字节，分别为8字节的commitlog物理偏移量、4字节的消息长度、8字节tag hashcode，单个文件由30W个条目组成，可以像数组一样随机访问每一个条目，每个ConsumeQueue文件大小约5.72M；

- (3) IndexFile：IndexFile（索引文件）提供了一种可以通过key或时间区间来查询消息的方法。Index文件的存储位置是：$HOME \store\index${fileName}，文件名fileName是以创建时的时间戳命名的，固定的单个IndexFile文件大小约为400M，一个IndexFile可以保存 2000W个索引，IndexFile的底层存储设计为在文件系统中实现HashMap结构，故rocketmq的索引文件其底层实现为hash索引。

- 在上面的RocketMQ的消息存储整体架构图中可以看出，RocketMQ采用的是混合型的存储结构，即为Broker单个实例下所有的队列共用一个日志数据文件（即为CommitLog）来存储。RocketMQ的混合型存储结构(多个Topic的消息实体内容都存储于一个CommitLog中)针对Producer和Consumer分别采用了数据和索引部分相分离的存储结构，Producer发送消息至Broker端，然后Broker端使用同步或者异步的方式对消息刷盘持久化，保存至CommitLog中。只要消息被刷盘持久化至磁盘文件CommitLog中，那么Producer发送的消息就不会丢失。正因为如此，Consumer也就肯定有机会去消费这条消息。当无法拉取到消息后，可以等下一次消息拉取，同时服务端也支持长轮询模式，如果一个消息拉取请求未拉取到消息，Broker允许等待30s的时间，只要这段时间内有新消息到达，将直接返回给消费端。这里，RocketMQ的具体做法是，使用Broker端的后台服务线程ReputMessageService不停地分发请求并异步构建ConsumeQueue（逻辑消费队列）和IndexFile（索引文件）数据

### 页缓存与内存映射

- 页缓存（PageCache)是OS对文件的缓存，用于加速对文件的读写。一般来说，程序对文件进行顺序读写的速度几乎接近于内存的读写速度，主要原因就是由于OS使用PageCache机制对读写访问操作进行了性能优化，将一部分的内存用作PageCache。对于数据的写入，OS会先写入至Cache内，随后通过异步的方式由pdflush内核线程将Cache内的数据刷盘至物理磁盘上。对于数据的读取，如果一次读取文件时出现未命中PageCache的情况，OS从物理磁盘上访问读取文件的同时，会顺序对其他相邻块的数据文件进行预读取。

- 在RocketMQ中，ConsumeQueue逻辑消费队列存储的数据较少，并且是顺序读取，在page cache机制的预读取作用下，Consume Queue文件的读性能几乎接近读内存，即使在有消息堆积情况下也不会影响性能。而对于CommitLog消息存储的日志数据文件来说，读取消息内容时候会产生较多的随机访问读取，严重影响性能。如果选择合适的系统IO调度算法，比如设置调度算法为“Deadline”（此时块存储采用SSD的话），随机读的性能也会有所提升。

- 另外，RocketMQ主要通过MappedByteBuffer对文件进行读写操作。其中，利用了NIO中的FileChannel模型将磁盘上的物理文件直接映射到用户态的内存地址中（这种Mmap的方式减少了传统IO将磁盘文件数据在操作系统内核地址空间的缓冲区和用户应用程序地址空间的缓冲区之间来回进行拷贝的性能开销），将对文件的操作转化为直接对内存地址进行操作，从而极大地提高了文件的读写效率（正因为需要使用内存映射机制，故RocketMQ的文件存储都使用定长结构来存储，方便一次将整个文件映射至内存）

### 消息刷盘

- (1) 同步刷盘：如上图所示，只有在消息真正持久化至磁盘后RocketMQ的Broker端才会真正返回给Producer端一个成功的ACK响应。同步刷盘对MQ消息可靠性来说是一种不错的保障，但是性能上会有较大影响，一般适用于金融业务应用该模式较多。

- (2) 异步刷盘：能够充分利用OS的PageCache的优势，只要消息写入PageCache即可将成功的ACK返回给Producer端。消息刷盘采用后台异步线程提交的方式进行，降低了读写延迟，提高了MQ的性能和吞吐量