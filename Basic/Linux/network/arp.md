# arp

arp 表缓存了局域网中 ip <-> mac 的映射， 通过arp协议填充

```shell
# 查看
arp

# 删除
arp -i <dev> -d <ip>

# 删除网卡的所有 arp 缓存
ip neigh flush dev <dev>
```