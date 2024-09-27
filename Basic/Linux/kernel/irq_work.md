## Irq Work

Linux每CPU都存在如下三种数据结构，用以服务irq work

```c
static DEFINE_PER_CPU(struct llist_head, raised_list);
static DEFINE_PER_CPU(struct llist_head, lazy_list);
static DEFINE_PER_CPU(struct task_struct *, irq_workd);
```

irq work
- `init_irq_work`: 声明一个 irq work， 需要传入一个回调函数，同时默认flag为全0
- `irq_work_queue`: 将一个 irq work 加入到当前CPU的 lazy_list 或 raised_list 中
  - 如果 irq work 不是 lazy_work 或者 nohz 使能时，入队操作将会直接唤起irq work的执行？

运行时机: irq_work_run

