# Kvm

KVM是linux中的一个模块，可内嵌到linux中，也可作为单独的模块。不同体系结构中虚拟化的实现各不相同, 而 KVM 需要为上层应用提供一个较为稳定的入口，因此 KVM 源代码会包括两个部分，其中一部分在 `virt/kvm` 中，包含 KVM 模块中较通用的逻辑，特别是与上层应用交互的ioctl接口部分，其次则是各个体系结构目录下的 `arch/*/kvm`, 包含有各个体系结构中虚拟化实现的具体逻辑，例如执行vcpu的逻辑

## Common API

> ioctl允许用户定义不同的 ioctl 号以绑定不同的功能，是一种超级系统调用

KVM 是一个内核模块，除对硬件初始化外，还为上层应用提供服务，应用程序通过 ioctl 系统调用来使用这些服务, 在用户看来，KVM模块是一个 misc 设备，通常在 `/dev/kvm` 路径下

而在 KVM 模块中，此设备为 [`kvm_dev`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L5085)，作为misc设备，其 `file_operations` 实现为 [`kvm_chardev_ops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L5079), 其中定义了 ioctl 入口函数 [`kvm_dev_ioctl` ](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L5039), 根据传入的 ioctl 号的不同，来执行 `KVM_GET_API_VERSION`、`KVM_CREATE_VM` 等通用操作，而若 ioctl 不在通用选项中，则会转而调用 [`kvm_arch_dev_ioctl`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L5073) 来触发在各个体系中的特殊功能。所有的 KVM ioctl 号定义在 `include/uapi/linux/kvm.h` 中

通过 `/dev/kvm` 可以进行VM的创建，所得到的是一个 VM 描述符，实质是一个匿名 inode， 其相应的 `file_operations` 实现为 [`kvm_vm_fops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L4983), 其中定义了 ioctl 的入口函数 [`kvm_vm_ioctl`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L4711), 用户在获取到 VM 描述符后，能通过 ioctl 来为 VM 创建 vcpu、mem等资源

通过 `KVM_CREATE_VCPU` 能够创建一个 vcpu，与VM类似, vcpu在KVM中也是一个文件描述符, 其 `file_operations` 为 [`kvm_vcpu_fops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L3860)，其 ioctl 入口为 [`kvm_vcpu_ioctl`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L4075), 其他KVM设备也通过类似的机制实现

|                                          file_operations                                           | ioctl | desc  |
| :------------------------------------------------------------------------------------------------: | :---: | :---: |
|    [`kvm_vcpu_fops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L3860)    |       |       |
| [`kvm_vcpu_stats_fops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L4043) |       |       |
|   [`kvm_device_fops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L4394)   |       |       |
|  [`kvm_vm_stats_fops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L4681)  |       |       |
|   [`kvm_chardev_ops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L5079)   |       |       |
|  [`stat_fops_per_vm `](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L5611)  |       |       |

## Run VM in VCPU

每个qemu虚拟机都是一个进程:
1. qemu进程启动后就创建 VM 以及 VCPU 等及其他设备，开启 KVM 加速时，部分 KVM 支持的设备，如 vCPU 都会通过 ioctl 请求 KVM 来进行创建
2. 完成设备的创建后，对于 vCPU, qemu进程会为每个 vCPU 启动一个线程
3. vCPU 线程的核心是一个死循环，其中会利用创建号的 vCPU fd 请求 KVM 执行 ` KVM_RUN`,
4. 进入到内核态的 KVM 后，会调用体系结构对应的 [`kvm_arch_vcpu_ioctl_run`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L11161), 其中会根据不同体系结构虚拟化实现初始化好 Guest OS 的运行环境, 再调用 [`vcpu_run`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L11020) 来启动vCPU
5. `vcpu_run` 中同样是一个死循环，核心函数为 [`vcpu_enter_guest`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L10572), 其在进行各项检测之后，开启一个死循环，并通过 [`static_call(kvm_x86_vcpu_run)(vcpu)`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L10833) 进入 vCPU 执行


`static_call` 宏包裹允许被包裹的函数动态变化，包裹 `kvm_x86_vcpu_run` 的原因在于 x86 中实现虚拟化的手段多样，Intel VMX 的实现中，实际为一段汇编 [`__vmx_vcpu_run`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/vmx/vmenter.S#L46), 其会保存当前 Host OS 的上下文并切换到 Guest OS 上下文执行

## VM Exit

执行用户指令的 VM 将保持在 Guest OS 中运行，当其执行到敏感指令或特权指令时，会由于特权级的限制而陷出到 Host OS，当然，陷出也涉及 Host OS上下文的恢复。按照进入的顺序，陷出通常首先在 KVM 中进行处理，核心逻辑在 [`__vmx_handle_exit`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/vmx/vmx.c#L6332) 实现，其预定义了一个函数数组 [`kvm_vmx_exit_handlers`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/vmx/vmx.c#L6008), 声明了 KVM 中能够处理的陷出事件，若无法被 KVM 处理则进入[`unexpected_vmexit`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/vmx/vmx.c#L6493)

导致这种情况的原因通常是Guest OS对KVM无法模拟的设备的操作，此时 KVM vCPU 相关的循环会结束并返回到用户态qemu进程的循环中，完成相关的设备模拟后，重复 VM enter 流程回到 Guest OS 继续运行


[linux虚拟化之Qemu](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzU1MDkzMzQzNQ==&action=getalbum&album_id=1474923257362464769&scene=173&from_msgid=2247484478&from_itemidx=1&count=3&nolastread=1#wechat_redirect)