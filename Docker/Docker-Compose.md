# Docker Compose
[菜鸟教程](https://www.runoob.com/docker/docker-compose.html)  

## 一、简介
## (1) 概述
Docker Compose是一个工具，能够通过yaml文件配置多个容器，并通过简单的"docker-compose up & docker-compose down"启动与关闭这些容器  

- Docker Compose使用步骤
1. 使用 Dockerfile 定义app的运行环境
2. 在 docker-compose.yaml 中定义app及其所需要的服务(redis、msql或其他微服务) ，使这些服务能够在一个隔离的环境中允许
3. 使用 docker-compose up 启动app依赖的服务以及app本身

## (2) 网络

[docker-compose网络](https://www.jianshu.com/p/c3d264994374)  

默认情况下，compose会为应用创建一个网络，并将所有容器加入到这个网络中，使得容器之间能够相互访问，且还能够以服务名称作为hostname来进行访问

> 服务名称及 servives 下配置的名称，不同于 container_name  


## 二、安装docker-compose
[官方安装指导](https://docs.docker.com/compose/install/)

- 使用pip简易安装

```shell
$ pip install docker-compose

# 测试
$ docker-compose --version  
docker-compose version 1.25.0, build unknown
```

## 三、配置文件
### (1) Dockerfile
Dockerfile是一个文本文件，包含了构建一个镜像所需的指令

- 示例

```dockerfile
# 基于 python:3.7-alpine 镜像构建一个新的镜像
FROM python:3.7-alpine 
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

### (2) docker-compose.yml
- 示例

```yml
version: "3.9"  # optional since v1.27.0
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
      - logvolume01:/var/log
    links:
      - redis
  redis:
    image: redis
volumes:
  logvolume01: {}
```

- 基础用法

```shell
# 依次按照配置启动容器
# docker-compose up -d, 可让将要启动的容器全部后台运行
$ docker-compose up 

# 关闭容器并删除
$ docker-compose down
```
- 参数解释
   1. depends_on
      - 设置容器之间的依赖关系，docker-compose会按照容器之间的依赖关系依次启动容器

- 网桥名称问题
   - 默认网桥名称为 当前 "目录+default" 


