# Memory

uboot 中, 提供了 `md`, `mm`, `mw` 三个工具来直接操作物理内存

`md`: 打印目标内存(0x), 目标长度中的值
`mm`: 按一定步长从给定的起始地址开始打印内存中的值
`mw`: 修改内存中的值