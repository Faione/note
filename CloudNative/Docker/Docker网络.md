## Docker 网络分析

## Docker 网络配置

- 将容器置于同一个网络中
- 为容器增加extra-ip访问宿主网络
  - 为容器增加域名`hostsvc`
  - `host-gateway`指向docker0网桥，与宿主网络互联

```yml
extra_hosts:
    - "hostsvc:host-gateway"
```