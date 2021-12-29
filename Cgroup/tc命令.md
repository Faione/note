# Traffic Control

- [Traffic Control](#traffic-control)
  - [参考](#参考)
  - [一、概述](#一概述)
    - [(1) 基础](#1-基础)
    - [(2) TC工具](#2-tc工具)
  - [二、TC工具的使用](#二tc工具的使用)
    - [(1) 创建HTB队列](#1-创建htb队列)
    - [(2) 常用命令](#2-常用命令)
  - [三、TC+Cgroup限制进程流量](#三tccgroup限制进程流量)
  - [三、容器网络调控](#三容器网络调控)

## 参考

- [tc用法](https://www.cnblogs.com/yulia/p/10346339.html)
- [tc简介](https://cloud.tencent.com/developer/article/1409664)
- [*tc概述](https://blog.csdn.net/qinyushuang/article/details/46611709)
- [tc流量控制](https://www.cnblogs.com/yhp-smarthome/p/11182683.html)
- [tc详细操作](https://blog.csdn.net/u011641885/article/details/45640313)

- [tc实践](http://perthcharles.github.io/2015/06/12/tc-tutorial/)
- [tc HOWTO](https://tldp.org/HOWTO/html_single/Traffic-Control-HOWTO/)

## 一、概述

### (1) 基础

- 报文转发

报文分组从输入网卡(入口)接收进来，经过路由的查找，以确定是发给本机的，还是需要转发的

如果是发给本机的，就直接向上递交给上层的协议，比如TCP，如果是转发的，则会从输出网卡(出口)发出。网络流量的控制通常发生在**输出网卡**处。虽然在路由器的入口处也可以进行流量控制，Linux也具有相关的功能，但一般说来，由于我们无法控制自己网络之外的设备，入口处的流量控制相对较难。因此我们这里处理的流量控制一般指出口处的流量控制

流量控制的一个基本概念是队列(Qdisc)，每个网卡都与一个队列(Qdisc)相联系，每当内核需要将报文分组从网卡发送出去，都会首先将该报文分组添加到该网卡所配置的队列中，由该队列决定报文分组的发送顺序

- 输出队列

有些队列的功能是非常简单的，它们对报文分组实行先来先走的策略。有些队列则功能复杂，会将不同的报文分组进行排队、分类，并根据不同的原则，以不同的顺序发送队列中的报文分组。为实现这样的功能，这些复杂的队列需要使用不同的过滤器(Filter)来把报文分组分成不同的类别(Class)。这里把这些复杂的队列称为可分类(Classiful)的队列。通常，要实现功能强大的流量控制，可分类的队列是必不可少的。因此，类别(Class)和过滤器(Filter)也是流量控制的另外两个重要的基本概念

类别(Class)和过滤器(Filter)都是队列的内部结构，并且可分类的队列可以包含多个类别，同时，一个类别又可以进一步包含有子队列，或者子类别。所有进入该类别的报文分组可以依据不同的原则放入不同的子队列 或子类别中，以此类推。而过滤器(Filter)是队列用来对数据报文进行分类的工具，它决定一个数据报文将被分配到哪个类别中

### (2) TC工具

tc 是Linux 系统中的一个工具,全名为 traffic control (流量控制)

Linux通过TC工具进行进行流量控制, 一般流程为:
   - 为网卡配置一个队列
   - 在该队列上建立分类
   - 根据需要建立子队列和子分类
   - 为每个分类建立过滤器

在Linux中，可以配置很多类型的队列，比如CBQ、HTB等，其中CBQ 比较复杂，不容易理解。HTB(Hierarchical Token Bucket)是一个可分类的队列， 与其他复杂的队列类型相比，HTB具有功能强大、配置简单及容易上手等优点。在TC中，使用"major:minor"这样的句柄来标识队列和类别，其中major和minor都是数字

对于队列来说，minor总是为0，即"major:0"这样的形式，也可以简写为"major: "比如，队列1:0可以简写为1:。需要注意的是，major在一个网卡的所有队列中必须是惟一的。对于类别来说，其major必须和它的父类别或父队列的major相同，而minor在一个队列内部则必须是惟一的(因为类别肯定是包含在某个队列中的)。举个例子，如果队列2:包含两个类别，则这两个类别的句柄必须是2:x这样的形式，并且它们的x不能相同，比如2:1和2:2

? : 标识省略的0

## 二、TC工具的使用

### (1) 创建HTB队列

- 为网卡添加 HTB队列

```shell
# tc qdisc [add | change | replace | link] dev DEV [parent qdisk-id |root] [handle qdisc-id] qdisc [qdisc specific parameters]
$  tc qdisc add dev eth0 root handle 1:htb default 11

# "add": 表示要添加
# "dev eth0": 表示要操作的网卡为 eth0
# "root": 表示为网卡eth0添加的是一个根队列
# "handle 1:": 表示添加的队列句柄为 "1:"
# "htb": 表示要添加的为HTB队列
# "default 11": htb特有队列参数，标识所有未分类的流量都分配给 1:11
```

- 为根队列创建类别

```shell
#tc class [add | change | replace] dev DEV parent qdisc-id [classid class-id] qdisc [qdisc specific parameters]
$ tc class add dev eth0 parent 1: classid 1:11 htb rate 40mbit ceil 40mbit

# "parent 1:": 表示类别的父亲为根队列 "1:"
# "classid 1:11": 表示创建标识为 "1:11" 的队列
# "rate 40mbit": 表示系统将确保该类别带宽为 40mbit
# "ceil 40mbit": 表示该类别最高可占用的带宽为 40mbit
```

- 为各类别创建过滤器
  
```shell
#tc filter [add | change | replace] dev DEV [parent qdisc-id | root] protocol protocol prio priority filtertype [filtertype specific parameters] flowid flow-id
$ tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dport 80 0xffff flowid 1:11

# "protocol ip": 表示过滤器检查ip协议字段
# "prio 1": 不同优先级的过滤器，系统将从小到大的顺序来执行，同优先级的过滤器，系统按照命令的先后顺序执行过滤器
# "u32 match ip dport 80 0xffff flowid 1:11": 以第一个命令为例，判断的是dport字段，如果该字段与Oxffff进行与操作的结果是8O，则”flowid 1:11”表示将把该数据流分配给类别1:1 1
```


### (2) 常用命令

```shell
# 删除网卡上的配置，并恢复会初始状态
$ tc qdisc del dev ens33 

# 查看, -s 可以看到细节内容
# 查看端口 队列信息
$ tc -s qdisc ls dev ens33 

# 查看端口 类别信息
$ tc -s class ls dev ens33

# 查看端口 过滤器信息
$ tc -s filter ls dev ens33

```


## 三、TC+Cgroup限制进程流量

- cgroup操作

```shell
# /sys/fs/cgroup/net_cls/
# 创建 cgroup 子系统 net_cls
$ mkdir client

# 增加 classId, 0x10010
$ echo 0x10010 > net_cls.classid

```

- tc 操作

```shell
# 清除原有队列
$ tc qdisc del dev ens33

# 创建 htb 队列, 句柄为 "1:0", 默认类别为 1
$ tc qdisc add dev ens33 root handle 1:0 htb default 1

# 创建类别, 归属 1:0 队列，类别为 1:1, 限速为 10000Mbit
$ tc class add dev ens33 parent 1:0 classid 1:1 htb rate 10000Mbit

# 创建类别, 归属 1:0 队列，类别为 1:10, 限速为 10Mbit, 峰值为 10Mbit
$ tc class add dev ens33 parent 1:0 classid 1:10 htb rate 10Mbit ceil 10Mbit

# 设置过滤器, 归属 1:0 队列, 协议为 IP, 过滤 1:10 cgroup 标签
$ tc filter add dev ens33 parent 1:0 protocol ip prio 10 handle 1:10 cgroup

# handle 1:10 cgroup: 标识将 cgroup中定义的 1:10 classId 数据包放入 类别 1:10 中

```

- 测试

```shell
# 使用 iperf 进行带宽测试
$ cgexec -g net_cls:client iperf -c 192.168.10.129 -t 10 

[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-10.0 sec  11.8 MBytes  9.85 Mbits/sec

```

## 三、容器网络调控

- 基础环境

```shell
# 安装 iproute2, 容器需要 privileged 权限
$ apt-get install iproute2
```

- 使用tc进行带宽限制

```shell
# 容器中执行命令
$ tc qdisc change dev eth0 root tbf rate 10mbit latency 50ms burst 10000 mpu 64 mtu 15000
$ tc qdisc change dev eth0 root tbf rate 10mbit latency 50ms burst 10000 
# "tbf": 令牌桶
# "rate 10mbit": 内核发放令牌的速度，每个比特要发出去时，需要从桶中取出一个令牌
# "latency": 数据包在队列中的最长等待时间
# "burst": 突发流量


# 容器外执行命令
$ docker exec <containerId> tc qdisc change dev eth0 root tbf rate 10mbit latency 50ms burst 10000
```




