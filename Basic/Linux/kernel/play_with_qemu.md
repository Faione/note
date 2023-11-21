# Play Kernel On Qemu

- [Play Kernel On Qemu](#play-kernel-on-qemu)
  - [Env Prepare](#env-prepare)
    - [software](#software)
    - [Kernel Source Code](#kernel-source-code)
    - [Busybox](#busybox)
  - [Quick Start](#quick-start)
    - [Kernel](#kernel)
      - [Config](#config)
      - [Compiling](#compiling)
      - [Emulating](#emulating)

## Env Prepare

### software

llvm, clang, lld

```shell
sudo pacman -S llvm clang lld
```

### Kernel Source Code 

download from [kernel org](https://www.kernel.org/)

### Busybox

Kernel本质上只是一个硬件资源管理程序, 并提供了一套标准接口来规范对硬件/抽象层的使用, 完整的系统应当还包含有其他的程序，来完成诸如shell等, Busybox提供了一系列基础程序功能，基于Busybox可以构建一个系统基础的软件环境

download from [buzybox](https://busybox.net/)


## Quick Start

### Kernel

get more guidience from [kernel doc](https://www.kernel.org/doc)

#### Config

```shell
# 使用LLVM 工具链来代替 GNU 工具链
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

```shell
# `10` meaning 10 threads
make LLVM=1 -j 10
```

#### Emulating

get filesystem image from [dqib](https://people.debian.org/~gio/dqib/)
- append 传入额外的内核启动命令参数, `nokaslr` 用来关闭内核地址空间随机化

```
KERNEL="/home/fhl/Workplace/c/linux-6.1.11/arch/x86/boot/bzImage"

qemu-system-x86_64 \
    -machine pc \
    -cpu Nehalem \
    -m 1G \
    -drive file=image.qcow2 \
    -device e1000,netdev=net \
    -netdev user,id=net,hostfwd=tcp::2222-:22 \
    -kernel $KERNEL \
    -initrd initrd \
    -nographic \
    -append "root=LABEL=rootfs console=ttyS0"
```

```
qemu-system-x86_64 \
    -enable-kvm \
    -machine pc \
    -cpu host \
    -smp cpus=4 \
    -m 8G \
    -drive file=image.qcow2 \
    -device e1000,netdev=net \
    -netdev user,id=net,hostfwd=tcp::2222-:22 \
    -kernel $KERNEL \
    -initrd initrd \
    -nographic \
    -append "root=LABEL=rootfs console=ttyS0"
```

```shell
# Simple VM
$ qemu-system-x86_64 -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"

# KVM Accelert
$ qemu-system-x86_64 -enable-kvm -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"

# KVM and Using virtio Net
$ qemu-system-x86_64 -enable-kvm -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -netdev user,id=network0 -device virtio-net-pci,netdev=network0 -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"
```

```shell
$ gdb vmlinux  -ex "target remote localhost:1234"
```

qemu-system-x86_64 -machine pc -m 4G -kernel arch/x86/boot/bzImage -initrd /dqib/initramfs.cpio.gz -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"

debian登录管理器的初始用户密码为 `root root`


[6.x_gdb_scripts_patch](https://lore.kernel.org/lkml/20230607221337.2781730-1-florian.fainelli@broadcom.com/T/#m89733097d8c7bdde834e9977292e09aaf3fd79c8)

[kernel_debugging](https://docs.kernel.org/dev-tools/gdb-kernel-debugging.html)

[debian_kernel_building](https://wiki.debian.org/BuildADebianKernelPackage)