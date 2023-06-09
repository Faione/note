# MMC

> MMC: Multi-Media Card, 实际是 与 SD (Secure Digital) 规格不同的存储介质, 但两者使用相同的接口和通信协议. uboot 中的 mmc 子系统则同时提供了对两者的支持

mmc 是一组命令, 提供了操作 uboot mmc subsytem 的能力

## Basic

`mmc list`: 查看可用的 mmc 设备, 嵌入式场景中一般通过 dts 及上电信号给出
`mmc dev`: 用来切换当前的 mmc 设备
`mmc info`: 查看当前 mmc 设备的详细信息

## Read & Write

`mmc read blk# cnt` 与 `mmc write blk# cnt` 是一对命令, 用于将 mmc 设备上指定 `<blk, cnt>` 的数据读取到 `addr` 对应的内存上, 这种读写方式比较原始, 但相对地也非常灵活, 通常用于加载操作系统到内存上