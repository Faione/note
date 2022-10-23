# Frp内网穿透

- [Frp内网穿透](#frp内网穿透)
  - [一、说明](#一说明)
    - [(1) 内网穿透](#1-内网穿透)
    - [(2) frp项目](#2-frp项目)
  - [二、搭建](#二搭建)
    - [(1) 暴露ssh](#1-暴露ssh)

[frp 内网穿透 web](https://www.jianshu.com/p/57658825ff0d)
[frp github](https://github.com/fatedier/frp)
## 一、说明

### (1) 内网穿透

局域网内机器能够借助NAT技术访问外部网络, 而在外部看来, 这些主机都是通过同一个ip与外部网络交互
这使得局域之外无法访问局域网内机器上的服务

内网穿透则是利用端口转发, 实用公网ip机器作为中间媒介, 将局域网主机的服务暴露出去, 从而使得外部能够通过访问公网IP主机, 间接访问到局域网主机上的服务

### (2) frp项目

frp github: 
>frp is a fast reverse proxy to help you expose a local server behind a NAT or firewall to the Internet. As of now, it supports TCP and UDP, as well as HTTP and HTTPS protocols, where requests can be forwarded to internal services by domain name

frp 架构
![frp-架构](./images/frp-architecture.png)

公网ip运行 frps 程序, 转发请求
局域网主机运行 frpc 程序, 暴露端口
用户通过公网ip访问到局域网主机暴露的服务

## 二、搭建

### (1) 暴露ssh

1. 安装软件

公网ip服务器以及局域网服务器上都需要安装frp

```shell
# 下载 frp
$ wget https://github.com/fatedier/frp/releases/download/v0.38.0/frp_0.38.0_linux_amd64.tar.gz .

# 解压缩
tar -zxvf frp_0.38.0_linux_amd64.tar.gz -C ./frp
```

2. 配置运行

**公网ip服务器**

public ip: x.x.x.x

配置 frps.ini
```ini
# frps.ini
[common]
bind_port = 10045
Start frps on server A:
```
运行
```shell
$ ./frps -c ./frps.ini
```

**局域网主机**

UserName: aab

配置 frpc.ini

```ini
# frpc.ini
[common]
server_addr = x.x.x.x // public ip 
server_port = 10045 // pulbic server listen, between frps

[ssh]
type = tcp 
local_ip = 127.0.0.1 
local_port = 22 // local port, traffic in
remote_port = 10046 // public server port, traffic out
```

运行

```shell
$ ./frpc -c ./frpc.ini
```

**用户**

```shell
$ ssh -oPort=10046 aab@x.x.x.x 
```

流程理解
 - 局域网服务器与公网ip服务器通过端口10045建立连接
 - 用户与公网ip服务器通过端口10046建立连接, frp将请求发送给局域网服务器
 - 局域网frp收到请求后, 将数据转发给22端口
 - ssh收到数据后, 发送响应, 局域网frp监听响应, 收到后发送给公网ip服务器
 - 公网ip服务器将响应发送回用户

## 热配置