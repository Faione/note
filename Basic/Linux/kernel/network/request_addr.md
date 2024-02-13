# 理解和处理 Cannot assign requested address

[Cannot assign requested address](https://www.cnblogs.com/thatsit/p/cannot-assign-requested-address.html)

```shell
## 增加随机端口的范围: 32768 60999(wsl defualt) -> 10000 65000
$ sudo sysctl -w net.ipv4.ip_local_port_range="10000 65000"

## 减少 tcp fin 连接的超时时间: 60(default) -> 15
$ sudo sysctl -w net.ipv4.tcp_fin_timeout=15
```