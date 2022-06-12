# Gogs 轻量级git仓库

## 一、说明

Gogs（/gɑgz/）项目旨在打造一个以最简便的方式搭建简单、稳定和可扩展的自助 Git 服务。使用 Go 语言开发使得 Gogs 能够通过独立的二进制分发，并且支持 Go 语言支持的 所有平台，包括 Linux、macOS、Windows 以及 ARM 平台

## 二、Docker 搭建gogs

gogs依赖一个后端数据库, 选择使用Mysql作为后端存储库

### (1) Docker Mysql

```yml
version: "3"
services:   
    mariadb:
        image: "mariadb:latest"
        enviroment:
            # - MARIADB_DATABASE=gromtest // 默认创建的database, 用户 MARIADB_USER 能获得此数据库的全部权限
            - "MARIADB_USER=fhl" 
            - "MARIADB_PASSWORD=123456"
            - "MARIADB_ROOT_PASSWORD=123456"
```
容器启动后, 仍然需要进行数据库的创建

```shell
$ docker exec -it <mariadbId> /bin/bash

# 登入数据库
# 小写 p 指定将要输入的密码
$mariadbId mysql -p

# 创建指定类型的数据库
$mysql CREATE DATABASE IF NOT EXISTS gogs DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

# 查看创建好的数据库
$mysql show databases;
```

### (2) Docker Gogs

```yml
version: "3"
services:   
    gogs:
        image: "gogs/gogs"
        ports:
            - "10118:22"
            - "10119:3000"
        volumes:
        - ./var/gogs:/data
```
使用 公网ip:10119 访问初始页面, 进行初次安装的配置

Docker配置注意事项

1. 数据库地址可以指定: mariadb:3306 
   - 同一个 docker-compose文件中
2. Domain填写公网ip(公网访问需求)
3. SSH Port, HTTP Port 分别使用暴露的端口
4. Application URL使用: <Domain>:<HTTP Port>


```shell
# 替换分支前可以删除当前的远程分支
$ git remote rm origin
```

### (3) 统一Compose文件

```yml
version: "3"
services:   
    gogs:
        image: "gogs/gogs"
        ports:
            - "10118:22"
            - "10119:3000"
        volumes:
        - ./var/gogs:/data
    mariadb:
        image: "mariadb:latest"
        volumes:
        - ./var/mariadb:/var/lib/mysql 
        environment:
            - "MARIADB_USER=fhl"
            - "MARIADB_PASSWORD=123456"
            - "MARIADB_ROOT_PASSWORD=123456"
```

URL
   - `http://47.108.237.20:10119/`