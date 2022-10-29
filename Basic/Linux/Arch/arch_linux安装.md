# 安装arch linux

[official](https://wiki.archlinux.org/title/Installation_guide)
[安装archlinux](https://zhuanlan.zhihu.com/p/112541071)

## 基本概念

### 硬盘分区

[archlinux硬盘分区](https://wiki.archlinux.org/title/Partitioning#Example_layouts)

todo

### 启动顺序

[archlinux启动顺序](https://wiki.archlinux.org/title/Arch_boot_process#Boot_loader)

todo


## ghost系统

[pacman清华镜像源](https://mirrors.tuna.tsinghua.edu.cn/help/archlinux/)

host烧录在镜像中，直接读取到内存中运行，具备基本的安装环境，在这个环境中，将目标硬盘(安装os的硬盘)作为设备进行挂载，并在其上进行linux内核及相关软件的安装

使用 `fdisk` 查存在的硬盘， 使用 `cfdisk` 进行硬盘分区， 使用 `mkfs.cvfat -F32`  


### 安装内核

[内核make过程](https://blog.csdn.net/a29562268/article/details/122903007)

使用 `pacstrap` 进行内核、相关软件工具的安装
- todo 分析软件行为
- 内核也是一个软件



## host系统

进行初始的设置，如语言、时间等，并最终设置uefi启动程序，之后进行reboot


# 安装桌面环境

[](https://zhuanlan.zhihu.com/p/405352705)