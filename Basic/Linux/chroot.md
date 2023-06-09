# chroot

能够切换当前的根目录, 并与真正的根目录隔离

## chroot 与 busybox 搭建沙盒

busybox 实际上是集成了各种基础工具的功能的工具，如使用 `busybox echo hello` 等同于 `echo hello`, 而通过链接，如 `ln -s busybox ls`, 可创建名为 `ls` 指向 `busybox` 的软链接，运行 `ls` 可以实现与 `ls` 相同的效果

```
# 创建bin目录
$ mkdir -p my_rootfs/bin

# 指定 -s 则仅会创建符号链接，使得切换根目录后，找不到链接的 busybox 而发生错误
$ sudo busybox --install my_rootfs/bin

# 切换根目录
$ sudo chroot my_rootfs /bin/sh
```
