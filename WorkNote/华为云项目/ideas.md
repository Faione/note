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
