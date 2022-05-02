# Reading

## 工作说明

大家好，ATC 2022 的第二轮审稿工作开始了，需要大家帮忙一起审一下论文，并写审稿意见（尽量英文）。由于时间比较紧急，请大家在4月3日中午前把 Review 意见反馈给我

1）review 文件中每个部分都要填，其中 comment 部分写大约 300-500 个单词的评论，尽量用英文

2）Questions for authors' response 部分需要提出 2-3 个问题

3）如果 reject，需要把拒绝的理由给的充分一些

4）请大家在 4月3日中午之前将 review 发我。

本次审稿共 5 篇论文，题目如下图所示，大家积极认领哇

## 阅读记录

### Problem & Background

- 背景
  - 受限于硬件技术，当前GPU提供商难以在GPU内存容量上继续扩展，应对GPU使用需求的增长，常见的方式是使用共享多GPU服务器，这样即能够提供足够的算力，相比于单独机器，同时节省基础设施的成本
    - 多GPU服务器上往往运行广泛且差异化的应用
      
- 问题
  - 在多GPU服务器中，不同GPU中的内存相互独立，服务于各自的应用，因此存在当部分GPU因内存不足而发生与host内存交换时，其他GPU的内存可能仍有空闲
    - 这使得多GPU服务器中GPU内存并未得到充分地使用

### Challenges

- GPU中的空闲内存数量高度可变且难以提前预知，因此有效获取可用的邻近GPU空闲内存非常困难

### State-of-the-arts

- 应对无法装入GPU内存的大型数据
  - 在多GPU服务器中，可以使用图分区法，使得每个分区适合于单独的GPU
    - 引入了更多的复杂性，以至于一些图算法无法运行在多GPU服务器中
    - 此外，对于DNN这种会占用多个GPU的训练任务，也会阻碍其他工作负载的在GPU上的扩展
  - 使用UVM(unified virtual memory)将host端的内存作为交换设备来提供无限内存的抽象 
    - 这种方式受限于PCIe接口速率, 产生显著的性能开销，同时也无法避免一些GPU内存空闲的情况
  - 分析DL训练负载的数据流图，插入 pre-eviction 与 pre-fetch 操作
  - 内存压缩技术

- 高速连接
  - Nvidia提供了NVLink，使得GPU之间能够相互访问，且带宽远高于PCIe(600GB/s -> 32GB/s)
    - Nvidia A100内置NVLink支持多达12个三代NVLink的连接
- 平台无关的控制
  - Nvidia与AMD提供了UVM技术，使得大内存应用能够在有限内存的GPU中运行，这项技术作为GPU驱动实现，因此在UVM中实现memory harvesting不需要修改GPU应用或ML框架
    - UVM实现原理(page fault发生在GPU而不是CPU中)
      - UVM将host内存作为GPU的交换空间，driver通过page fault来判断GPU所访问的Page是在GPU还是在Host内存上
      - 通过一个统一的页表，UVM将GPU虚拟地址转换为GPU物理地址或主机物理地址
        - 如果UVM判断GPU访问的页面通过统一的页表映射在Host内存上
          - 触发page fault
          - UVM将数据写入GPU内存中(PCIe)
        - 当GPU中的内存空间不足时，驱动则要在处理缺页异常前，将一个旧页交换出GPU
          - page换入换出时，需要更新映射
- Pre-ef-host

### Key insights/ideas/techniques

> 考虑 NVLink 的高速性，GPU使用自己的Local memory作为顶级Cache，使用 spare memory 作为二级Cache，而host内存则作为最后一层，弥补了NVLink引入导致的访问邻居GPU内存与访问Host内存的速度差异

- TODO: 
  - 每个GPU中的spare memory是否有上限，yielding GPU产生的性能损失是否有评估
  - Harvesting GPU 与 yielding GPU 如何划分，如果是固定分配，当任务首先被调度到yielding GPU上执行时，如何保证memHarvester有效？如果是动态分配，当所有GPU内存负载都很高时，及没有空闲内存时, 为Harvesting GPU带来的性能提升，与yielding GPU的性能损失相比，系统整体的效率是否有提高
    - 一般情况下，Harvesting GPU的提升巨大，yielding GPU性能损失小，整体有提高
  - 考虑动态机制，是否有测试多GPU服务器不同负载下，memHarvester 与 HUVM对整体性能的影响？
  - 由于memHarvester会占用NVLink，那对于要使用NVLink进行并行工作的任务是否会产生影响？
  - ?spare memory增加，反而导致性能略微下降(Figure 9)


- 核心理念:
  - NVLink的出现，使得访问Neighbor GPU内存的速度远快于通过PCIe访问Host内存，基于此设计了HUVM新型层次结构，而为实现对这种层次结构内存的管理，设计了内存管理工具memHarvester
  - 将GPU通过PCIe访问Host Memory的延迟转化为通过NVLink访问Neighbor GPU的延迟，从关键路径上优化了延迟

- HUVM (hierarchical unified virtual memory)
  - HUVM由 local GPU, spare memory of neighbor GPUs, the host memory 三层结构构成，GPU按顺序依次访问

- memHarvester
  - 描述
    - 在GPU Driver层实现的集中式协调器，负责系统中所有GPU内存的管理
    - 使用一种多路并行预取器，利用多GPU系统中的PCIe、NVLink
      - 当要从Local memory中换出chunk时，如果邻居存在空闲的spare memory，则优先使用NVLink而不是PCIe来进行内存的换出
  - memHarvester预取过程
    - memeHarvester首先通过NVLink从邻居的空闲内存中预取数据到当前GPU
      - 同时，如果邻居GPU的PCIe通道空闲，则允许预取host内存中的数据到空闲内存
        - 使用这种方式可以有效地将读取主机内存的延迟转化为读取空闲内存的延迟
    - 由于spare memory空间有限，因此存在spare memory与host memory数据的swap
  - *memHarvester使用2MB大页来提升性能
  - 当划出spare memory的GPU上运行的应用需要额外内存空间时，memHarvester会立即将spare memory恢复成原始的物理内存，以降低性能影响
    - removable标记，否则不处理
  - memHarvester透明地检测spare memory并动态地生成新的内存层次结构

- 有效收割邻居GPU上的spare memeory所采用的技术
  - hierarchical and background eviction (分层与后台驱除)
  - fetching data in parallel (并行获取数据)
  - prefetching in a neighbor GPU memory (数据预取)

- memHarvester主要流程
  1. 当前GPU需要换出数据时，memHarvester使用基于NVLink连接的spare memory作为victim buffer而不是直接向Host memory换出，以此来换出数据时的延时
    - memHarvester使用pre-eviction来最大化spare memory的效益
  2. 使用memHarveser也无法完全避免将数据换出到host memory
    - memHarvester使用大页来环节换出时的性能损失
  3. 如果访问host memory不可避免，则会利用并行性来处理 page fault
     - Fault batch 一部分读入当前GPU memory，另一部分读入Harvested GPU 的Spare Memory，从而同时利用两条独立的PCIe通道
       - 从头开始，从尾开始
  4. 存放在spare memory中的数据会通过NVLink预取到Local GPU，同时也会将Host Memory的数据通过PCIe预取到spare memory或者Local GPU memory，取决于PCIe的空闲情况
       - m:n, memHarvester按请求顺序处理

- Eviction
  - 流程
    - Local GPU 换出内存到Spare Memory后，继续进行Page的取回，此时memHarvester启动一个后台线程，将harvested中存入的换出内存复制到host memory上
      - copy完成后，将harvested中的这些内存标记为 removable，这些内存被视为空闲内存
    - 当harvested GPU需要更多内存时，就会产生缺页异常，memHarvester 将 removable的page恢复为Local Memory（LRU）
      - 如果此 harvested GPU 中没有空闲与removable的内存，则此GPU必须等待直到内存变成removeable
      - 这种情况很少发生
  - Pre-eviction
    - 默认情况下，当GPU中的空闲内存块小于50时，memHarvester启动pre-eviction线程
      - pre-eviction线程与writeback线程组成流水线，共同完成eviction过程
  - Large page eviction
    - 使用内核的连续内存页分配，用一个操作完成2MB页向host内存的写回，而不是分成512个4KB页
  - Eviction policy
    - round-robin fashion

- Fetch
  - memHarvester为每个GPU启动缺页异常处理线程, 分发处理任务给每个处理线程
    - harvesting GPU的缺页处理线程从 fault buffer 头部开始取，yielding GPU 的处理线程则从尾部开始，将数据取到harvested memory中
      - page fault batch: 
    - 之后，spare memory中取回的faults将通过Vlink消费
  - Multi-Path parallel prefetcher
    - 存放在spare memory中的数据会通过NVLink预取到Local GPU，同时也会将Host Memory的数据通过PCIe预取到spare memory或者Local GPU memory，取决于PCIe的空闲情况
    - memHarvester使用一个跨步预取器
    - 通过从page fault history中提取的内存访问模式, memHarvester根据块的位置从主机内存或收集的内存中预获取接下来的几个块
      - 我们根据经验选择预取量为32MB，步幅为2MB

### Lessons learned from experiments



#### 实验

- 实验配置
  - AWS p3.8xlarge instance.
    - four NVIDIA V100 (16GB) GPUs connected through NVLink
    - PCIe 3.0 
      - TODO: PCIe 4.0 2x PCIe 3.0, 
- 对照组
  - Base: UVM与 imitate pre-eviction & prefetch
  - Pre-ef-Host
- 实验
  - 采用不同机制下的性能比较
  - 采用不同的技术组合下，harvester带来的性能提升
  - 不同应用对于预取内存数量的敏感程度
  - 不同应用对于spare memory数量的敏感程度
  - 不同机制下吞吐量的提升(H:Y有变化)
  - 不同应用，在不同 H:Y 下的内存使用情况

- 实验结果
  - 对于DNN训练和图形分析工作负载的各种组合场景，实验显示，使用HUVM与memHarvester的多GPU服务器有2.71倍的性能提升，并且对同一服务器上的其他工作负载干扰很小


## 草稿

==+== USENIX ATC '22 Review Form
==-== DO NOT CHANGE LINES THAT START WITH "==+==" OR "==*==".
==-== For further guidance, or to upload this file when you are done, go to:
==-== https://atc22.usenix.hotcrp.com/offline

==+== =====================================================================
==+== Begin Review #1279
==+== Reviewer: Yungang Bao <baoyg@ict.ac.cn>

==+== Paper #1279
==-== Title: Memory Harvesting in Multi-GPU Systems with Hierarchical
==-==        Unified Virtual Memory

==+== Review Readiness
==-== Enter "Ready" if the review is ready for others to see:

Ready

==*== Overall merit
==-== Choices:
==-==    1. Reject
==-==    2. Weak reject
==-==    3. Weak accept
==-==    4. Accept
==-==    5. Strong accept
==-== Enter the number of your choice:

3

==*== Reviewer expertise
==-== Choices:
==-==    1. No familiarity
==-==    2. Some familiarity
==-==    3. Knowledgeable
==-==    4. Expert
==-== Enter the number of your choice:

2

==*== Paper summary
==-== Markdown styling and LaTeX math supported.

这篇论文着眼多GPU服务器承担多种不同计算任务负载的场景，在供应商提供的UVM与NVLink技术的基础上，设计HUVM内存层次结构以及相应的memHavester内存管理器，将Neighbor GPU的空闲内存作为Vitim Buffer，使得GPU通过PCIe访问Host Memory转化为通过NVLink访问Neighbor GPU，优化了关键路径上的性能，并提供Large Page，parallel fetch，multi-path parallel prefetcher等技术，进一步优化性能，最终显著降低访问Host memory的延时，并对于内存敏感性应用，相比之前的研究能够提供显著的吞吐性能提升

==*== Strengths
==-==    What are the paper’s important strengths? Just a couple sentences,
==-==    please.
==-== Markdown styling and LaTeX math supported.

1. 在多GPU服务器运行多种负载的场景中，通过NVLink使得Neighbor GPU的空闲内存能够被使用，提高了整体GPU内存的使用率
2. 利用NVLink与PCIe之间的速度差，设计了HUVM，提升了整体的性能
3. 内存管理器对HUVM中的eviction、fetch的实现逻辑完善，并能够利用到NVLink、PCIe进行并行操作，同时使用Large Page、PreEviction、Prefetch等技术，进一步提升性能

==*== Weaknesses
==-==    What are the paper’s important weaknesses? Just a couple
==-==    sentences, please.
==-== Markdown styling and LaTeX math supported.

1. spare memory的大小能够对提升效果产生影响，而由于spare memory调整是动态的，因此提升效果并不总是最好
2. 基于NVLink进行的设计，适用于支持NVLink的多GPU平台，应用场景较为狭窄

==*== Comments for author
==-== Markdown styling and LaTeX math supported.

- 作者感知敏锐且具有创新精神.NVLink技术对于多GPU系统来说是一个重磅事件，作者敏锐地发现NVLink与PCIe之间巨大差异所带来机会，即利用Neighbor GPU，同时，作者也审慎地基于实验评估在多GPU服务器运行多种负载的场景中的可行性，在计算机体系结构中层次结构设计很常见，GPU厂商也为解决GPU内存瓶颈的问题而提供UVM技术，然而这项技术却受限于PCIe接口速度，导致性能降低，作者创新性地将两者结合，提出HUVM内存层次结构并设计相应的内存管理工具，这无疑是启发性的。而在系统实现中，作者充分将HUVM设计理念落实，同时考虑到GPU内存负载的动态性，让系统也随之动态地进行变化，以提高内存的使用效率，同时，作者还根据GPU同时连接NVLink与PCIe这一特征，设计基于NVLink与PCIe并行的机制，并引入了诸如Large Page，prefetch、preeviction等多种性能优化的技术，最后克服了设计时的挑战，完成了整个系统，而这都能够体现出作者深厚的专业知识积累以及开拓精神。在实验验证的环节，除对系统本身进行验证外，作者还对实验中所选定的应用的GPU内存使用情况进行了分析，得到这些应用在所需内存数量上特征，以及对于不同数量prefrech的敏感程度，这些结果对于其他人的研究同样有所帮助，但无疑离不开作者细致的研究精神


==*== Questions for authors’ response
==-==    Specific questions that could affect your accept/reject decision.
==-==    Remember that the authors have limited space and must respond to
==-==    all reviewers.
==-== Markdown styling and LaTeX math supported.

1. 设置 Harvesting GPU 与 Yielding GPU的依据是什么? 调度GPU任务时是否会进行区分？如果任务被首先调度到 Yielding GPU 上执行时，memHarvester能否正常发挥作用？
2. 考虑到用户可能会利用NVLink进行多GPU的并行任务，当运行这样的任务导致NVLink繁忙，对memHavster会产生怎样的影响？


==*== Comments for PC
==-== (hidden from authors)
==-== Markdown styling and LaTeX math supported.



==+== Scratchpad (for unsaved private notes)

==+== End Review

## 工作内容

==+== USENIX ATC '22 Review Form
==-== DO NOT CHANGE LINES THAT START WITH "==+==" OR "==*==".
==-== For further guidance, or to upload this file when you are done, go to:
==-== https://atc22.usenix.hotcrp.com/offline

==+== =====================================================================
==+== Begin Review #1279
==+== Reviewer: Yungang Bao <baoyg@ict.ac.cn>

==+== Paper #1279
==-== Title: Memory Harvesting in Multi-GPU Systems with Hierarchical
==-==        Unified Virtual Memory

==+== Review Readiness
==-== Enter "Ready" if the review is ready for others to see:

Ready

==*== Overall merit
==-== Choices:
==-==    1. Reject
==-==    2. Weak reject
==-==    3. Weak accept
==-==    4. Accept
==-==    5. Strong accept
==-== Enter the number of your choice:

3

==*== Reviewer expertise
==-== Choices:
==-==    1. No familiarity
==-==    2. Some familiarity
==-==    3. Knowledgeable
==-==    4. Expert
==-== Enter the number of your choice:

2

==*== Paper summary
==-== Markdown styling and LaTeX math supported.

- This paper focuses on the scenario where multi-GPU servers consolidating various workloads that exhibit highly varying resource demands, and on top of the UVM and NVLink provided by the GPU vendors, this paper introduces a new unified memory, c called HUVM and the supporting memory management, called memHarvester, which has a set of techniques.By using the spare memory of the Neighbor GPU as a victim buffer, the latency of host memory access is turned into that of a neighbor GPU memory, optimizing performance on the critical path and also improving throughput performance compared to baseline and prior studies. 

==*== Strengths
==-==    What are the paper’s important strengths? Just a couple sentences,
==-==    please.
==-== Markdown styling and LaTeX math supported.

1. In scenarios where multiple GPU servers run various workloads, harvesting the idle memory of the Neighbor GPU by using NVLink, which improves the overall GPU memory utilization
2. By leveraging the speed difference between NVLink and PCIe and a set of techniques including large page support, parallel
fetch, and multi-path parallel prefetcher, memHarvester reduces the latency of accessing host memory and improves throughput performance


==*== Weaknesses
==-==    What are the paper’s important weaknesses? Just a couple
==-==    sentences, please.
==-== Markdown styling and LaTeX math supported.

1. The size of the spare memory can have an impact on the performance, and since the spare memory adjustment is dynamic, the performance will not always the best
2. The design based on NVLink is suitable for multi-GPU platforms that support NVLink, resulting in narrow usage scenarios.


==*== Comments for author
==-== Markdown styling and LaTeX math supported.

- 作者感知敏锐且具有创新精神.NVLink技术对于多GPU系统来说是一个重磅事件，作者敏锐地发现NVLink与PCIe之间巨大差异所带来机会，即利用Neighbor GPU，并审慎地基于实验评估在多GPU服务器运行多种负载的场景中的可行性. 事实上，在计算机体系结构中层次结构设计很常见，GPU厂商也为解决GPU内存瓶颈的问题而提供UVM技术，然而这项技术却受限于PCIe接口速度，导致性能降低，作者创新性地将两者结合，提出HUVM内存层次结构并设计相应的内存管理工具，这无疑是启发性的。而在系统实现中，作者充分将HUVM设计理念落实，同时考虑到系统中GPU内存负载的动态性，让系统也随之动态地进行变化，以提整体内存的使用效率，同时，作者还考虑到平台中的GPU通过PCIe连接主板与通过NVLink连接其他GPU这一特征，设计基于NVLink与PCIe并行的机制，与Large Page，prefetch、pre-eviction等多种性能优化的技术一起克服了设计时的挑战，完成了整个系统，而这都能够体现出作者深厚的专业知识积累以及开拓精神。在实验验证的环节，作者对系统在多个的场景下进行对照实验，体现出系统在不同场景下对于其他技术的优越性。而在这个过程中，作者也对实验中所选定的应用的GPU内存使用特点进行了分析，这些应用都是常见的对内存需求大的GPU应用，结果展示出这些应用在所需内存数量上各自的特点，以及它们对于不同数量prefrech的敏感程度，这些结果对于其他人的研究同样有所帮助，但无疑离不开作者细致的研究精神

- You have a keen perception and innovative spirit. NVLin is an important breakthrough for multi-GPU systems, you are keenly aware of the opportunity presented by the huge speed difference between NVLink and PCIe，which is the utilization of The Neighbor GPU Memory.And you evaluate the availability in scenarios where multiple GPU servers run various workloads by experiment.In fact, hierarchical design is common in computer architectures, and GPU vendors also offer UVM technology to solve the problem of memory bottlenecks. However, this technology is limited by the speed of the PCIe, resulting in reduced performance. Your innovative combination of the two, proposing the HUVM and designing the corresponding memory manager, is undoubtedly enlightening. In the system implementation, you fully implement the HUVM design concept, meanwhile, you take into account the dynamics of the GPU memory load in the system, then your memHarvester also dynamically adjusts to improve the utilization of overall GPU memory. In addition, you take advantage of the feature that the GPUs in the platform simultaneously connects the motherboard via PCIe and other GPUs via NVLink, then design the multi-path parallel prefetcher, finally overcomes the design-time challenges together with a variety of performance optimization techniques such as Large Page, prefetch, pre-eviction and etc. These reflect your deep professional knowledge. In Evaluation, you conducted control experiments on the system in multiple cases, which reflects the superiority of the system over other technologies. And in the process, you also analyze the different GPU memory usage of the applications selected in the experiment. These applications are common GPU applications that require a lot of memory.The results show the different memory work load of each application and the applications's different sensitivity to the amount of prefetch, which are equally helpful for other people's researches. This is inseparable from your meticulousness while treating the research.

==*== Questions for authors’ response
==-==    Specific questions that could affect your accept/reject decision.
==-==    Remember that the authors have limited space and must respond to
==-==    all reviewers.
==-== Markdown styling and LaTeX math supported.


1. What is the mechanism for setting up the Harvesting GPU and Yielding GPU? Will there be a distinction when scheduling GPU tasks? If the task is first scheduled to run on the Yielding GPU, will memHarvester work properly?
2. Users may use NVLink to run multi-GPU parallel tasks，which may cause NVLink to be busy, what impact will it have on memHavster?


==*== Comments for PC
==-== (hidden from authors)
==-== Markdown styling and LaTeX math supported.



==+== Scratchpad (for unsaved private notes)

==+== End Review

