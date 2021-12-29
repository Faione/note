# Agent 设计 V2
[设计参考](https://zhuanlan.zhihu.com/p/227859341)
## 1 引言

## 2 系统概述
### 2.1. 系统结构
Agent在整个系统中负责底层的支撑功能，主要为接收来自控制中心对所辖目标的日志拉取、资源调控命令，同时，又能够向Sponge发送注册、心跳，维护系统中所辖目标的状态   
而在设备上，agent 由三个微服务构成，分别是 agent service, repoter service 与 controller service, 功能上，agent service接入总线并于其他系统组件互通, 进行通信管理、接入管理、状态管理、控制方法管理、日志管理等功能，并同时提供sdk/cli，供接入对象使用, reporter service 与 controller service分别进行原始日志的收集与资源控制的执行，通过进程通信方式，如RESTful接口，与agent双向交互，而其他接入对象可以通过sdk实现注册、心跳等操作，并利用agent的扩展功能，实现opentracing。  

### 2.2. 系统功能
#### (1) Agent Service
- 初始化检查
- 注册发送
- 心跳发送
- 状态维护
- 方法注册
- 日志拉取
- 对象管理

#### (2) Reporter Service
- 监控抓取
- 消息格式化
- 启停开关

#### (3) Controller Service
- 方法注册
- 方法执行

当前工程修改: 区分模块，agent模块就是sdk，reporter、controller通过sdk进行调用，main方法里面，以线程的形式运行三个模块

## 3 程序设计详细描述 

## 4 公用接口程序设计说明 
