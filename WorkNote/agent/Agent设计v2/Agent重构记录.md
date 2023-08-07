## Api Server

- 目标
  - 对外提供 agent 的服务
- 实现方式
  - object 的api server 以方法注册到 api server中
  - 接收的所有请求，稍作处理后，均写到管道中
    - 以管道作为消息队列，降低并发执行的可能，提升应对并发的能力

## Agent Core

- 目标
  - agent 的核心运行过程，在一个协程中，集中地进行 object管理、监控与健康检查
- 实现方式
  - 由Manager、Collector、HeatBeat三个组件组成
    - 对应 对象管理、 对象监控、 健康检查
  - 从消息队列中取出消息，触发相应的控制流

## Manager 重构

- 目标：
  - 为每一个接入者构造一个抽象对象进行管理
    - guid注册
    - CRUDI
- 实现方式
  - 通过 client 完成 抽象对象 -> 实际对象 的转化与控制

## Controller 重构

- 并入 client，作为Manager的部分

## Collector 重构

- 目标
  - 监控一个对象，不断的收集(主动或被动)metric、log、trace数据，并写向通道中
实现方式
  - *对于一个对象的监控，会写向一个通道
    - 若存在多个消费者，则通过RPC 组播进行发送
    - 每一个对象，都会一个个单独的collector
  - 对于一个对象的监控信息会写向与其相关的所有通道中
    - 每增加一个消费者，就再增加一条通道，每条通道单独对于一个RPC进行单点通信
    - 存在一个单独的 collector 对所有监控进行管理
  - Jaeger Collector 特化为一个单独的 svc 

## HeatBeat 重构
