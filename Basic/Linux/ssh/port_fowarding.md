## PortFowarding

通过 ssh 建立本地与远端的隧道, 进而进行端口转发[^1]
- `-L`: LocalForward, 将传入本地端口的流量转发到远端端口, 实现在本地环境访问远端才能访问的服务
- `-R`: RemoteForward, 将传入远端端口的流量转发到本地端口, 实现在远端访问本地才能访问的服务

```
ssh -L local-port:target-host:target-port tunnel-host
```

tymm135 
pbxj928
Cqmyg@817

[^1]: [ssh_port_forwarding](https://wangdoc.com/ssh/port-forwarding)
