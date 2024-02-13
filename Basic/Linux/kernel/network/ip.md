# netns 

```shell
# 查看帮助
ip netns help

#增加一个命名空间
ip netns add <ns>

# list只能查看通过 ip netns 创建的命名空间
ip netns list

# 在给定的命名空间中执行命令
ip netns exec <ns> <cmd>
```

# link


```shell
# 增加 veth pair， veth pair 总是成对出现/删除
ip link add <> type veth peer <>

ip link show

ip link del <dev>
```
