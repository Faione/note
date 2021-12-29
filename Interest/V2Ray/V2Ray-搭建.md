# V2Ray搭建

## 一、说明
- V2Ray提供网络代理功能 
   - 即 VPN (virtual private network)  

- V2Ray 使用 inbound(传入) 和 outbound(传出) 的结构来描述数据包的流动方向
   - 可将 V2Ray 视为一个盒子，这个盒子有入口与出口，数据包从入口进入，在其中进行处理(路由),再从出口流出（IPO模型，处理的方法中就包括了所用到的协议）
   - Client: inbound 接收来自浏览器的数据， 由 outbound 发送出去(发给 V2Ray 服务器)
   - Server: inbound 接收来自 V2Ray Client 的数据， 由 outbound 发送出去(代理访问的网站等)

- V2Ray没有使用常规的C/S结构，软件本身既可以作为Client又可以Server，但在在配置文件上存在差异
   - 每个V2Ray都是一个节点，拥有 inbounds 和 outbounds， 这意味着 V2Ray并不只是简单的IPO模型，而可以拥有入口与出口 

- 参考
   - [V2Ray架构分析](https://www.v2fly.org/developer/intro/design.html)
   - [V2Ray白话指南](https://guide.v2fly.org/)


## 二、部署

保证部署的正常，需要在root权限下

### (1) 时间校准

V2Ray的验证方式中包含时间，时间不正确，则 V2Ray Server 会认为是非法请求，并拒绝连接
>需要保证Client与Server时间误差在90以内(vmess协议)

Linux 时间操作
```shell
# 查看系统时间
$ date -R

# 修改时间
$ sudo date --set="yyyy-mm-dd hh:mm:ss"

```

### (2) 在Linux服务器上部署 V2Ray Server

V2Ray 提供脚本安装、手动安装、编译安装3种方式

#### 安装依赖软件

安装 curl
   - 请求web服务器，获得网络资源

Debian/Ubuntu
```shell
$ apt update
$ apt install curl
```

#### 下载安装脚本

```shell
$ curl -O https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh
```

#### 执行安装

实际上就是启动脚本

```
bash install-release.sh
```

#### docker仓库
V2Ray为linux平台提供的预编译版本的docker images

```shell
docker pull v2fly/v2fly-core
```
文件结构: 
- /etc/v2ray/config.json：配置文件
- /usr/bin/v2ray：V2Ray 主程序
- /usr/bin/v2ctl：V2Ray 辅助工具
- /usr/local/share/v2ray/geoip.dat：IP 数据文件
- /usr/local/share/v2ray/geosite.dat：域名数据文件

#### 运行

启动 V2Ray
   - 首次安装，V2Ray不会自动启动

```shell
# 启动V2Ray
systemctl start v2ray

# 开机自启动
systemctl enable v2ray

# 二进制文件启动
/usr/bin/v2ray --config=/etc/v2ray/config.json
```

#### 升级

升级就是再次运行安装脚本

```
bash install-release.sh
```

#### 配置

安装好的V2Ray并不能直接进行工作，而需要进行一定的配  
   - V2Ray的配置文件为JSON格式
   - Linux中，可以使用 jq 软件来检查配置文件的语法是否正确

v2ray也提供配置文件检查功能

```shell
/usr/bin/v2ray -test -config /etc/v2ray/config.json
```

[V2Ray-配置](V2Ray-配置.md)






