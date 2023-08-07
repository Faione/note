# Logical Volume Manager

逻辑卷建立在磁盘设备上，且允许底层绑定不同类型的磁盘，使用 LVM 时，存储容量通常不是当前存储设备的最大值，需要先通过 LVM 工具修改大小，再应用到对应的文件系统上，才能够完全利用磁盘空间


```shell
# 扩展逻辑卷 `/dev/mapper/ubuntu--vg-ubuntu--lv`, 使用所有的剩余容量
$ sudo lvextend -l +100%free /dev/mapper/ubuntu--vg-ubuntu--lv

# 应用到ext4文件系统中
$ sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```

[linux_lvm](https://linux.cn/article-3218-1.html)