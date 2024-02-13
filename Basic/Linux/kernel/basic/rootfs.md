# RootFS

- [RootFS](#rootfs)
  - [1. Ramfs](#1-ramfs)
    - [使用 Busybox 实现静态连接的软件环境](#使用-busybox-实现静态连接的软件环境)
  - [2. Alpine Image](#2-alpine-image)
    - [分离 vmlinux 与 initramfs](#分离-vmlinux-与-initramfs)
  - [3. Dqib](#3-dqib)
  - [4. Tips](#4-tips)


## 1. Ramfs

qemu虚拟机首先加载 bios 系统，进行初步的系统初始化后，按指定的命令跳转内核执行，内核在完成基本初始化工作后加载 initrd 来对内存及磁盘进行初始化，其主要目的是挂载真正的根文件系统，而当系统启动至 `ininramfs` 阶段时，就能够进行交互操作了，因此也可以仅制作一个 ramfs 来作为 `rootfs` 进行操作


### 使用 Busybox 实现静态连接的软件环境

参考[gist](https://gist.github.com/chrisdone/02e165a0004be33734ac2334f215380e)构建一个 ramfs，参考[initrd](http://m.blog.chinaunix.net/uid-22342877-id-1774614.html)中的讨论来了解更多关于 initrd 的内容。需要注意的是，initrd ramfs 同样是一个完整的文件系统，区别在于其实际操作的是内存而非磁盘，仅作为一个中间的过程

**1. 准备根目录**

根目录结构
- dev: 设备文件
- usr: 用户相关的可执行文件
- bin: 可执行文件
- sbin: 系统级可执行文件
- lib: 系统和应用程序使用的共享库文件，以及一些重要的内核模块, 对于动态链接的程序而言，通过`ldd`可以查看其依赖的动态链接库
- etc: 系统配置文件
- proc: 虚拟文件系统，包含了系统运行时的信息, 即使不创建，若开启了内核中的 Proc fs 选项，也会自动的创建
- tmp: 存放临时文件
- sys: 虚拟文件系统，提供了内核中的对象和设备的信息和接口
- var: 经常变化的文件，比如日志（/var/log）、队列（/var/spool）、缓存（/var/cache）等
- root: root用户（系统管理员）的家目录
- mnt: 挂载文件系统，如CD-ROM驱动器、外部硬盘等

```shell
# 准备一个目录，用来存放之后的根文件系统
$ mkdir ramfs && cd ramfs

# 创建各个子目录
$ mkdir dev usr bin sbin lib etc proc tmp sys var root mnt
```

**2. 安装基本软件环境**

将 CONFIG_PREFIX 设置为上述准备的目录，并将 `CONFIG_STATIC` 设置为静态链接
- bin、sbin、usr 中存放了相关的可执行代码程序，linuxrc 在早期linux中使用，通常作为引导程序

```shell
# 命令会将相关软件存放在 bin sbin usr 中
$ make install -j`nproc`
```

**3. 初始化etc基础配置**

etc中保存了系统中的一些基本配置文件
- /etc/inittab: 用于指导 init 如何管理系统的启动
- /etc/fstab: 指导如何自动挂载文件系统
- /etc/passwd: 存储账户信息
- /etc/group: 存储用户组信息
- /etc/shadow: 存储用户密码信息, 使用一个sha256摘要
- /etc/profile: 配置用户登入到系统后所执行的脚本

参考[rv_fs](https://doc-en.rvspace.org/VisionFive/Software_Technical_Reference_Manual/VisionFive_SWTRM/making_file_system.html)中进行各个配置，使用[cttyhack ](https://stackoverflow.com/questions/36529881/qemu-bin-sh-cant-access-tty-job-control-turned-off)来解决没有TTY情况下使用sh的问题

**4. 初始化init启动脚本**

/etc/inittab 定义了 init 的行为，其中 `sysinit` 将在系统启动之后执行 `/etc/init.d/hello` 脚本

```
::sysinit:/etc/init.d/hello
::respawn:-/bin/login
::restart:/sbin/init
::ctrlaltdel:/sbin/reboot
::shutdown:/bin/umount -a -r
::shutdown:/sbin/swapoff -a
```
`hello` 中通常需要挂载一些目录, 初始化设备等

```shell
# 按 /etc/fstab 中的设置挂载所有目录
mount -a
# 按 /sys 下找到设备，在 /dev 中创建对应的设备节点
mdev -s
# 指定 ttyS0 为默认登录使用的 tty
getty -L ttyS0 115200 vt100
```

**5. 打包**

`find .` 获取当前目录下的目录与文件列表，`cpio -o -H newc` 将获取的列表归档为 initramfs的cpio格式

```
find . | cpio -o -H newc | gzip > /home/user/Desktop/rootfs.cpio.gz
```

## 2. Alpine Image

`initramfs` 仅仅只是一个初级的软件环境，只能够进行较基础的调试，在虚拟磁盘上构建一个完整发行版的系统则更为通用
- 基于轻量级发行版 `Alpine` 构建虚拟机镜像

利用 [`alpine-make-vm-image`](https://github.com/alpinelinux/alpine-make-vm-image) 脚本制作 alpine linux镜像
- `example/test/packages` 定义了要额外安装的程序
- `./example/configure.sh` 定义了为 apline linux 初始化的脚本
- `-t`: 使能了 console=ttyS0
- `-m`: 配置了安装软件所使用的 mirror

```shell
./alpine-make-vm-image \
              -t -m "https://mirrors.ustc.edu.cn/alpine" \
              --image-format qcow2 \
              --image-size 5G \
              --boot-mode UEFI \
              --packages "$(cat example/test/packages)" \
              --fs-skel-dir example/test/rootfs \
              --fs-skel-chown root:root \
              --script-chroot \
              alpine-uefi.qcow2 -- ./example/test/configure.sh
```

### 分离 vmlinux 与 initramfs

使用 `qemu-nbd` 连接虚拟机磁盘并挂载

```shell
sudo qemu-nbd --connect=/dev/nbd0 alpine-uefi-2024-02-02.qcow2
```

查看磁盘分区

```shell
sudo fdisk -l /dev/nbd0
```

挂载boot分区

```shell
sudo mount /dev/nbd0p1 /path/to/boot

# 也可以挂载 linux 分区，再利用 chroot 来进行软件的安装
```

拷贝 vmlinux 与 initramfs，并复制 `startup.nsh` 中的内容作为 kernel cmd

Alpine Maker 脚本中默认的 rootfs label 为 `root` (line 557: `mkfs.$ROOTFS -L root $mkfs_args "$root_dev"`)
- 也可以再虚拟机启动之后，设置 rootfs label `e2label /dev/sda1 new-label`

## 3. Dqib

[Dqib](https://people.debian.org/~gio/dqib/)是预编译的 debian 系统作为最小软件环境，提供了不同架构的支持, 并预先分离出了 kernel 与 initrd来允许用户进行自定义，从而能够快速的搭建调试环境

dqib中提供了完整的支持，包括
- `kernel`: 虚拟机内核
- `initrd`: inital ram disk 引导系统
- `image.qcow2`: 包含完整软件的根文件系统
- `*key`: 用于连接虚拟机的密钥

debian登录管理器的初始用户密码为 `root root`


## 4. Tips

`.qcow2` 是稀疏格式的文件，因此可以使用 tar 的 `-S` 参数进行进一步的压缩


```shell
# compression: alpine-uefi.qcow2 -> box.img 
$ tar -zcvSf box.img alpine-uefi.qcow2

# decompression: box.img -> alpine-uefi.qcow2
$ tar -xf box.img
```