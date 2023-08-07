# iptables

iptables 是kernel提供给用户进行网络规则设置的用户接口
- 5个hook点对5个Chain: PREROUTING, INPUT， FORWARD， OUTPUT， POSTROUTING
- 实现功能的不同对应4个表: raw, mangle, nat, filter

```shell
# 查看当前的规则, 默认显示的是 filter 表
$ iptables -L

# 查看 nat 表
$ iptables -t nat -L

# 查看的同时并显示规则序号
$ iptbales -t nat -L --line-number
```

## NAT

增加nat规则

```shell

```

