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

- Microkernel需要用户在使用时额外编译加载功能模块，而Unikernel允许用户预先将unikernel所需模块共同编译
  - 因此，unikernel app 能够提供小型、轻量、且高效的虚拟程序
- 宏内核系统中，程序与内核分别运行在不同的地址空间中，内核提供了底层硬件的抽象，并通过系统调用暴漏出来，而在之上的程序依赖这些系统调用以使用硬件资源让自己能够运行，而为支持各种各样的应用程序，宏内核需要在内部集成更多的功能，这导致宏内核十分臃肿
- 而在Unikernel中，应用程序与内核运行在同样的地址空间中，包括了app自生的指令与os级别的指令
  - 而为了构造这样的程序，unkernel使用专用的交叉编译方式，将从Library OS中选择的底层级方法与程序代码本身编译在一起，最终得到一个能独立运行并提供服务的镜像

### (4) Security in Unikernel

- 宏内核提供广泛的功能支持，对于单个程序而言，无可避免地有多余的成分，而这些都有可能称为攻击的对象，而在Unikernel中，用户只用选配程序运行所需要的模块功能，相比于宏内核，功能模块更少，更加稳定，同时，由于提供的模块少，攻击者很难对unikernel程序展开攻击，这极大增强了unikernel的安全性

### (5) Immutable Infrastructures

- 不变性意味着程序一旦运行就不在进行修改
  - 如果程序需要修改或进行更新，不应当大量更新代码或打补丁，而应该直接丢弃当前程序，运行新版本而取而代之
  - 采用"destroy and provision"思想主要是为保持应用程序的轻量级，而不是通过补丁的方扩张应用
    - mmutable Infrastructures的例子是 windows，系统在起初安装时非常简单，但随着版本更新，会增加各种各样的补丁，这些补丁不仅会带来程序体积的增加，增加程序的复杂性，还有可能导致新的bug与漏洞
  - unikernel旨在开发和部署，因此无法进行远程连接或调试bug，其在设计上是不可变的，同时，unikernel启动的快速性能允许进行无缝更新

### VM | Container | Unikernel

- virtual machine 基于 hypervisor 管理程序实现，hyperviser提供硬件资源的抽象，而运行在这些抽象资源的上的每个OS就是 virtual machine，程序依赖 vm 运行
- container 基于 namespace，cgroup 所提供的隔离机制，共享同一个内核，相比于 virtual machine 更轻量，但由于共享内核，安全上难以保证
- unikernel 同样基于 hypervisor 提供的硬件资源抽象，但不同的是，unikernel中的程序 以 library os 利用硬件资源，unikernel给予了程序直接运行在 hypervisor抽象层之上的能力
  - 在生产环境上仍然不够成熟

| Technology       | Pros                                                                                                                                                                        | Cons                                                                                                                                                                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Virtual Machines | - Allows deploying different operating systems on a single host<br> - Complete isolation from host<br> - Orchestration solutions available                                  | - Requires compute power proportional to number of instances<br> - Requires large infrastructures<br> - Each instance loads an entire operating system                                                                                         |
| Linux Containers | - Lightweight virtualization<br> - Fast boot times<br> - Ochestration solutions<br> - Dynamic resource allocation                                                           | - Reduced isolation between host and guest due to shared kernel<br> - Less flexible (i.e.: dependent on host kernel)<br> - Network is less flexible                                                                                            |
| Unikernels       | - Lightweight images<br> - Specialized application<br> - Complete isolation from host<br> - Higher security against absent functionalities (e.g.: remote command execution) | - Not mature enough yet for production<br> - Requires developing applications from the grounds up<br> - Limited deployment possibilities<br> - Lack of complete IDE support<br> - Static resource allocation<br> - Lack of orchestration tools |