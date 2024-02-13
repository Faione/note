## CFS Schedule

[`cfs_scheduler`](http://arthurchiao.art/blog/linux-cfs-design-and-implementation-zh/)以完全公平为目标，对于有 n 个理想进程的机器，调度器应当保证每个进程各占 1/n 的CPU时间

抢占式多任务系统中需要进行task之间的切换，在内核中，从一个task的上下文切换到另一个task的上下文是通过[`schedule`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L6738)函数完成的，同时在内核中会为每个 task 维护一个[`sched_entity`](https://elixir.bootlin.com/linux/v6.4.13/source/include/linux/sched.h#L549)保存必要的时间记账信息, 而其核心的过程包含在函数[`__schedule`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L6550)中

`__schedule` 中通过 [`pick_next_task`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L6035) 来寻找下一个应当被调度的task, 其会调用[`__pick_next_task`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L5958), 存在多个队列时，会从最高优先级的调度类开始，调用其 `pick_next_task`，从第一个返回非NULL值的类中选择下一个task。考虑到OS中多数task都是普通task，因此如果所有的task都在CFS调度器中，就会优先通过[`pick_next_task_fair`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/fair.c#L8004) 来获取task

> 事实上调度实体是分层级的，如 task -> 进程组 -> 用户，各个调度实体时间的父子关系通过 se 中的 parent 指针进行维护，同时任意一层中的se都包含一个 my_q 指针，用来其所拥有的下一层se的runqueue，使用 group_cfs_rq 函数可以获取 se 所对应的下层 se 的 cfs_rq，而对于task se而言，其 my_q 显然是空的。当更新task se 中的 vruntime 时，显然需要同时更新父se的 vruntime，以保证各层调度实体都能够达到公平，这样的调度也被称为 group scheduling[^9]，而group scheduling 的调度是自上而下的

> for_each_sched_entity(se) 宏能够从下层的调度实体开始，访问其 se->parent 向上层遍历
> group_cfs_rq(se) 函数则从上层调度实体开始，访问其 se->my_q 向下层遍历

`pick_next_task_fair` 中 [`simple`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/fair.c#L8093) 定义了简易逻辑，首先会调用 `put_prev_task` 函数将当前task放回调度队列，对于 CFS 调度器而言是 `put_prev_task_fair` 方法，对于当前的调度实体，会对其以及其父调度实体调用 `put_prev_entity` 将其重新放回调度队列中, 而具体在函数中会调用 [`update_curr`](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/fair.c#L897) 更新时间记账， 随后通过 `pick_next_entity` 从RBT中找到优先级最高的 se， 然后调用 `set_next_entity`，其中会调用 `__dequeue_entity` 从runqueue中取出se，这段代码在一个 do while 循环中执行，这是因为需要判断 se 是属于 task 还是 task group， 对于 task 而言， 其se中 my_q 为空，而对于 task group 而言， 其se中的 my_q 指向其所 "拥有" 的task cfs队列，从而在下一次循环中，会从此队列中取得task，从而保证返回的 se 是一个 task 的 se

`update_curr`[^6] 是CFS中的核心过程，其中主要进行的就是更新时间记账以及 vruntime 等核心数据，并调用 `update_min_vruntime` 更新当前的RBT。通常vruntime的增长与实际执行时间相同，而如果设置了优先级，则需要将实际时间加权计算[^7], nice值与实际权重的关系如下[^8], 相邻nice值权重相差10%, 如果se优先级为0，则delta vruntime就是执行时间，否则通过 `delta_vruntime = delta_exec * nice_0_weight / lw.weight`，其中 `lw.weight` 是当前se优先级对于的权重

在 next task 被选择出来之后，`__schedule` 还会判断next是否prev相等，相等则进行返回，否则则进行context switch，切换到下一个task

[^7]: [calc_delta_fair](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/fair.c#L709)
[^8]: [prio_to_weight](https://elixir.bootlin.com/linux/v6.4.13/source/kernel/sched/core.c#L11459)
[^9]: [group_scheduling](https://lwn.net/Articles/240474/)
[^10]: [kernel_cfs_scheduler](https://docs.kernel.org/scheduler/sched-design-CFS.html)

## CFS & CPU ACCT

`update_curr` 更新task时间记账时会同时更新CPU_ACCT Subsystem的时间记账

函数[`cgroup_account_cputime`](https://elixir.bootlin.com/linux/v6.4.15/source/include/linux/cgroup.h#L715)中完成了此逻辑，其核心函数[`cpuacct_charge`](https://elixir.bootlin.com/linux/v6.4.15/source/kernel/sched/cpuacct.c#L334)中会进行cpuacct的更新, `task_ca`能够从当前task_struct中获取对应的cpuacct， 其内部首先通过`task_css`从`struct css_set __rcu *cgroups`成员中读取出 cpuacct 子系统的 `cgroup_subsys_state`, 注意`cpuacct`包含有`cgroup_subsys_state`指针，意味着可通过`container_of`依据相对偏移从`cgroup_subsys_state`获取`cpuacct`， 实现这一逻辑的是`css_ca`函数，以上函数都包含在[`cpuacct.c`](https://elixir.bootlin.com/linux/v6.4.15/source/kernel/sched/cpuacct.c#L24)中, `cgroup_subsys_state`本身包含了指向其parent的指针，循环中基于此对其父CPU_ACCT也进行了更新

由此便可在 `cpuacct/cpuacct.usage`看到对应的记账信息

```c
void cpuacct_charge(struct task_struct *tsk, u64 cputime)
{
  // 获取当前task所在的cpu
	unsigned int cpu = task_cpu(tsk);
	struct cpuacct *ca;

  // 获取锁
	lockdep_assert_rq_held(cpu_rq(cpu));

  // 更新当前task及其所属的cgroup/parent cgroup的cpu acct
	for (ca = task_ca(tsk); ca; ca = parent_ca(ca))
		*per_cpu_ptr(ca->cpuusage, cpu) += cputime;
}
```

## CFS & CPU SET