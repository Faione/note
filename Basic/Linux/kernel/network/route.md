# Route

route 是linux中的路由表，用来决定网络包应当从哪个网卡上发出以及下一条的地址，其中 `Destination` 与 `Genmask` 构成目标网段的信息，采用最长匹配决定路由

Gateway 为 0.0.0.0 时意味着该网卡就在目标网段中，无需进行路由，反之则说明访问目标网路需要通过网关 gateway

已经组好的ip包交给下层协议处理，此时会根据路由表，来选择下一跳的地址，如果是 0.0.0.0， 则下一跳地址为目标地址，如果为 gateway 则下一条地址为 gateway

决定好下一跳的地址后，就会通过arp表来获取实际的mac地址，封装成帧然后再发送到网络中， 如果对应的表项不在，就会通过arp协议获取目标的mac地址

```shell
# 查看路由表
$ route

# 增加默认网关
$ route add default gw <gateway> <dev>

# 删除默认网关
$ route del default
```