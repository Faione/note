# KVM Event

## Eventfd

linux 进程(task)之间可通过 [`eventfd`](https://man7.org/linux/man-pages/man2/eventfd.2.html) 进行通信

通过系统调用 `eventfd` 可创建一个 fd, 其在内核维护了一个 `uint64` 的计数器，用户程序可以通过返回的 fd 来对计数器的值进行读写
- `read`: 如果 count 不为 0，则将其值进行返回，否则阻塞当前 task 直到 count 不为 0, 随后将其读出并重设 count 为 0 
- `write`: 用户传入一个数值, 并与 eventfd object 当前值进行累加，若这次累加将会溢出，则阻塞当前 task 直到能够进行累加为止
- `poll`: 需要用户传入一个 poll table，eventfd 中的处理逻辑则为，调用 `poll_wait`, 触发传入的 pt 的 `_qproc` 逻辑，然后根据当前计数器的 count 值
  - count > 0: 置 `EPOLLIN`, 可以被读取
  - count == ULLONG_MAX: 置 `EPOLLERR`, 写入则会溢出
  - ULLONG_MAX - 1 > count: 置 `EPOLLOUT`，可以写入

开启 `EFD_SEMAPHORE` flag时，`eventfd` 可模拟信号量，即 `read` 用来将信号量减1，`write` 则用增加给的数量的资源
开启 `NON_BLOCKING` flag时，满足阻塞条件时会直接返回 `EAGAIN`, 让用户程序来决定轮询或者放弃


通过此系统调用实际上是创建了一个 `eventfd_ctx` 结构体保存 uint64 的计数器以及一个等待队列, 然后再基于此创建一个匿名inode, 并将 `eventfd_ctx` 保存在 `file->private_data` 中. eventfd 中 file_operations 的实现为`eventfd_fops`.

`task_struct` 中有一个可配置的 `in_eventfd` 字段， 若其为 1 则说明正在一个 `eventfd` 的处理上下文中，反之则不是，使用此字段可用来判断当前的处理是否存在嵌套

除提供给用户的接口外，eventfd还提供了一个内核接口 `eventfd_signal`, 相比于用户接口简化了逻辑，目的在于允许内核手动地向用户程序发送信号，此过程中，内核并不在生产者/消费者模型中，实际是内核与用户程序的一种通信机制

KVM 中 `ioeventfd` 和 `irqfd` 都是基于 `eventfd` 的通信机制，都需要用户程序预先申请一些 `eventfd`，并通过 `read`, `write` 操作 `eventfd` 来触发更复杂的逻辑的执行

## ioeventfd

ioeventfd 是一种 VM 向 Qemu 的通信机制，Qemu IO 相关线程通过 read eventfd 阻塞以等待 IO 事件, VM 写特殊的内存地址则会陷出到 KVM 中触发 IO 模拟并通过一系列回调到 `eventfd_signal` 以唤起阻塞的 Qemu IO 线程工作

Qemu 首先预注册好一些 eventfd，并将其与所需要的内存地址(PCIE/IO) 通过 ioctl [`KVM_IOEVENTFD`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/kvm_main.c#L4793) 向 KVM 请求分配 ioeventfd，随后便在 eventfd 上阻塞以等待相关事件.

KVM 收到 ioctl 请求后执行 [`kvm_ioeventfd`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/eventfd.c#L977) 来进行 ioeventfd 的分配过程，并通过返回值来告知 Qemu 是否分配成功，即对 Qemu 程序而言，只需要关注 eventfd 而 ioeventfd 完全在 KVM 中进行维护

实际过程中 KVM调用 [`kvm_assign_ioeventfd_idx`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/eventfd.c#L804) 进行分配，其中将 ioevetfd 作为 iodevice 并调用 `kvm_iodevice_init` 进行初始化，其 `kvm_io_device_ops` 的实现为 [`ioeventfd_ops`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/eventfd.c#L772)
- [`ioeventfd_write`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/eventfd.c#L748): 对 `ioeventfd` 进行写，会调用 `eventfd_signal` 以唤醒用户态的 Qemu

iodevice 的相关接口在 [`include/kvm/iodev.h`](https://elixir.bootlin.com/linux/v6.1.56/source/include/kvm/iodev.h)定义, 其中 `kvm_iodevice_write` 便会调用 ioevetfd 所注册的 `ioeventfd_write`，而 `ioeventfd` 在创建完毕之后，就会作为 `kvm_io_device` 保存到 `vcpu->arch.apic->dev` 字段中

x86 vmx 实现中，GuestOS 执行 IO 指令陷出到 KVM时会触发 [`handle_io`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/vmx/vmx.c#L5287) 回调，通过内部一系列回调之后，最终调用 `eventfd_signal` 来唤起注册了 ioeventfd 的 Qemu, 主要的回调如下: 
- [`ioeventfd_write`](https://elixir.bootlin.com/linux/v6.1.56/source/virt/kvm/eventfd.c#L748) 作为 `kvm_io_device` 的实现注册在 `vcpu->arch.apic->dev` 中
- [`write_mmio`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L7521) 注册在 [`write_emultor`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L7550)，而 `write_emultor` 实现了 [` read_write_emulator_ops`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L7485), 用来提供读写的模拟
- [`emulator_write_emulated`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L7672) 注册在 [`emulate_ops`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L8255) 中， 对 VM 写操作进行模拟, 其最后都会调用 `emulator_read_write`, 不同之处在于传入的 `read_write_emulator_ops` 是
- [`init_emulate_ctxt`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L8338) 执行时，将 `emulate_ops` 保存在 vcpu 中的 `ctxt->ops` 字段中
- `handle_io` 注册在 `kvm_vmx_exit_handlers` 中, 对 VM 陷出进行处理
- [`em_push`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/emulate.c#L1857) 注册在 [`opcode_table`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/emulate.c#L4615), 在 `x86_decode_insn` 完毕时对 push 相关指令进行模拟

[`vcpu_mmio_write`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kvm/x86.c#L7128) 中调用 `kvm_iodevice_write` 以执行对保存在其中的 `dev` 的 `write` 方法

GuestOS Exit -> `handle_io` -> `kvm_emulate_instruction` -> `x86_emulate_instruction` -> `em_push` -> `push` -> `segmented_write` -> `emulator_write_emulated` -> `emulator_read_write` -> `write_mmio` -> `vcpu_mmio_write` -> `ioeventfd_write` -> `eventfd_signal` -> Qemu


GuestOS -> handle_io -> kvm_emulate_instruction -> x86_emulate_instruction -> x86_decode_emulated_instruction -> x86_decode_insn -> kvm_queue_exception

em_push -> push -> segmented_write -> emulate_ops -> write_emulated -> emulator_write_emulated -> emulator_read_write-> -> emulator_read_write_onepage -> write_emultor -> read_write_emulator_ops write_emultor -> read_write_mmio -> write_mmio -> vcpu_mmio_write -> kvm_iodevice_write -> ioeventfd_write -> eventfd_signal -> Qemu

## irqfd

irqfd 是一种 Qemu 向 Guest OS 通信的机制，使得 Qemu 可以通过 write eventfd 来向 VM 注入中断

kvm_kernel_irqfd

Qemu用户程序预先申请 eventfd，并将其连同其他所需要的内容填充 `kvm_irqfd` 结构体中，再通过 KVM ioctl [`KVM_IRQFD`] 创建 `irqfd`， `irqfd` 执行中会对一系列关键数据进行初始化，最终使得用户对 eventfd 的写操作将触发 `irqfd_wakeup` 的执行

`kvm_irqfd_assign` 是分配 `irqfd` 的核心逻辑, 用来构造核心数据结构体 `kvm_kernel_irqfd`, irqfd 的一系列操作都依赖此结构体完成
1. 初始化 `irqfd` 的 `kvm_kernel_irqfd` 的基本内容
2. 从用户传入的 fd 中读取出 `eventfd`，并将其保存到 `irqfd` 中
3. 使用 `init_waitqueue_func_entry` 初始化 `irqfd` 的等待队列元素(wait_queue_entry)，将 `irqfd_wakeup` 作为此等待队列元素被唤醒时的 `wait_queue_func_t ` 回调逻辑
4. 使用 `init_poll_funcptr` 初始化 `irqfd` 的 poll table，将 `irqfd_ptable_queue_proc` 作为对 ptable `_qproc` 时的 `poll_queue_proc` 回调逻辑
5. 传入 eventfd `f.file` 与 irqfd 的 `pt` 作为 `vfs_poll()` 的参数并执行
- `vfs_poll()` 会调用 `file` 的 `poll` 方法，即 `eventfd_poll`
- `eventfd_poll` 首先会执行 `poll_wait`, 对于传入的 pt， 其 `_qproc` 被注册为 `irqfd_ptable_queue_proc`
- `irqfd_ptable_queue_proc` 核心就是将 `irqfd->wait` 插入到 eventfd 的等待队列中
- 回到 `eventfd_poll` 之后则会判断计数器 `count` 的取值，来决定返回值 `events`
- 如果为 `EPOLLIN` 则说明已经有用户程序发起了 eventfd 写的事件, 此时则调用 `schedule_work` 对 `irqfd->inject` 进行延迟处理
6. 返回值仅用于告知用户程序系统调用的执行是否顺利

`irqfd_wakeup` 核心在于唤起一次 `irqfd->inject` 的执行，`inject` 为一个 `work_struct`, 即一个延迟工作，其逻辑为函数 `irqfd_inject`，能够向 VM 中注入中断
- `irqfd_inject` 的核心通过调用 `kvm_set_irq` 来完成， 涉及到中断路由 `kvm_kernel_irq_routing_entry` 中相关回调的使用  

`eventfd_write` -> `waitqueue_active` -> `irqfd_wakeup` -> `irqfd_inject`