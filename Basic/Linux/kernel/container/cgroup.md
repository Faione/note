# Cgroup In Kernel


开启[`Cgroup`](https://elixir.bootlin.com/linux/v6.4.15/source/include/linux/cgroup-defs.h#L43)之后(通常是默认的), 内核源代码中的如下部分将会被编译到内核中，其中 `cgroup_subsys_id` 是包含当前所有[cgroup_subsys](https://elixir.bootlin.com/linux/v6.4.15/source/include/linux/cgroup_subsys.h)的枚举， `SUBSYS` 宏用来定义枚举成员，即根据 `_x` 拼成员 `_x ## _cgrp_id`, `##` 用于连接两个操作符，得到结果如 `cpuacct_cgrp_id`, 而最后一个枚举成员 `CGROUP_SUBSYS_COUNT` 便就是当前枚举类型的总数

```c
#ifdef CONFIG_CGROUPS

struct cgroup;
struct cgroup_root;
struct cgroup_subsys;
struct cgroup_taskset;
struct kernfs_node;
struct kernfs_ops;
struct kernfs_open_file;
struct seq_file;
struct poll_table_struct;

#define MAX_CGROUP_TYPE_NAMELEN 32
#define MAX_CGROUP_ROOT_NAMELEN 64
#define MAX_CFTYPE_NAME		64

/* define the enumeration of all cgroup subsystems */
#define SUBSYS(_x) _x ## _cgrp_id,
enum cgroup_subsys_id {
#include <linux/cgroup_subsys.h>
	CGROUP_SUBSYS_COUNT,
};
#undef SUBSYS
```

## Struct

