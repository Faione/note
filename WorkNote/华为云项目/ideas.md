# VM场景的性能指标

虚拟网络设备
- 延迟
- 吞吐

vCPU资源
- cpu 时间片
- 调度延迟(offcpu -> oncpu)

内存资源
- 使用量

LLC资源
- 使用量
- llc路分配

磁盘IO资源
- 吞吐
- 延迟？


## 网络设备延迟感知

对于使用 virtio，基于 vhost 的虚拟网络设备
- sendmsg/recvmsg 延迟

## vCPU资源使用感知

vCPU time

## LLC 资源使用

resctrl

## 内存资源使用

memroy

## IO资源使用

block request

维度/层级 -> 信息 -> 架构
分层解释 + 示例 （总-分）

Shadow Thread(Link Thread)
- 同一个 task 在SMT/CMP上的副本，拥有相同的调度状态(同时调度运行，同时调度退出)
- 用于在SMT/CMP之间共享调度状态，基于perCPU调度来模拟全局调度
- shadow thread性质类似于 idle，idle 也可以作为一种 shadow thread
- shadow thread本身不占用，或占用较少cpu, 主要作用为一种 barrier, 以限制/隔离 SMT/CMP 上的资源竞争
- shadow thread也可跨越机器，在分布式环境中模拟全局调度

shadow thread 的目标是提供一种调度对象的抽象，最大程度地复用当前成熟的调度器，向调度器传递更丰富的信息协助调度，而不是制造各种复杂的调度器