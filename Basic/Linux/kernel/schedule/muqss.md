## MuQSS

BFS(Brian Fuck Scheduler)
- rr_interval(time_slice), EEVDF(earliest eligible virtual deadline first)
- $$virtual\_{}deadline = jiffies + (prio\_{}ratio * rr\_{}interval)$$
- 使用一个 global runqueue 和一把 global lock 管理所有task, 每轮调度选择最早 deadline 的task执行, 调度间隔是 rr_interval
- rr_interval 默认值为 6ms，这基于人类7ms感知速度，以及每个CPU上0-2个任务所决定的，这使得每个任务的等待时间不会超过7ms 
- 不进行负载均衡，而是在每次调度是，为task选择空闲的CPU，优先级从内向外(拓扑), 即 hyper-threading -> numa -> socket
- 精简掉了大量特性，如cgroup


BFS中的全局锁会在CPU数量超过16时产生争用

MuQSS(Multiple Queue Skiplist Scheduler)启发自BFS
- rr_interval(time_slice), EEVDF(earliest eligible virtual deadline first), skip list 
- $$virtual\_{}deadline = niffies + (prio\_{}ratio * rr\_{}interval)$$
- 为解决BFS全局锁的性能问题，使用 per-cpu runqueue, 引入 skip list 维护task, 使用 niffies 替换 jiffies, 实现高分辨率定时
- 选择 task 执行时，MuQSS对per-cpu runqueue进行无锁检查，找到最优的task(EEVDF), 从相关队列取出此 task 时，采用 "trylock" 策略，如获取失败，则移动到另一个 runqueue 上进行尝试
- 知道CPU拓扑，在选择一个hyperthreaded siblings之前会尽量选择一个idle core，当tasks运行在hyperthreaded core时，低优先级的task运行时间将会被限制，以保证高优先级task的运行时间(存在争用)

[The MuQSS CPU scheduler](https://lwn.net/Articles/720227/)