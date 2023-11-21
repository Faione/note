# Char Device

device, cdev, file_operations, inode 之间的关系

通过 `register_chrdev_region` 或 `alloc_chrdev_region` 注册的字符设备的设备号会在 `/proc/devices` 中出现, 然而此时仅仅只是将设备号分配出去

与设备操作强相关的是 cdev, 其可以通过 `cdev_alloc` 或 `cdev_init` 进行构造，其中 `ops` 字段包含了与此设备相关的 `file_operations`

设备驱动程序中只需要进行设备号的申请，并构造 cdev 即可，随后用户需要通过 `mknod` 创建一个 inode 并与 `/proc/devices` 中的此设备关联，此时 cdev 和 dev_t(设备编号) 将作为成员填充到 `inode` 数据结构中

其他程序通过读取 `inode` 可获取 cdev 等相关数据结构，而对于文件的`read`, `write` 等系统调用将通过 `file_operations` 定义的函数来完成


