# Cgroup Base
- [cgroup cpu 入门](https://fuckcloudnative.io/posts/understanding-cgroups-part-2-cpu/)
- [cgroup 入门](https://fuckcloudnative.io/series/linux-cgroup-%E5%85%A5%E9%97%A8%E7%B3%BB%E5%88%97/)

## 一、基础概念

cgroup，用来统一将进程进行分组，并在分组的基础上对进程进行监控和资源控制管理等

cgroup 是 Linux 下的一种将进程按组进行管理的机制，在用户层看来，cgroup 技术就是把系统中的所有进程组织成一颗一颗独立的树，每棵树都包含系统的所有进程，树的每个节点是一个进程组，而每颗树又和一个或者多个 subsystem 关联，树的作用是将进程分组，而 subsystem 的作用就是对这些组进行操作。cgroup 主要包括下面两部分

   - subsystem : 一个 subsystem 就是一个内核模块，他被关联到一颗 cgroup 树之后，就会在树的每个节点（进程组）上做具体的操作。subsystem 经常被称作 resource controller，因为它主要被用来调度或者限制每个进程组的资源，但是这个说法不完全准确，因为有时我们将进程分组只是为了做一些监控，观察一下他们的状态，比如 perf_event subsystem。到目前为止，Linux 支持 12 种 subsystem，比如限制 CPU 的使用时间，限制使用的内存，统计 CPU 的使用情况，冻结和恢复一组进程等，后续会对它们一一进行介绍
   - hierarchy : 一个 hierarchy 可以理解为一棵 cgroup 树，树的每个节点就是一个进程组，每棵树都会与零到多个 subsystem 关联。在一颗树里面，会包含 Linux 系统中的所有进程，但每个进程只能属于一个节点（进程组）。系统中可以有很多颗 cgroup 树，每棵树都和不同的 subsystem 关联，一个进程可以属于多颗树，即一个进程可以属于多个进程组，只是这些进程组和不同的 subsystem 关联。目前 Linux 支持 12 种 subsystem，如果不考虑不与任何 subsystem 关联的情况（systemd 就属于这种情况），Linux 里面最多可以建 12 颗 cgroup 树，每棵树关联一个 subsystem，当然也可以只建一棵树，然后让这棵树关联所有的 subsystem。当一颗 cgroup 树不和任何 subsystem 关联的时候，意味着这棵树只是将进程进行分组，至于要在分组的基础上做些什么，将由应用程序自己决定，systemd 就是一个这样的例子

## 二、CPU

### (1) 基础操作

systemd -> system daemon: 为系统的启动与管理提供一套完整的解决方案
   - [systemd 服务管理](https://cloud.tencent.com/developer/article/1516125)

```shell
# 查看当前cgroup层级信息
systemd-cgls --no-page 

# 查看动态层级信息
systemd-cgtop

```

### (2) 分配CPU相对使用时间

- cpu share


- cpu quota


### lib-cgroup 工具

- 删除cgroup

```shell
$ cgdelete cpuset:mycgroup
```

- [memory](https://segmentfault.com/a/1190000008125359)

