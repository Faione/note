# Clive 

- [clive-source-code](https://github.com/fjballest/clive)
- [clive-unkernel-base-on-go](https://lsub.org/clive/)

## Clive设计理念

- Clive 是一种旨在在分布式和云计算环境中工作的操作系统。
- 主要设计准则是: 
  - 云计算场景中不应该存在软件栈, 应用程序和服务与能够让它们直接在硬件上运行的程序库一起被编译
  - 系统接口是按照类似 CSP 的风格设计的, 应用程序和组件通过通道进行通信，通道桥接网络、管道、和任何其他 I/O 组件