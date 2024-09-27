# Sched Ext

A scheduler framework base on eBPF

# Patch Follow

[v1](https://lore.kernel.org/all/20221130082313.3241517-1-tj@kernel.org/)


## Why

**为实验与探索提供方便**


**自定义**

[AMD hints scheduler](https://lore.kernel.org/lkml/20220910105326.1797-1-kprateek.nayak@amd.com/)

**快速的调度部署**


Deployment for
- hardware bug
- resource contention

`low-priority workloads were causing degraded
performance for higher-priority workloads due to consuming a disproportionate
share of memory bandwidth`

## How

BPF’s struct_ops feature

**Dispatch queues**

**Scheduling cycle**

# Doc

[extensible_scheduler_class](https://github.com/sched-ext/sched_ext/blob/sched_ext-v5/Documentation/scheduler/sched-ext.rst)


如果没有加载BPF Scheduler，则调度类将会被设置为Fair，尽管此时的调度策略仍然是EXT

```c
#ifdef CONFIG_SCHED_CLASS_EXT
	else if (task_should_scx(p))
		p->sched_class = &ext_sched_class;
#endif
```

## CPU Kicking

集中式调度所有的调度决策集中在特定的CPU核心上进行，并通过CPU交互模型来同步决策结果，交互模型由通信机制、协议两部分组成，设计时需要考虑延时与数据的原子性

Ext调度类提供了 `scx_bpf_kick_cpu` kfunc，允许BPF程序通过IPI来与各个CPU交互，首先，EXT调度类在初始化时，会在每个CPU的RQ上初始化一个kick_cpus_irq_work，中断的回调函数为`kick_cpus_irq_workfn`，同时每个RQ还会保存四类CPU Mask
- scx_bpf_kick_cpu 会在当前CPU的rq中，根据目标CPU设置CPU Mask标志，随后将kick_cpus_irq_work通过irq_work_queue函数加入到当前CPU的irq work队列中
- core调度时，如果选择了EXT调度类，则首先会执行 scx_notify_pick_next_task，并将 scx_rq 中的 pnt_seq (pick_next_sequence)进行递增

```c
struct scx_rq {
	struct scx_dispatch_q	local_dsq;
	struct list_head	runnable_list;		/* runnable tasks on this rq */
	unsigned long		ops_qseq;
	u64			extra_enq_flags;	/* see move_task_to_local_dsq() */
	u32			nr_running;
	u32			flags;
	bool			cpu_released;
	cpumask_var_t		cpus_to_kick;
	cpumask_var_t		cpus_to_kick_if_idle;
	cpumask_var_t		cpus_to_preempt;
	cpumask_var_t		cpus_to_wait;
	unsigned long		pnt_seq;
	struct irq_work		kick_cpus_irq_work;
};
```

irq work唤起执行时，会进入 `kick_cpus_irq_workfn` 的逻辑中，并遍历每个cpu mask来检视需要kick的CPU，针对单个CPU，会使用`kick_one_cpu`，其中关键在于`resched_curr`的调用
- resched_curr会设置CPU为需要抢占
- 如果目标cpu与发起resched_curr的cpu不同，则改用 smp_send_reschedule

smp_send_reschedule 在不同体系结构下的实现各不相同
- x86: 实现为 `native_smp_send_reschedule`，即发送IPI并指定中断向量为RESCHEDULE_VECTOR，目标CPU在收到IPI之后会执行sysvec_reschedule_ipi中的内容，并将CPU当前设置为需要抢占


```c
// # arch/x86/kernel/apic/ipi.c

void native_smp_send_reschedule(int cpu)
{
	if (unlikely(cpu_is_offline(cpu))) {
		WARN(1, "sched: Unexpected reschedule of offline CPU#%d!\n", cpu);
		return;
	}
	__apic_send_IPI(cpu, RESCHEDULE_VECTOR);
}


// # arch/x86/kernel/smp.c
/*
 * Reschedule call back. KVM uses this interrupt to force a cpu out of
 * guest mode.
 */
DEFINE_IDTENTRY_SYSVEC_SIMPLE(sysvec_reschedule_ipi)
{
	apic_eoi();
	trace_reschedule_entry(RESCHEDULE_VECTOR);
	inc_irq_stat(irq_resched_count);
	scheduler_ipi();
	trace_reschedule_exit(RESCHEDULE_VECTOR);
}
```

三种kick模式的差异
- SCX_KICK_IDLE
- SCX_KICK_PREEMPT
- SCX_KICK_WAIT

SCX_KICK_IDLE的目标会存放在 cpus_to_kick_if_idle 中，其余目标首先会保存在 cpus_to_kick 中，然后根据flag再在 cpus_to_preempt 或 cpus_to_wait 中保存

cpus_to_kick 中的目标都会调用 kick_one_cpu 进行处理，cpus_to_kick_if_idle 中的目标使用 kick_one_cpu_if_idle 进行处理。
kick_one_cpu中
- cpus_to_preempt: 遍历其中的任务，若目标CPU的当前任务属于Ext类时，则将其slice设置为0，即抢占目标的当前任务
- cpus_to_wait: 记录所有目标cpu scx_rq 的pnt_seq到 pseqs 数组中

> 使用 smp_load_acquire、smp_store_release这对原子操作来安全地访问内存
> cpu_relax通常是让CPU运行一些较为"轻松"的指令，x86中的实现为 "rep; nop"，即重复的空指令，减少对片上资源的占用(ALU、FU等)

以上处理完毕之后，如果需要等待，则遍历 cpus_to_wait 中的目标，轮询目标CPU scx_rq 的 pnt_seq
- pnt_seq未变化时，执行 cpu_relax 进行忙等，此时Ext调度类会hang在内核态，也意味着
- 当目标CPU上的EXT被调度时，pnt_seq会递增，此时便退出 wait 状态

## Dispatch & CPU Aquire & CPU Release

> balance 大于 1 通常意味着此调度类 rq 中有任务，因而能够继续执行

schedule_loop 的 put_prev_task_balance 中首先会从当前调度类开始向低优先级的调度类遍历，直到有一个调度类 balance 结果大于1，Ext中的balance 方法为 balance_scx，此方法的调用也意味着Ext调度类获得了CPU的运行权限，因此首先会触发 bpf scheduler 中的 cpu_accquire 逻辑，同时，若且当前CPU的 local DSQ 以及 global DSQ 的任务数量均为0，则会进入一个有限循环，唤起 bpf scheduler 的 dispatch 方法尝试调度，并直到没有任务返回，如最终都没有任务被调度，则 balance 返回 0

Ext pick_next_task 的实现为从 local 或 global DSQ 中获取任务，如果没有，就返回空

每当有调度类的任务被pick时，就会触发 scx_notify_pick_next_task 函数，其中会记录 Ext 调度类被抢占的原因，并在被高优先级原因抢占时，触发bpf scheduler 的 cpu_release 回调
