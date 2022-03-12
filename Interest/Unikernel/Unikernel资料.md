# Unikernel资料收集

- [unikernel项目汇总](http://unikernel.org/projects/)
- [unikernel摘要分析](https://github.com/cetic/unikernels) 



## 一、理论概念

- Anil Madhavapeddy 于 2013 年左右在一篇题为“Unikernels: Library Operating Systems for the Cloud”的论文中首次引入（Madhavapeddy 等人, 2013 年）
> Unikernels are specialized, single-address-space machine images constructed by using library operating systems
- "specialized" 意味着 unikernel 中只有一个程序
- "Single-address space"(单地址空间) 意味着Unikernel不区分用户态与核心态
- "Library operating systems" 是 unikernel 的核心

### (1) Microkernel

- 相比于宏内核，微内核通过将部分功能转移至用户态以减少内核代码
- 微内核保持内核较小，从而降低了内核中出现错误和缺陷的风险

**Monolithic vs Microkernel**

- 当前主流的OS给人的映像是总能够潜在地执行任何要求的方法，OS的设计者并不关心用户使用OS的意图，总是在内核中集成经可能多的功能
- 在使用微内核的场景中，OS本身会非常小，同时OS仅提供开箱即用的最基础的功能，用户需要根据自身的需求去安装额外的模块，同时，这些额外的功能模块均在用户空间中执行并于底层的微内核模块交互
- 由于模块之间的隔离性，微内核相比于宏内核更稳定，但同样地，由于许多功能并没有集成在内核中，这增加了用户使用OS的难度，同时，不同版本的功能模块的选择，无疑也增加了用户使用的成本

### (2) Library Operation System

- 程序所需要使用的内核与模块与程序本身运行在同一个地址空间中，并且程序能够直接调用内核级别的功能，而不需要进行系统调用
- Library OS 通过公开低级硬件抽象来提供增强功能，但因此难以支持大范围的硬件，即如果要构造一个完整的Library OS，内核必须使用为特定目标硬件编写的设备驱动程序进行编译，导致 Library OS 的可移植性非常差
- 当前虚拟化就技术已经通过公开虚拟化硬件驱动的方式，提供了底层硬件的抽象，这使得Library OS的只需要去支持通用的虚拟驱动而不是支持多种多样的硬件设备
- 这同样也为构建 unikernel 应用程序提供了基础
  - 将已测试的虚拟化技术与加载了hypervisor drivers的Library OS相结合，以实现完全可移植性

### (3) Unikernel

- Microkernel需要用户在使用时额外编译加载功能模块，而Unikernel允许用户预先与所需模块编译

