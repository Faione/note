# agent多容器启动方案

## 一、基础

通过调用 docker-compose 指定配置文件来进行多个容器的启动

```shell
# 启动
$ docker-compose -f <filePath> up -d

# 关闭
$ docker-compose -f <filePath> down
```

## 二、启动流程

1. 控制中心发出启动命令, 指定配置文件
   - agent 与 控制中心 通过repo对配置文件进行同步
   - 配置文件最终需要存储在agent中
   - 可通过类似 deployment 来对配置文件进行描述, 约定双方要启动的目标

2. agent收到启动命令, 读取配置文件, 解析出要启动的容器, 并一一进行注册
   - 需要yml文件解析库
   - 解析完成之后, 修改或增加 containerName 条目 

3. agent 执行 docker-compose up
   - 节点中需要有 docker, docker-compose

## 三、关闭流程

1. agent 读取配置文件, 解析出要关闭的容器, 并一一进行注销

2. agent 执行 docker-compose down

3. 执行成功后, agent删除配置文件


