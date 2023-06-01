# Fat

fat 同样是一组 uboot 命令, 能够对使用 FAT 文件系统的存储设备进行读写, 使用时需要指定目标设备及分区`<interface> [<dev[:part]>]`

## Basic

`fatinfo`: 获取目标设备目标分区的信息
`fatls`: 类似 `ls`, 显示目标目录下的文件信息
`fatsize`: 类似 `size`, 显示目标可执行文件的分段信息

## Read & Write

`fatload`: 将目标文件加载到目标内存地址上, 内存地址为16进制且不能使用 0x
`fatwrite`: 将内存中指定位置, 大小的数据, 写入到目标文件中