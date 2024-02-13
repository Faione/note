# Play Kernel On Qemu

- [Play Kernel On Qemu](#play-kernel-on-qemu)
  - [Env Prepare](#env-prepare)
    - [Compiling Tools](#compiling-tools)
    - [Kernel SRC](#kernel-src)
    - [Busybox SRC](#busybox-src)
  - [Quick Start](#quick-start)
    - [FileSystem](#filesystem)
      - [Dqib](#dqib)
      - [Simple Ramfs](#simple-ramfs)
    - [Kernel](#kernel)
      - [Config](#config)
      - [Compiling](#compiling)
      - [Emulating](#emulating)

## Env Prepare

### Compiling Tools

llvm, clang, lld

```shell
sudo pacman -S llvm clang lld
```

### Kernel SRC

download from [kernel org](https://www.kernel.org/)

### Busybox SRC

Kernel本质上只是一个硬件资源管理程序, 并提供了一套标准接口来规范对硬件/抽象层的使用, 完整的系统应当还包含有其他的程序，来完成诸如shell等, Busybox提供了一系列基础程序功能，基于Busybox可以构建一个系统基础的软件环境

download from [buzybox](https://busybox.net/)


## Quick Start

### FileSystem

#### Dqib

可以使用预编译的 debian 系统作为最小软件环境, download from [dqib](https://people.debian.org/~gio/dqib/)
- debian登录管理器的初始用户密码为 `root root`

dqib中提供了启动一个虚拟机的完整支持，包括
- `kernel`: 虚拟机内核
- `initrd`: inital ram disk 引导系统
- `image.qcow2`: 包含完整软件的根文件系统
- `*key`: 用于连接虚拟机的密钥

#### Simple Ramfs

实际上操作一个系统不需要以上完整的软件环境，可以基于 Busybox 构造一个 initrd ramfs 来简单地进行操作
- qemu虚拟机首先加载 bios 系统，进行初步的系统初始化后，按指定的命令跳转内核执行，内核在完成基本初始化工作后加载 initrd 来对内存及磁盘进行初始化，其主要目的是挂载真正的根文件系统

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

### Kernel

get more guidience from [kernel doc](https://www.kernel.org/doc)

#### Config


相关配置项
- CONFIG_GDB_SCRIPTS: enable
- CONFIG_DEBUG_INFO_REDUCED: off
- CONFIG_FRAME_POINTER: enable if exists
- CONFIG_RANDOMIZE_BASE: disable


```shell
# 生成默认配置
make defconfig

# 可使用 LLVM 工具链来代替 GNU 工具链
make LLVM=1 menuconfig
```

about rust

```
# enable rust support
General Setup
    -> Rust Support

# add rust samples
Kernel hacking
    -> Sample kernel code
        -> Rust samples
```

#### Compiling

kernel中预置了脚本，可以很方便将新内核打包生成 debian 包，用于在实际 debian 系统中的安装, 参考[debian_kernel_building](https://wiki.debian.org/BuildADebianKernelPackage)

```shell
# `LLVM=1` means enable LLVM
make LLVM=1 -j`nproc`

# make debian pkg, `O=output` will save all in ./output
make O=output -j`nproc` bindeb-pkg

# 生成`compile_commands.json`, 用于clangd
```

#### Emulating

使用 qemu 来模拟一个虚拟机
- append 传入额外的内核启动命令参数, `nokaslr` 用来关闭内核地址空间随机化, `root=LABEL=rootfs` 指定启动时使用 label 为 rootfs 的文件系统， `console=ttyS0` 指定了启动过程中要将信息输出到那个设备

```shell
# Simple VM
$ qemu-system-x86_64 -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"

# KVM Accelert
$ qemu-system-x86_64 -enable-kvm -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"

# KVM and Using virtio Net
$ qemu-system-x86_64 -enable-kvm -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -netdev user,id=network0 -device virtio-net-pci,netdev=network0 -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"
```

**只加载 initrd**

```shell
qemu-system-x86_64 -machine pc -m 4G -kernel arch/x86/boot/bzImage -initrd /dqib/ramfs.cpio.gz -nographic -append "nokaslr console=ttyS0"
```