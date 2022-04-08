# Unikernels: Library Operating Systems for the Cloud


- [Unikernels: Library Operating Systems for the Cloud](#unikernels-library-operating-systems-for-the-cloud)
  - [阅读记录](#阅读记录)
    - [Problem & Background](#problem--background)
    - [Challenges](#challenges)
    - [State-of-the-arts](#state-of-the-arts)
    - [Key insights/ideas/techniques](#key-insightsideastechniques)
      - [Appliance](#appliance)
      - [Mirage](#mirage)
        - [Device Driver](#device-driver)
        - [Type-Safe Protocol I/O](#type-safe-protocol-io)
    - [总结](#总结)
    - [Lessons learned from experiments](#lessons-learned-from-experiments)

## 阅读记录

### Problem & Background

- background， 计算虚拟化
- problem
  - 现行的VM虽然将应用程序封装在虚拟机镜像中，但是与原本的系统相比，尽管VM中运行特定的应用，但是其所有使用的系统镜像并没有特殊化

### Challenges



### State-of-the-arts

- hypervisor
- lib OS

### Key insights/ideas/techniques

> lib OS 给予开发者更多的控制权，让开发者能够根据程序的特性，深度定制操作系统的功能，与此同时，也大大增加了开发的难度

#### Appliance

- 配置
  - 不同于通过配置文件将诸如数据库、web服务连接在一起，unikernels则将这些应用视为单个程序中的库，使得配置的定义变得显示且可编程化
- 安全
  - 在外部，通过ssl/ssh等协议信任外部实体
  - 在内部，通过专门化编译，运行时的普遍类型安全，以及hypervisor和工具链扩展，防止不可见的编译器或运行时错误
- 单地址空间
  - 由于访问控制依赖于语言的类型安全机制来强制执行，而不再依赖于用户空间进程，因此虚拟地址可以进一步简化为单地址空间模型
- 密封
  - 通过在Xen中增加功能，以使得编译后的Appliance使用 W^X 的内存访问策略
- 地址空间随机化
  - 编译系统镜像时实现地址随机化

> Write Xor Execute (W^X)
> 应用程序用户空间中的每个页都可以是可写或可执行的，但不能同时可以又可执行

#### Mirage

- 主要功能
  - 编译和链接 OCaml 代码为一个可以在Xen中运行的VM镜像
- Ocaml语言
- PVBoot Library
  - 提供初始化一个单VCPU VM 和 Xen event channels，并跳转至入口方法的支持
  - 与传统OS不同，不支持多进程和非阻塞的线程
  - 提供两种内存页面分配器
    - Slab
      - 支持C代码
    - Extent
      - 保留一个连续的内存区域
      - 以2MB的块进程操作，并允许映射到 x86-64 的超级页
    - 内存区域中被静态地分配给不同的角色
      - 如 垃圾收集堆，I/O 数据页
  - Domainpoll function，阻塞 一组通道和超时的 VM
  - 提供最小的异步支持
    - 事件驱动的VM将会休眠，知道I/O可用或超时
- Lauguage Runtime
  - 修改两个核心区域: 内存管理 与 并发
  - 内存管理
    - 内存区域划分
    - VM之间的通信
      - Local VM 通过hypervisor将内存页访问权限授予remote VM，并使用这种方式进行直接通信
  - 并发
    - PVBoot's simple domainpoll function
    - 集成了Lwt协程库
      - 在内部将阻塞的方法评估为事件描述符，从而能够为开发者提供直线的控制流
    - Mirage 提供一个轮询监听事件并唤醒轻量级线程的评估器
      - 因此，VM要么执行OCaml代码，要么被阻塞，不存在内部抢占或者异步中断
    - 大多数线程调度和线程逻辑都包含在代码库中，开发者可以根据应用的需要进行修改
      - eg: tagging thread for debugging、statistics or prioritisation

##### Device Driver

- Mirage 对 Xen 提供的抽象设备的接口进行驱动
  - Xen Devices包括一个在VM 中的*前端驱动*，以及一个多路复用前端请求的*后端驱动*
    - 两者由一个能够另一端发送信号的事件通道和一个被分成由生产者/消费者指针跟踪的固定大小的 requests slots 的单个内存页面连接
      - response 被写入到与 requests 相同的slut中
        - 这种从一段写入，另一端读出的数据结构称为 ring
      - 前端驱动实现了流量控制，避免 ring 溢出
  - Xen 中多数设备使用这种模式

**Zero-Copy Device I/O**

- Xen device protocol 并不直接数据写入共享内存中，而是用来协调通过引用传递4KB内存页
  - 两个通信虚拟机共享一个*grant table*，该表将pages映射到此表中的整数偏移（称为grant），并由hypervisor检查并强制执行更新
  - grant通过设备驱动共享ring进行交换，并由remote vm查找，以及进行page 映射或将page拷贝到自己的地址空间中
    - 一旦数据到达remote VM中，就必须被传输给应用
    - 由于POSIX APIs不支持零拷贝socket，因此通常需要从VM'Kernel到正确的用户空间进程的二次拷贝
- Unikernel没有用户空间，因此收到的页可以直接交给应用
  - cstruct库将下层的数组分片成更小的视图来避免复制
- 对于需要进行手动追踪与释放的资源
  - Mirage 使用 OCaml的类型系统来保证资源被正确地释放
  - 尽管如此，也无法保证消除所有的内存泄露风险，因为结构体中的不被删除的引用将会一直存在
  
##### Type-Safe Protocol I/O

- Mirage使用 OCaml 实现协议库，保证了所有外部I/O的处理时类型安全的，从而让unikernel在面对内存溢出时更健壮
- 数据以离散包的形式到达网络栈与存储站
  - Mirage 使用映射能够产生类型流的方法到包流的channel iteratees的方式，解决数据包与流之间的间隙

**网络处理**

- Mirage 网络栈强调应用级可控性
  - 提供了两种通信方式
    - vchan传输
      - 快速的，主机上，虚拟机之间的传输
      - 基于共享内存的快速互联
    - 对外通信的Ethernet传输
      - 通过 scatter-gather I/O 解决协议处理的问题
        - 网络堆栈为每个写入分配一个head page，网络库根据需要，将传入的有效负载重新排列到子视图中，然后将所有片段作为一个数据包写入设备环

**存储**

- Mirage 块设备与网络设备一样使用 Ring 抽象，使用相同的I/O页来提供高效的块级别访问，基于OCaml 文件系统与缓存 库
  - 程序可以选择缓存策略，而不是使用默认的方式，而不同的缓存策略可以作为库的方式提供
    - 缓存方式可以跟随程序的不同，高度定制化


### 总结

- 性能
  - Unikernel能够在 50ms 内重新启动，使得微重启称为可能

- 类型安全系统
  - 类型安全
    - 每个变量、函数自变量和函数返回值将存储一个可接受的类型的数据，并意味着涉及不同类型的值的操作“有意义”且不会导致数据丢失、位模式解释不正确或内存损坏
- 重构OS为一组可以被链接到程序的库
- 向后兼容性


### Lessons learned from experiments