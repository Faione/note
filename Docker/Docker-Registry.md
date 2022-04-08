# Docker Registry 私有库

- [Docker Registry 私有库](#docker-registry-私有库)
  - [一、基础](#一基础)
    - [(1) 概念](#1-概念)
    - [(2) 上传](#2-上传)
    - [(3) 拉取](#3-拉取)
    - [(4) 存在问题](#4-存在问题)
  - [二、Registry](#二registry)
    - [(1) 说明](#1-说明)
    - [(2) 搭建](#2-搭建)
    - [(3) 接口说明](#3-接口说明)
  - [三、Habor](#三habor)


- [Dokcer 私有库搭建](https://www.cnblogs.com/huanchupkblog/p/10843800.html)
- [Habor 搭建](https://cloud.tencent.com/developer/article/1404719)
- [Docker 私有仓库配置](https://blog.csdn.net/buildcourage/article/details/80296453)

## 一、基础

### (1) 概念

Registry
   - Registry 是一个开源的，无状态的（stateless），高可扩展的（highly scalable）服务器端应用，用来存储和获取你的分布式 Docker 镜像

   - Registry 是一个存储（storage）和内容分发（content delivery）系统，持有命名的（named）Docker 镜像，通过使用不同的标签版本来区分

镜像命名
   - 在 docker 命令中使用镜像名称来反映他们的来源：
      - docker pull ubuntu 表示 docker 从官方的 Docker Hub 中拉取名称为 ubuntu 的镜像。这是命令 docker pull docker.io/library/ubuntu 的简写(Default: docker.io/library)
      - docker pull myregistrydomain:port/foo/bar 表示 docker 从位于 myregistrydomain:port 的仓库中寻找镜像 foo/bar

### (2) 上传

1. docker 通过镜像命名来反应其来源, 因此, 上传镜像时首先需要重新tag
   - 默认 registry_domain 为 "docker.io/library", 默认 tag 是 "latest" 

```shell
# 规范为 "registry_domain/image_name:tag", 如 "39.101.140.145:5000/interference-cpu-core-1:v0.1"
$ docker tag jamming-cpu-core-1:v0.1 39.101.140.145:5000/interference-cpu-core-1:v0.1
```

2. 使用新tag进行上传

```shell
$ docker push 39.101.140.145:5000/interference-cpu-core-1:v0.1
```

### (3) 拉取

1. 拉取镜像

```shell
$ docker pull 39.101.140.145:5000/interference-cpu-core-1:v0.1

$ docker pull 39.101.140.145:5000/cpu-ctrl-core-1

```

2. 运行镜像

```shell
$ docker run -d --rm 39.101.140.145:5000/interference-cpu-core-1:v0.1 /bin/sh /root/boot.sh
```

### (4) 存在问题

1. 不可靠私有仓库问题

```shell
Error response from daemon: Get 39.101.140.145:5000/v1/_ping: http: server gave HTTP response to HTTPS client
```

处理方法
   - 新增或补充配置daemon.json
```shell
# tee: 标准输入复制到每个指定文件，并显示到标准输出 
$ tee /etc/docker/daemon.json << EOF
{ "insecure-registries":["152.136.134.100:10048"] }
EOF

# $ systemctl daemon-reload

$ systemctl restart docker 
```


## 二、Registry

### (1) 说明

docker官方提供的简易镜像存储库

### (2) 搭建

1. 简易搭建

```shell
$ docker run -d -p 5000:5000 --restart always --name registry registry:2 
```

2. 增加安全配置

3. docker-compose

```yml
version: '3'
services:
  docker-register:
    image: "registry:2"
    container_name: "registry"
    ports:
      - "5000:5000"
    volumes:
      - ./registry:/var/lib/registry
    restart: always       
```



### (3) 接口说明 

- [registry api v2](https://docs.docker.com/registry/spec/api/)

1. 查看当前log

```http
http://39.101.140.145:5000/v2/_catalog

->
{"repositories":["interference-cpu-core-1"]}
```

## 三、Habor