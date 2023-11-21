# Syscall

syscall本身通过注册中断来实现，传统的实现中依赖 `int 0x80`

用户程序能够通过 ABI 对动态链接库进行调用，系统调用也可以认为是一种 ABI，是 Linux Kernel 提供给用户程序对其所管理的资源进行操作的方式

与通常 ABI 不同的是，操作内核资源涉及到特权级的切换，并且由于系统调用的过程发生在内核之中，因而程序运行的上下文也不同于函数调用的上下文，涉及地址空间及栈的切换

这种差异也使得系统调用机制的实现与函数完全不同，早期x86平台的实现中，系统调用是通过注册 `0x80` 中断实现，标准库中在将系统调用的参数准备完毕之后，便调用 `int 0x80` 唤起内核处理

现代 CPU 使用 `sysenter/sysexit` 指令来唤起系统调用，这些指令可以认为是 64bit 的 `int 0x80`, 同时在性能表现上也更好

| enter | exit  |       |  |
| :---: | :---: | :---: ||
| int 0x80 |  iret   |  old(32bit)  |
| sysenter | sysexit | Intel(64bit) |
| syscall  | sysret  |  AMD(64bit)  |

[syscall_vs_int](https://blog.packagecloud.io/the-definitive-guide-to-linux-system-calls/)
[intel_x86_vs_x64_syscall](https://stackoverflow.com/questions/15168822/intel-x86-vs-x64-system-call)
[kernel_syscalls](https://wenfh2020.com/2021/09/05/kernel-syscall/)

## 内核实现

### 特权级切换

传统系统调用是一种软件中断, 操作系统初始化过程中会完成对应中断向量的注册, 当 `0x80` 中断触发时，此中断描述符中设置了应当切换的特权级(ring0)，以及中断处理函数地址

syscall指令则需要与两个重要的MSR寄存器协同工作，其中
- `MSR_LSTAR`: 保存系统调用的入口地址
- `MSR_STAR`: 保存用户和内核代码段和数据段的选择子(地址空间切换)
syscall指令所做的事情就是
- 将pc设置为 `MSR_LSTAR` 寄存器中的值, 把用户程序的下一条指令保存在 RCX 寄存器中
- 从 `MSR_STAR` 读取到代码段与栈段的选择子，填充到当前寄存器中

sysret指令则相反
- 从 `MSR_STAR` 获取用户的代码段与栈段的选择子
- 将 RCX 寄存器中的值覆盖到 RIP 中
- 恢复 EFLAGS 

[x86_64_特权级](https://zhuanlan.zhihu.com/p/655185121)

### 上下文保存与恢复

系统调用中需要进行上下文的保存和恢复，其主要是对进入内核态之前，用户态的cpu状态，地址空间(寄存器)进行保存，并在完成系统调用之后，恢复这些寄存器

不同体系结构下有不同的实现，x86中通过 [`entry_SYSCALL_64`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/entry/entry_64.S#L87) 汇编完成了这些功能，注意指令 `swapgs`, 其执行之后就进入了内核的地址空间中，将寄存器保存到栈上之后，会唤起 `do_syscall_64` 函数来执行系统调用，而当从其中返回时，就开始恢复用户态的上下文，较早的实现为 [`swapgs_restore_regs_and_return_to_usermode`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/entry/entry_64.S#L615) 这段汇编，其会从栈上恢复保存的寄存器值，并通过 `swapgs` 切换到用户地址空间，随后通过 `iret` 切换特权级并返回

较新的实现中则通过 [`syscall_return_via_sysret`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/entry/entry_64.S#L198) 恢复上下文并调用 `sysretq` 进行返回

### 系统调用注册及初始化

#### 注册

系统调用函数实质上与内核中的普通的功能函数没有什么不同，但考虑到其需要对外提供API, 同时又需要在syscall过程时进行分发，因此需要进行集中管理，内核提供了一组宏来来将定义好的内核函数注册为到系统调用中

通过 [`SYSCALL_DEFINEx`](https://elixir.bootlin.com/linux/v6.1.56/source/include/linux/syscalls.h#L217) 宏用来注册系统调用，其会根据所注册函数的名称，生成 `__do_sys_`, `sys_`, `__se_sys` 等符号作为系统调用的入口

系统调用需要统一分发，因此需要用一个数据结构存储所有的系统调用入口，内核中使用 `sys_call_table` 保存所有的系统调用的入口函数，组织为一个数组，下标即是系统调用号，相应的，内核中依赖一系列手段来对其以及整个系统调用相关的基础设施将进行初始化

编译期间，内核会根据代码及[配置](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/entry/syscalls/syscall_64.tbl)生成 `<asm/syscalls_64.h>` 临时头文件, 其中就包含了所有的 [`sys_call_ptr_t`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/include/asm/syscall.h#L19), 而系统调用号和对于的入口地址都在配置中声明

#### 初始化

内核主函数 [`start_kernel`](https://elixir.bootlin.com/linux/v6.1.56/source/init/main.c#L993) 中会调用 `trap_init`, 其在不同体系结构中的实现各不相同，x86 中 [`trap_init`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kernel/traps.c#L1458) 在最后会进行 [`cpu_init`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kernel/cpu/common.c#L2292)并调用 [`syscall_init`](https://elixir.bootlin.com/linux/v6.1.56/source/arch/x86/kernel/cpu/common.c#L2061)对syscall相关的基础设施进行初始化
1. 设置 MSR_STAR 寄存器，将用户代码的CS 和 啮合代码的 CS 写入其中
2. 将 `entry_SYSCALL_64` 地址写入到 MSR_LSTAR 寄存器中
3. 对于需要模拟的 `IA32` 进行相关初始化
4. 设置 MSR_SYSCALL_MASK 寄存器，定义执行系统调用时应当被清除的EFLAGS寄存器中的标志

### 用户态

用户态代码库中会封装各个系统调用的参数为一个函数，而其内部则会通过 `syscall` 或 `int` 指令陷入到内核, 并在完成之后回到用户代码继续执行，其执行的主要过程如下

entry_SYSCALL_64 -> inner:entry_SYSCALL_64_safe_stack -> inner:entry_SYSCALL_64_after_hwframe -> do_syscall_64 -> syscall_return_via_sysret -> inner:entry_SYSRETQ_unsafe_stack -> inner:entry_SYSRETQ_end

do_syscall_64 -> do_syscall_x64 -> `regs->ax = sys_call_table[unr](regs)`

发生系统调用时，ax寄存器保存了系统调用号，而在系统调用完成以后，ax保存的是系统调用的返回值，此时在 pt_regs 中由一个额外的字段 orig_ax 保存了系统调用号，以使得当系统调用需要重新执行时，能够知道当时的系统调用号