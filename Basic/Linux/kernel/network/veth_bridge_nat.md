## 交换网络

初始化网络拓扑 

```shell
# 创建网络命名空间
$ sudo ip netns add netdemo 
 
# 增加虚拟网络对
$ sudo ip link add vethdemo type veth peer vethdemo_p

# 增加一个虚拟网桥
$ sudo ip link add brdemo type bridge

# 将 vethdemo_p 连接到 brdemo
$ sudo ip link set dev vethdemo_p master brdemo

# 将 vethdemo 加入到 netdemo中
$ sudo ip link set vethdemo netns netdemo
```

设置ip并启动网卡，此时 vethdemo 与 brdemo 通过网桥相连，透过 vethdemo_p 联通了默认网络命名空间与netdemo

```shell
# 设置 ip 地址
$ sudo ip netns exec netdemo ip addr add 192.168.3.2/24 dev vethdemo
$ sudo ip addr add 192.168.3.1/24 dev brdemo

# 启动网络设备, veth pair两端会同时启动
$ sudo ip netns exec netdemo ip link set vethdemo up
$ sudo ip link set brdemo up
```
host A vethdemo 第一次ping时 host B brdemo时:
1. A构造icmp request包交给下层i下而已，kernel查询路由表，发现目标在vethdemo所处的同一网段，可以直接发送
2. A查询arp表，发现目标地址不在缓存中，因此广播arp报文
3. arp包经由 vethdemo_p 到达 bridge， bridge， 向所有除vethdemo_p的所有端口发送arp报文, 其中B收到并发现于自己的ip相同，于是缓存A的mac地址，并进行回应
4. A收到arp响应包，得到了目标对地址对应的Mac地址，因此开始后续数据帧的发送
5. birdge根据mac地址信息，将转发数据帧到B， 数据帧传送完毕后，B 读取到icmp request报文，随后构造 icmp reply 报文进行回应

## 路由网络

A要访问不同网段(host B能够访问)的其他主机, 此时查询路由表后显然会提示 unreachable，而为达到此目标，需要让 host B 提供路由功能
- 使能 host 的 ipv4 forwarding 功能，当收到目的地址非本机ip的包，不丢弃，而是进行转发
- 使用 nat 来进行外部地址访问

```shell
# 开启host ipv4转发
$ sudo sysctl net.ipv4.conf.all.forwarding=1

# 配置iptables，使得host将来自192.168.3.0/24网段的数据通过nats地址转化发送出去
$ sudo iptables -t nat -A POSTROUTING -s 192.168.3.0/24 ! -o brdemo -j MASQUERADE

# 设置默认路由为 192.168.3.1，网卡 vethdemo
$ sudo ip netns exec netdemo route add default gw 192.168.3.1 vethdemo
```

host A 通过 host B nat访问其他主机:
1. A 首先构造icmp request包交给下层协议，kernel查询路由表，发现目标ip地址最长匹配为默认路由(0.0.0.0), 对应的路由表项为 192.168.3.1 vethdemo, 即下一跳地址为网关，随后根据arp表获取mac地址并发送包
2. B 收到包之后，由于开启了转发，因此会查询自己的路由表，获取下一条的地址为 192.168.176.2 ens33
3. 由于设置了 POSTROUTING 配置， 对于来自 192.168.3.0/24 的包，会使用 nat 进行地址转化，同时会使用 icmp 包中的 identifier [^1] 对转化进行标注，以区分不同的 icmp 包，并使用ens33的ip地址转发icmp request包
4. ens33收到icmp reply包时，会检查其中的 identifier， 再通过 nat 转化将 host A 的地址填充到目标地址字段，并发送回 A


[^1]: [icmpv4](http://www.tcpipguide.com/free/t_ICMPv4EchoRequestandEchoReplyMessages-2.htm)
[^2]: [nat地址转换详解](https://zhuanlan.zhihu.com/p/375937088)








