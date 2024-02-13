# Task Schedule

## Time irq

linux中定义了 `HZ`, 用来设置设置系统定时器每秒的时钟中断次数，而在内核中会维护一个 jiffies 变量，记录当前时钟中断的次数，显然使用 jiffies / HZ 能够计算得到一个具体的时间值

[`tick_handle_periodic`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/time/tick-common.c#L107)是时钟中断事件的处理函数，其中 [`tick_periodic`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/time/tick-common.c#L85)完成了时钟中断的主要逻辑
- `do_timer`: 更新 `jiffies_64` 的值，同时使用 [`calc_global_load`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/loadavg.c#L349) 更新当前的负载情况
- `update_wall_time`: 更新墙上时钟
- [`update_process_times`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/time/timer.c#L2064): 更新进程的时间记账信息
  - 从代码实现上可以看出，每次时钟中断发生时，会将上一次中断到这一次中断的所有时间记账到此刻的进程上，既是中间可能发生过数次的进程切换，这说明进程的时钟记账并非是完全准确的，而这种误差可以通过增加HZ，即缩短时钟中断的间隔来减小
  - [`scheduler_tick`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L5640)触发调度器的相关流程，如时间片切换、进程优先级调整、负载平衡、定时器处理，其中 `curr->sched_class->task_tick` 就是调度器决定任务调度的函数，在CFS调度器中，此函数为[`task_tick_fair`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/fair.c#L12082)
    - `task_tick_fair` 中首先遍历当前进程的所有调度实体，并对每个实体所属的`cfs_rq`执行[`entity_tick`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/fair.c#L5159), 其中首先会执行一系列`update_*`函数更新相关记账信息，最后再判断当前就绪队列中的task数量大于1时，执行[`check_preempt_tick`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/fair.c#L4993), 其中会根据CFS的决策，判断是否需要抢占当前task，抢占是通过[`resched_curr`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L1041)实现, 其作用是将队列中的当前task标记为需要重新调度

## Schedule Timing

时钟中断处理中，并不会进行任务的切换，而是设置好相应的flag，切换发生在从中断处进行返回时，即`entry.S`汇编中所定义的`restore`过程，其会根据上述过程所设置的flag来决定是否调用[`preempt_schedule_irq`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L6969), 其中就会执行 `__schedule` 来真正实现task切换

在x86中，相关的逻辑定义在`arch/x86/entry/thunk_64.S`中，其中声明了每个系统调用/中断/异常返回时应该执行的事情，其中`preempt_schedule`便会进行抢占相关的逻辑，具体实现在函数[`preempt_schedule_common`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L6820)中

`preempt_schedule`的实现逻辑大体相似，其中包含有`exception_enter` 与`exception_exit`两个hook点。在主循环中，首先关闭抢占并开启本地中断，然后进入 `__schedule` 调度，若存在一个能够被调度的不同task，则 `__schedule` 中会发生 contex switch，此时从内核态返回时，下一个task会开始运行，否则回到循环中，并根据 `need_resched` 决定是否继续循环。从循环中退出会执行`exception_exit`，随后返回到 `entry.S` 定义的汇编中，在 riscv 的实现里则是恢复因中断被打断的寄存器信息，然后返回到用户态继续执行