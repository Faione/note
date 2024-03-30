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