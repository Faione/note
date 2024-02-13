# Intro

Intel RDT(Resource Director Technology) 是一种硬件技术，用于在共享资源的多租户环境中管理和控制处理器缓存、内存带宽和其他系统资源的分配。通过使用 RDT，管理员可以更好地控制并限制不同负载对系统资源的使用，避免因为过度占用某个资源而导致性能下降或系统崩溃等问题。该技术适用于数据中心、虚拟化环境和云计算等共享资源的场景，它可以提高应用程序性能和系统的整体效率。RDT 技术已经被纳入了 Linux 内核中，可以通过各种软件工具进行配置和管理

## Env

启用 Intel RDT 需要硬件\软件上的支持, 其中硬件需要CPU提供相关的控制功能, 软件上则以来操作系统提供的接口


**CPU**

通过 `lscpu` 查看 CPU Flags 中是否支持 Intel RDT[^1]

**Kernel**

通常只需要内核版本在 `4.1` 及以上, 就能够使用 RDT 相关功能, 但需要注意的是, 相关功能必须在编译时开启

```shell
# check kernel config
sudo cat /boot/config-`uname -r` | grep CONFIG_X86_CPU_RESCTRL
```
同时也需要在 grub 配置文件中增加 `rdt=` 内核启动参数[^2]

```shell
# /etc/default/grub
GRUB_CMDLINE_LINUX="...rdt=cmt,mbmtotal,mbmlocal,l3cat,l3cdp,mba"

# update grub
sudo update-grub && sudo reboot
```

挂载 resctrl

```shell
$ sudo mount -t resctrl resctrl -o cdp,mba_MBps /sys/fs/resctrl
```

## Interface

RDT 主要提供了两套方式来进行资源控制, 其中一种是通过修改 CPU 上的 `MSR` 寄存器来实现相关功能, 与之配套的有一系列工具及用户库[^3], 另一种方式则是通过内核提供的用户接口[^1], 这种方式与 cgroup 十分类似



[^1]: [kernle_doc_aboubt_resctrl_subsystem](https://docs.kernel.org/arch/x86/resctrl.html)

[^2]: [kernel_parameters](https://docs.kernel.org/admin-guide/kernel-parameters.html)

[^3]: [intel_cmt_cat](https://github.com/intel/intel-cmt-cat)

[^4]: [zihao's_qos_agent](https://github.com/ChangZihao/QoS-Agent/blob/master/llcManager.go)