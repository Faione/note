# Capacity Aware Sched

## CPU Capacity

Symmetric、Asymmetric(Heterogeneous)

Maximum CPU Capacity
- 并非所有CPU使用相同的μArch
- 因为DVFS的存在, 并非所有的CPU都能够都达到OOP(Operating Performance Points)

$$capacity(cpu) = work_per_hz(cpu) * max_freq(cpu)$$

## Task Utilization

基础公式, 其中 duty_cycle 意为占空比, 本意指一个周期内信号处于激活状态所占的比例, 而在CPU的执行过程中, 也仅有 执行/空闲 两种状态，因此使用 duty_cycle 可以描述 task_util    

$$task_util(p) = duty_cycle(p)$$

### Frequency invariance

当 CPU 频率发生变化时, 会导致OPPs的改变，从而导致 duty_cycle 的变化，为了总是反映出相对于最大 Capacity 的 duty_cycle， 因此需要对频率进行修正

$$task_util_freq_inv(p) = duty_cycle(p) * (curr_frequency(cpu) / max_frequency(cpu))$$

### CPU invariance

若 CPU 频率相同, 则 CPU 本身的差异也会导致OPPs的变化, 因此也需要对 CPU Capacity 进行修正

$$task_util_cpu_inv(p) = duty_cycle(p) * (capacity(cpu) / max_capacity)$$

### Invariant task utilization

综合上述分析，task_util_inv 的计算公式如下，其反映出的效果是好像task就在系统中Capacity最大的CPU，以最大频率运行的一样

```
                                   curr_frequency(cpu)   capacity(cpu)
task_util_inv(p) = duty_cycle(p) * ------------------- * -------------
                                   max_frequency(cpu)    max_capacity
```

### Utilization estimation

事实上并没有有效手段能够在 task 首次运行时就能够对其行为(以及task utilization)进行预测。CFS调度器通过维护一个对每个调度实体的负载跟踪(PELT)的机制，其使用到的仍然是机制所得到的平均利用率而非瞬时利用率。容量感知调度的基于有这样一种机制的基础上编写，而实际实现的这种机制通常是基于估计的

## Scheduler topology

- `sched_asym_cpucapacity`是全局静态的，标注系统是否是是非对称的
- `SD_ASYM_CPUCAPACITY_FULL ` 在最低级的调度域设置，标识当前调度域是否是非对称的 
- `SD_ASYM_CPUCAPACITY ` 在任意跨非对称调度域的调度域上设置, 标识当前调度域是否包含了非对称的部分

## Capacity aware scheduling implementation


