# Play Kernel On Qemu

- [Play Kernel On Qemu](#play-kernel-on-qemu)
  - [1. Env Prepare](#1-env-prepare)
    - [Compiling Tools](#compiling-tools)
    - [Kernel SRC](#kernel-src)
    - [Busybox SRC](#busybox-src)
  - [2. Quick Start](#2-quick-start)
    - [VM Image](#vm-image)
    - [Kernel](#kernel)
      - [Simple Config](#simple-config)
      - [Alpine Config](#alpine-config)
      - [Compiling](#compiling)
    - [3. Emulating](#3-emulating)

## 1. Env Prepare

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


## 2. Quick Start

### VM Image

此处虚拟机镜像为一种可引导的存储介质
- 准备好rootfs的`.qcow2`(qemu copy-on-write)格式的存储介质
- cpio归档的 ramfs

### Kernel

get more guidience from [kernel doc](https://www.kernel.org/doc)

#### Simple Config

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

启用 rust 相关的配置

```
# enable rust support
General Setup
    -> Rust Support

# add rust samples
Kernel hacking
    -> Sample kernel code
        -> Rust samples
```

#### Alpine Config

[module_missing_when_change_kernel](https://unix.stackexchange.com/questions/579035/mounting-uuid-xxx-on-sysroot-failed-no-such-device-occurs-after-linux-kernel)

vmlinux 也可以自行编译，但需要注意的是，`initramfs` 中保存了部分内核模块，这些内核模块需要与内核匹配，自行编译的内核不建议加载这些模块(通常不会加载), 为此可以将模块都设置为 build-in, 即将所有的 `m` 配置修改为 `y`，来避免关键驱动缺失的问题
- 通过修改 initramfs 也能够解决上述问题，使用 `mkinitfs -o /boot/initramfs-virt <kernel-version>`

alpine linux 内核编译参考 [`linux-virt`](https://gitlab.alpinelinux.org/alpine/aports/-/blob/3.19-stable/main/linux-lts/APKBUILD?ref_type=heads) 的构建脚本, 通常可选择 [virt.x86_64.config](https://gitlab.alpinelinux.org/alpine/aports/-/tree/3.19-stable/main/linux-lts?ref_type=heads) 作为内核编译选项

#### Compiling

**简单编译**

kernel中预置了脚本，可以很方便将新内核打包生成 debian 包，用于在实际 debian 系统中的安装, 参考[debian_kernel_building](https://wiki.debian.org/BuildADebianKernelPackage)

```shell
# `LLVM=1` means enable LLVM
make LLVM=1 -j`nproc`

# make debian pkg, `O=output` will save all in ./output
make O=output -j`nproc` bindeb-pkg
```


**基于旧配置**

```shell
# 拷贝 config 到 output 目录下，再使用 olddefconfig 来基于旧 config 补全config
make O=output olddefconfig

# 使用最大核心数量-1进行内核编译
make O=output -j `expr $(nproc) - 1`
```

**其他**

```shell
# 生成`compile_commands.json`, 用于clangd
# -d 为内核 build 的目录
./scripts/clang-tools/gen_compile_commands.py -d output/ 
```

### 3. Emulating

使用 qemu 模拟虚拟机，append 传入额外的内核启动命令参数
- `nokaslr` 用来关闭内核地址空间随机化, 尤其是开启了内核地址空间随机时，方便进行debug
- `root=LABEL=rootfs` 指定启动dqib时使用 label 为 `rootfs` 的文件系统，而对于 alpine maker 来说, 默认的label是 `root`
  - 文件系统标签通常需要挂载文件系统之后才能获取，因此也可以指定 `root=dev/vda2` 这样的设备，使得直接从kernel boot rootfs
- `console=ttyS0` 指定了启动过程中要将信息输出到那个设备

**加载 initrd**

```shell
qemu-system-x86_64 \
  -machine pc -m 4G \
  -kernel arch/x86/boot/bzImage \
  -initrd /dqib/ramfs.cpio.gz \
  -nographic \
  -append "nokaslr console=ttyS0"
```

**加载 alpine** 

向虚拟机中增加了 `virtio-blk-pci` 和 `virtio-net-pci` 两个加速设备，后端分别对应虚拟机磁盘文件与宿主机的 br0 网桥

```shell
sudo qemu-system-x86_64 \
  -enable-kvm \
  -machine 'pc' \
  -cpu 'Nehalem' \
  -smp 4,cores=4 \
  -m 4G \
  -device virtio-blk-pci,drive=hd \
  -drive file=alpine-uefi.qcow2,if=none,id=hd \
  -device virtio-net-pci,netdev=net \
  -netdev bridge,br=br0,id=net \
  -kernel /home/fhl/alpine_temp/vmlinuz-virt \
  -initrd /home/fhl/alpine_temp/initramfs-virt \
  -nographic \
  -append "initrd=initramfs-virt root=LABEL=root rootfstype=ext4 modules=kms,scsi,virtio console=ttyS0"
```

**加载 dqib**


```shell
# Simple VM
$ qemu-system-x86_64 -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"

# KVM Accelert
$ qemu-system-x86_64 -enable-kvm -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"

# KVM and Using virtio Net
$ qemu-system-x86_64 -enable-kvm -machine pc -m 4G -drive file=/dqib/image.qcow2 -kernel arch/x86/boot/bzImage -initrd /dqib/initrd -netdev user,id=network0 -device virtio-net-pci,netdev=network0 -nographic -append "nokaslr root=LABEL=rootfs console=ttyS0"
```