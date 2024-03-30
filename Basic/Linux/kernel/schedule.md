# Linux调度

- [Linux调度](#linux调度)
  - [一、Core调度](#一core调度)
    - [(1) 时钟中断-scheduler\_tick](#1-时钟中断-scheduler_tick)
    - [(2) 抢占标记-resched\_curr](#2-抢占标记-resched_curr)
    - [(3) 执行调度-schedule](#3-执行调度-schedule)
      - [(4) 切换时机](#4-切换时机)
    - [(5) 任务选择-pick\_next\_task](#5-任务选择-pick_next_task)
    - [(6) 任务取出-put\_prev\_task](#6-任务取出-put_prev_task)
    - [(6) 任务取出-set\_next\_task](#6-任务取出-set_next_task)
    - [(6) 任务入队-enqueue\_task](#6-任务入队-enqueue_task)
    - [(7) 任务出队-dequeue\_task](#7-任务出队-dequeue_task)
    - [(8) 任务移动-sched\_move\_task](#8-任务移动-sched_move_task)
    - [(9) 优先级调整-set\_user\_nice](#9-优先级调整-set_user_nice)
  - [二、Sched Class调度](#二sched-class调度)
    - [非抢占调度-STOP/FIFO](#非抢占调度-stopfifo)
    - [抢占式调度-RR/FAIR/BATCH/IDLE](#抢占式调度-rrfairbatchidle)
  - [其他](#其他)
    - [Preemption modes](#preemption-modes)
    - [HZ](#hz)


Sched Class是Linux中实现调度策略的关键机制。[`sched_class`](https://elixir.bootlin.com/linux/v6.6.20/source/kernel/sched/sched.h#L2231)结构体是这一机制中的核心，其中定义了实现调度类所需要的所有函数，而通过[`DEFINE_SCHED_CLASS`](https://elixir.bootlin.com/linux/v6.6.20/source/kernel/sched/sched.h#L2317)宏可以定义一个调度类.

## 一、Core调度

[core调度](https://docs.kernel.org/admin-guide/hw-vuln/core-scheduling.html)

调度器设计时需要参考不同的软硬件环境与实际需求，内核通过提供`sched_class`这一层抽象来简化调度器的设计。理解调度这一复杂过程，可以从宏观角度入手，而在core.c中就定义了大部分的宏观操作代码。

### (1) 时钟中断-scheduler_tick

>> linux中定义了 `HZ`, 用来设置设置系统定时器每秒的时钟中断次数，而在内核中会维护一个jiffies变量，记录当前时钟中断的次数, 显然使用jiffies / HZ能够计算得到一个具体的时间值

在Linux中，驱动调度的核心机制是时钟中断，内核在编译时会确定一个中断间隔，并注册相应的中断处理函数，对于timer时钟中断的处理逻辑大致可以分为以下几个步骤
1. 更新 wall_time
2. 更新进程的时间，设置抢占标记
3. 根据抢占标记，来选择执行schedule函数
4. 返回用户态执行

当时钟中断发生时，通常会打断当前任务的执行，从用户态/内核态上下文切换到中断处理函数的执行中。APIC timer的中断处理函数为[`sysvec_apic_timer_interrupt`](https://elixir.bootlin.com/linux/v6.6.21/source/arch/x86/kernel/apic/apic.c#L1076)，其中涉及调度相关的核心部分为[`update_process_times`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/time/timer.c#L2064)，包含两个部分，其中[`account_process_tick`](https://elixir.bootlin.com/linux/v6.6.20/source/kernel/sched/cputime.c#L487)用来更新任务的时间信息，如记录user\sys不同态的时间，而常用到的CPU利用率便基于这些记录。

[`scheduler_tick`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L5640)则与调度逻辑密切相关。除了通用的逻辑外，还会读取当前任务的调度类信息，并执行`task_tick`来触发对应调度类的调度逻辑，其中就涉及到抢占任务的判断。


### (2) 抢占标记-resched_curr

值得注意的是，内核中将抢占的逻辑分为了`抢占决策`与`抢占执行`两部分，而`task_tick`一般只进行抢占决策，并调用[`resched_curr`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/sched/core.c#L1041)来设置thread_info中的标志位以及preempt_count信息，之后便中断的后续部分执行。

```c
struct thread_info {
	unsigned long		flags;		/* low level flags */
	unsigned long		syscall_work;	/* SYSCALL_WORK_ flags */
	u32			status;		/* thread synchronous flags */
```

### (3) 执行调度-schedule

中断处理的[`irqentry_exit`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/entry/common.c#L406)部分会再进行`抢占执行`部分。实际上，任何调用[`exit_to_user_mode_prepare`](https://elixir.bootlin.com/linux/v6.6.21/source/arch/arm64/kernel/entry-common.c#L129)的内核代码，都有机会进行`抢占执行`，在内核中。

`read_thread_flags`会读取当前任务的thread info信息，如果其中存在一些flag，则会进一步进入到`exit_to_user_mode_loop`中

```c
static __always_inline void exit_to_user_mode_prepare(struct pt_regs *regs)
{
    ...
	ti_work = read_thread_flags();
	if (unlikely(ti_work & EXIT_TO_USER_MODE_WORK))
		ti_work = exit_to_user_mode_loop(regs, ti_work);
    ...
}
```

而如过检查到上述`抢占决策`所设定的标记`_TIF_NEED_RESCHED`, 则会调用`schedule`函数

```c
/**
 * exit_to_user_mode_loop - do any pending work before leaving to user space
 * @regs:	Pointer to pt_regs on entry stack
 * @ti_work:	TIF work flags as read by the caller
 */
__always_inline unsigned long exit_to_user_mode_loop(struct pt_regs *regs,
						     unsigned long ti_work)
{
	/*
	 * Before returning to user space ensure that all pending work
	 * items have been completed.
	 */
	while (ti_work & EXIT_TO_USER_MODE_WORK) {

		local_irq_enable_exit_to_user(ti_work);

		if (ti_work & _TIF_NEED_RESCHED)
			schedule();
        ...
}
```

#### (4) 切换时机

**中断**

[DEFINE_IDTENTRY](https://elixir.bootlin.com/linux/v6.6.21/source/arch/x86/include/asm/idtentry.h#L49)宏用来顶一个一个中断向量，而在宏中，就设置好了中断处理的主要逻辑，其中在中断返回时，会产生一个切换时机

irqentry_exit -> irqentry_exit_to_user_mode -> exit_to_user_mode_prepare

**系统调用**

entry_64.S: do_syscall_64

[`do_syscall_64`](https://elixir.bootlin.com/linux/v6.6.21/source/arch/x86/entry/common.c#L74)是x86-64中系统调用的入口函数，而在处理完系统调用后，会产生一个切换时机

syscall_exit_to_user_mode_work -> exit_to_user_mode_prepare


### (5) 任务选择-pick_next_task

core中定义了一个内部函数[`pick_next_task`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/sched/core.c#L6069), 用于在 schedule 中挑选下一个适合执行的任务

### (6) 任务取出-put_prev_task

pick好一个任务时，若与当前任务不同，则需要将当前任务放回到队列中， 此过程中同样涉及到任务入队，但不同于任务创建时的入队，此处针对于一个曾处于runq中的任务


### (6) 任务取出-set_next_task

set_next_task 用于将选择好的任务从队列中取出，并设置为下一个要执行的任务。这个过程中也涉及到任务出队，但不同与任务执行完毕后的出队，此处的出队是临时地


### (6) 任务入队-enqueue_task

core中定义了一个内部函数[`enqueue_task`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/sched/core.c#L2091)封装了不同调度类enqueue_task的实现

fork一个新进程执行时，首先会经由 kernel_clone->copy_process->sched_fork 完成调度信息的初始化，随后会依次调用 kernel_clone->wake_up_new_task->activate_task, 从而将任务加入到调度类的运行队列上

### (7) 任务出队-dequeue_task

core中定义了一个内部函数[`dequeue_task`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/sched/core.c#L2108)封装了不同调度类dequeue_task的实现

进程main函数结束之后，通常还会执行exit系统调用，[`do_exit`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/exit.c#L809)是过程中的核心逻辑, 其中会进行一些资源回收工作，显然 exit 通常会返回，核心就在于[`do_task_dead`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/sched/core.c#L6706)中会调用 schedule 函数切换到下一个进程，其中就会进行 deactivate_task->dequeue_task

执行调度循环(__schedule_loop)时，会将不再执行的任务从队列中移出，通过依次调用 deactivate_task->dequeue_task 完成
 

### (8) 任务移动-sched_move_task

core中定义了一个将task从一个group移动到另一个group中的方式[`sched_move_task`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/sched/core.c#L10499)。而与调度策略类似，任务移动也只是修改了任务的相关信息，因而实现逻辑也十分简单
1. 将任务移除当前队列
2. 修改任务group信息
3. 将任务加入到新队列中

### (9) 优先级调整-set_user_nice

对于相同队列中的任务，调度策略依赖预先的优先级定义，linux提供了nice机制来进行优先级的什么，通过core中的[`set_user_nice`](https://elixir.bootlin.com/linux/v6.6.21/source/kernel/sched/core.c#L7188)实现。优先级调整实际上也是字段的修改，因此逻辑与上述任务移动类似


## 二、Sched Class调度

Core实质上是一种批处理调度器，因其绝大部分逻辑都足够通用，所以被单独提取为一个任务调度框架，同时具体的调度器行为交由SCHED_CLASS来执行

### 非抢占调度-STOP/FIFO

最简单的 stop 调度类(STOP调度策略)，就是从批处理中分拆出来的剩余逻辑，几乎所有的调度类功能都是空的，在此调度器下，实际上就是批处理调度的逻辑，任务以FIFO的形式加入到CORE队列中(STOP中只为CORE计数)，并在一个任务退出时，切换到另一任务执行。

同时在rt调度类中，也提供了FIFO调度策略，此时`task_tick_rt`中只更新记账信息，而不进行任何抢占标志的设置，实质上，任务还是以FIFO进行调度，但不同于stop调度类，rt调度类中存在多个优先级队列，使得能够为进程设置不同的优先级，来让进程被优先执行

### 抢占式调度-RR/FAIR/BATCH/IDLE

抢占式调度即同一个队列中的任务，可以被剥夺执行的权限，并由调度策略决定另一任务的运行

抢占式调度通常依赖时钟中断，并在每个`task_tick`中决策以判断是否设置抢占标签。
- HZ决定了时间片的粒度(注意，不是时间片的大小)
- RR、FAIR都是抢占式调度

## 其他

### Preemption modes

抢占式调度强调的是同一个队列中的任务能够被剥夺执行权限而让CPU执行另一个任务，通常由调度策略来决定抢占的发生，并以系统调用、中断处理作为进行调度的时机。而内核抢占模式通常指内核态代码的执行，是否能够被抢占(通常是高优先级的中断)

[Preemption modes](https://lwn.net/Articles/944686/)

当前Linux内核提供了4种抢占模式，每种模式的区分在于内核代码执行过程中，可抢占位点的不同:
- PREEMPT_NONE, 最早的抢占模型，内核态代码需要显示地调用一些函数来主动放弃CPU
- PREEMPT_VOLUNTARY，相较于PREEMPT_NONE增加了一些内核态代码中的抢占位点
- PREEMPT， 完全抢占，内核可以在任何时候被抢占
- PREEMPT_RT，实时抢占，多数自旋锁也能够被抢占，同时修改了内核代码，减少不可抢占的部分

越多的抢占位点能够使得系统的响应性提升，但同时内核代码被频繁打断则容易导致整体执行效率变低(局部性的破坏)

### HZ

CONFIG_HZ是一个编译时标志，用以指示内核的时钟滴答频率。

周期性的处理时钟中断有利于进行任务调度，然而如果CPU上并没有执行任务，则时钟中断会引入不必要的开销，而为了提升能源效率，内核也提供了[NO_HZ参数](https://docs.kernel.org/timers/no_hz.html)，在特定情况下，减少调度时钟中断
- CONFIG_HZ_PERIODIC=y: 永远  不要忽略时钟中断
- CONFIG_NO_HZ_IDLE=y: 忽略idle CPU上的时钟中断
- CONFIG_NO_HZ_FULL=y: 忽略idle以及只有**1个任务**的CPU上的时钟中断(对于实时任务)


