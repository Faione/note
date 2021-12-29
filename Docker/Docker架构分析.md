# Docker 架构分析
参考：
   - Docker源码分析
   - [Docker架构原理及简单使用](https://www.cnblogs.com/zhangxingeng/p/11236968.html#auto_id_17)
   - [Docker博客](https://zhuanlan.zhihu.com/p/89587030)
## 一、Docker基础模块
### (1) 总体架构
![image](/Docker/image/docker架构图.jpg)

### (1) 主要模块
Docker Client、Docker Daemon、Docker Registry、Grap、Driver、libcontainer、Docker  Container
### (2) 模块简介
1. Docker Client
   - Client是与Docker Daemon建立通信的最佳途径
   - 用户通过Docker Client 发起容器管理的请求，请求最终发往Docker Daemon
2. Docker Daemon
   - 具备Server功能，接受来自Docker Client的请求
   - 对请求的处理能力，Daemon内所有任务有Engine完成，每项工作以Job的形式存在
      - Engine
   - 用户发出下载容器镜像的请求，则Daemon会创建一个“pull”job，运行时从Docker Registry下载镜像，并通过graphdriver存储镜像到Graph中
3. libcontainer
   - 独立的容器管理解决方案，涉及namespaces、cgroups及capabilities等Linux特性
   - libcontainer抽象了这些Linux内核的特性，并提供完整、明确的接口给Docker Daemon

## 二、Docker Client
### (1) 概述
1. 用户通过可执行文件docker作为Docker Client发起Docker容器的管理请求
2. 主要通信方式（创建socket以监听通信）
   - tcp://host:port
      - 实验: 修改docker配置文件以启动tcp访问(/lib/systemd/system/docker.service)
         - [Docker Engine API](https://docs.docker.com/engine/api/v1.41/)
         - 使用 docker -H host:ip command 可以将请求发送至远程docker
   - unix://path_to_socket(默认)
     - UNIX域协议，用于单节点上的进程通信，其数据报服务可靠的
     - UNIX与TCP相比，仅复制数据而不执行协议处理，单节点上速度是TCP的两倍(1/7?)
     - [go语言unix通信实现参考](https://blog.csdn.net/qq_33399567/article/details/107691339)
   - fd://socketfd 
      - file descriptor 文件描述符, ubuntu下使用
      - [参考](https://www.jianshu.com/p/45e944a53152)
      - containerd, docker底层的替代

1. 生命周期
   1. 用户通过docker可执行文件创建Docker Client并发送容器管理请求
      - 也可以使用各种语言的Docker SDK创建Docker Client, 进行请求
   2. Docker Daemon接收请求并处理
   3. Docker Client接收请求的响应，并简单处理(打印以通知用户)
   4. Docker Client生命周期结束，用户可再次通过可执行文件docker创建Docker Client与发送请求

[Docker Client执行流程](https://www.cnblogs.com/davidwang456/articles/9579573.html)

### (2) 源码详解

## 三、Docker Daemon
### (1) 概述
1. 主要作用
   - 接收并处理 Docker Client 发送的请求
   - 管理所有的 Docker 容器
2. 子系统组成
   - Docker Server、Engine、Job
3. 生命周期
   - 通过二进制文件 docker 启动，通过 option "-d" 区分启动Client与Daemon
   - Daemon在后台启用Server，用以处理Client发送的请求
   - 接收请求以后，Server通过路由的分发与调度，找到相应的Handler来处理请求

### (2) Docker Server
- 作用
   - 专门服务与Docker Client，接收并调度分发Docker Client的请求
   - Docker Server 本身也是job（serverapi），随docker的启动而启动

- 工作流程(与go server相同)

   1. Docker server首先基于 gorilla/mux 库，创建 mux.Router路由器, 提供请求路由功能  
   2. 之后，Docker server 向mux.Router中添加有效的路由项(RESTful风格)，路由项由HTTP请求方法、URL以及Handler组成
   3. 对于Docker Client的每次请求, Docker Server均会创建一个 goroutine 来处理
   4. 在 goroutine 中，Docker Server首先读取请求内容，并进行解析，匹配响应的路由项，最后调用相应的Handler进行请求的处理与结果的回写
  
### (3) Engine
- 作用
   - Docker架构中的运行引擎，核心模块
   - 存储大量的容器信息，管理大部分Job的执行, Docker中大部分任务都需要Engine协助, 通过Engine匹配相应的Job完成Job的执行
   - 内部定义了一个handlers对象(map)，存储众多特定Job的处理方式handler(每组键值对就是Job)
   - 接管Docker Daemon的某些特定任务，如Daemon进程需要退出时，Engine负责完成退出前的所有善后工作

### (4) Job
- 作用
   - Engine内部最基本的工作执行单元
   - 存在名称、运行时参数、环境变量、标准输入输出、标准错误及返回状态等 
   - Job在被定义完毕之后，需调用Run()执行(类似于Unix进程）
### (5) 源码详解

## 四、Docker Registry
### (1) 说明
Docker Registry是一个存储Docker Image的仓库
   - 公有仓库: Docker Hub
   - 私有仓库: 用户自行搭建
      - Docker Registry配置(/etc/docker/daemon.json)
Docker Daemon提供三种与Registry交互的操作
   - search: 搜索镜像
   - pull: 拉取镜像
   - push: 推送镜像

## 五、Graph
### (1) 说明
Graph是容器镜像的保管者
   - Docker Registry中下载的镜像
   - 用户构建的镜像

### (2) 存储方式
支持多种镜像存储方式: aufs、devicemapper、Btrfs
- aufs
   - 一种联合文件系统
   - 聚合多个文件系统，以目录的形式呈现
      - 目录是统一的，而文件系统不同，这就是Union的意义 
   - COW机制
>fork()之后，kernel把父进程中所有的内存页的权限都设为read-only，然后子进程的地址空间指向父进程。当父子进程都只读内存时，相安无事。当其中某个进程写内存时，CPU硬件检测到内存页是read-only的，于是触发页异常中断（page-fault），陷入kernel的一个中断例程。中断例程中，kernel就会把触发的异常的页复制一份，于是父子进程各自持有独立的一份  
[参考]https://blog.csdn.net/u012501054/article/details/902411246

## 六、Driver
### (1) 说明
通过Driver定制Docker容器的运行环境
   - 存储方式、网络环境、执行方式
Driver的实现可分为三类: 
   - graphdriver
   - networkdriver
   - execdriver
## 七、Libcontainer
### (1) 说明
- 使用go语言设计实现的程序库，能够不依靠任何依赖，直接访问内核中与容器相关的系统调用
提供了一套标准的接口来满足上层对容器管理的需求
   - namespace的使用
   - cgroup的管理
   - rootfs的配置启动
   - linux capability权限集
   - 进程运行的环境变量配置

