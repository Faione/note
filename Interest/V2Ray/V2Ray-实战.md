# 基于容器的V2Ray搭建

## Container 时区

### 时区

- Linux通过两个文件控制当前时区
   - /etc/timezone 主要代表当前时区设置，一般链接指向/usr/share/zoneinfo目录下的具体时区
   - /etc/localtime 主要代表当前时区设置下的本地时间
   - 默认时区为零时区(容器默认的时区)

### 修改时区

同步宿主机与容器时区

```shell
# 启动时挂载宿主机时区文件
-v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro

# 启动时设置环境变量
-e TZ="Asia/Shanghai" 

# 运行时，拷贝宿主机时区文件覆盖原有配置
docker cp /usr/share/zoneinfo/Asia/Shanghai <containerId>:/etc/localtime
```

### Server端

使用docker image进行构建  

配置文件: config.json

```json
{
"inbounds": [
   {
      "port": 4396, 
      "protocol": "vmess", 
      "settings": {
         "clients": [
         {
            "id": "efad8a4b-f812-4493-903b-f28252769f29", 
            "alterId": 64
         }
         ]
      }
   }
   ],
   "outbounds": [
   {
      "protocol": "freedom", 
      "settings": {}
   }
   ]
}
```

docker-compose.yml

```yml
version: '2'

services:
    v2ray:
      image: v2fly/v2fly-core:latest
      ports:
        - '4396:4396'
      command: []
      environment:
        - TZ="Asia/Shanghai"
      volumes: # 挂载配置文件
        - /home/fhl/interestApp/v2ray/:/etc/v2ray/
```

启动

```shell
$ docker-compose up -d
```

### Client
使用 v2rayN, 添加服务器

配置文件
```json
{
  "policy": null,
  "log": {
    "access": "",
    "error": "",
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "tag": null,
      "port": 4396,
      "listen": null,
      "protocol": "vmess",
      "sniffing": null,
      "settings": {
        "auth": null,
        "udp": false,
        "ip": null,
        "address": null,
        "clients": [
          {
            "id": "efad8a4b-f812-4493-903b-f28252769f29",
            "alterId": 64,
            "email": "t@t.tt",
            "security": null
          }
        ]
      },
      "streamSettings": {
        "network": "tcp", // 服务器上需要打开对应的tcp端口
        "security": null,
        "tlsSettings": null,
        "tcpSettings": null,
        "kcpSettings": null,
        "wsSettings": null,
        "httpSettings": null,
        "quicSettings": null
      }
    }
  ],
  "outbounds": null,
  "stats": null,
  "api": null,
  "dns": null,
  "routing": {
    "domainStrategy": "IPIfNonMatch",
    "rules": []
  }
}
```