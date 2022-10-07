# md
## 虚拟化与容器
- 区别于管理程序虚拟化（Hypervisor virtualization），后者通过中间层将一台或多台独立的机器运行于物理硬件之上，而容器是直接运行在操作系统内核之上的用户空间
- 区别于传统虚拟化、半虚拟化,容器的运行不需要模拟层和管理层，而使用操作系统的系统调用接口
## 容器技术基础
- 容器得益于Linux内核特性，引入cgroup与namespace技术，使得容器与宿主机之间的隔离更加彻底
- 容器拥有独立的网络和存储栈，拥有自己的资源管理能力，这使得一台宿主机中的多个容器可以友好地共存
- 容器可以让多个独立的用户空间运行在同一台宿主机上
- 黄金模型: 一旦软件经过编译和一再测试，完美的构建成果就会被声明为黄金版本，不允许对它进一步更改，并且所有可分发的副本都是从此母片生成的
## Docker技术基础
### 核心组件
1. Docker Server & Client
2. Docker images
3. Registry：Docker Hub or Private
4. Docker Container
### Docker Server & Client
Docker是一种C/S架构的程序，用户通过Docker Client向Docker Server或本地Docker Daemon Process发送请求，Server或Daemon Process完成所有工作并返回结果  
>因此，Docker提供了一个命令行工具（Local Client）以及一整套RESTful API 
>Docker CLI、Docker Client就是对Docker服务/Daemon所提供的RESTful API进行请求的封装
### Docker Image
镜像是基于联合文件系统的一种层式结构
### Docker Container
#### 核心技术
Copy On Write
>fork()之后，kernel把父进程中所有的内存页的权限都设为read-only，然后子进程的地址空间指向父进程。当父子进程都只读内存时，相安无事。当其中某个进程写内存时，CPU硬件检测到内存页是read-only的，于是触发页异常中断（page-fault），陷入kernel的一个中断例程。中断例程中，kernel就会把触发的异常的页复制一份，于是父子进程各自持有独立的一份
[参考]https://blog.csdn.net/u012501054/article/details/902411246

