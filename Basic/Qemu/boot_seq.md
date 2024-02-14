# Linux Boot

linux 系统启动是一个复杂的过程，同时在不同的场景之下，启动流程也有所不同，一下讨论均以 Qemu X86 虚拟机为例

[arch_linux_boot_process](https://wiki.archlinux.org/title/Arch_boot_process)

## System Installation

讨论系统启动的过程之前，有必要知道所谓 `安装系统` 究竟安装了些什么

以常规的系统安装为例，首先需要从要安装的系统的官方网站中获取系统镜像(Arch/Ubuntu/Alpine), 随后将其刻录到存储介质中，得到一个可引导系统的 "系统盘"，或安装盘""
- 所谓`系统镜像`并非最终实际安装的系统，而是提供了一个能够进行 "安装系统" 这一功能的基础系统
- BIOS 从 "安装盘" 中引导安装系统(Ghost系统), 这一系统中，集成了了网络/磁盘等驱动，并预先准备了常用软件/驱动的安装包

Ghost系统识别实际要安装系统的存储介质，首先然后按照所需的 Linux 引导方式进行分区, 以UEFI为例
- EFI分区: 即boot目录, 主要存放 Kernel 以及 initramfs
- 其他分区: 用来安装其他的用户软件，或有其他用途

Ghost系统挂载目标存储介质，创建初始的 rootfs，随后通过 `chroot` 类似的手段，依靠Ghost系统的支持完成目标系统的内核、系统软件的安装，以及初步的设置

以上工作完成之后，目标存储介质就是 bootable 了，BIOS能够对其进行引导以进入目标系统


### Kernel Installation

内核作为一种特殊的软件，其安装过程也有所不同，以源码中执行 `make install` 为例，内核安装主要进行了以下几个过程
1. 编译内核，以及所需要的内核模块
2. 拷贝内核镜像(vmlinuz)到 `/boot` 目录下(EFI分区)
3. 创建 initramfs, 并保存到 `/boot` 目录下
4. 更新系统引导加载器(GRUB)的配置文件，增加新内核的选项
5. 复制 `System.map` 到 `/boot` 中，此文件包含了内核的符号选项，通常用于调试
6. 将内核模块放置在 `/lib/modules/$(KERNELRELEASE)/` 目录中
7. 运行update-initramfs和update-grub这样的命令，以确保initramfs和GRUB配置最新

### initramfs

 `/usr/sbin/mkinitramfs` 会重新打包内核模块和 udev 配置文件等，生成一个新的 `initramfs` 文件（初始内存文件系统），并将其保存到 `/boot` 目录下

# 启动前流程

1. BIOS 进行硬件自查(POST), 挂载磁盘并跳转到 bootloader
2. bootloader 识别文件系统(UEFI), 寻找 vmlinux 和 initramfs，并将其加载到内存中
- 对于压缩的 vmlinux, 则会进行解压，而对于 initramfs, 会向内核提供 initramfs 所存放内存的物理地址, 如启动日志中的 `RAMDISK: [mem 0xbf6ed000-0xbffcffff]`
3. 内核启动
  - 创建 rootfs，并挂载到 /，解压 initramfs 到 /
  - 执行 init 进程(systemd/initd/openrc)

[linux启动流程](https://blog.csdn.net/Anhui_Chen/article/details/106988113)


使用 UEFI 的虚拟机，`vmlinux` 与 `initramfs` 通常保存在 boot 分区中，一般由 bootloader 进行加载，也可以从虚拟机磁盘中拷贝出来，从而通过 qemu cmd 直接指定
- alpine linux 中，同样在 boot 分区中，还有一个 `startup.nsh` 文件保存了 kernel cmd, linux 启动之后也会将启动命令保存到 `/proc/cmdline` 中


## Qemu X86 Boot

常规引导过程中，对于使用 UEFI 启动的系统，需要为其准备 UEFI 固件，以进行操作系统的引导


使用 `-kernel` 作为 qemu 启动参数时，可以认为是 qemu 完成了 bootloader 的工作，即将 kernel 与 initramfs 加载到内存中，但是实际上，这个过程还是由 SeaBIOS 与 qemu 写作完成的, [qemu_emulator_without_a_bootloader](https://stackoverflow.com/questions/68949890/how-does-qemu-emulate-a-kernel-without-a-bootloader)
