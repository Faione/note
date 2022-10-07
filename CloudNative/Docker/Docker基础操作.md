# Docker基础操作
## 一、docker run-a stdin: 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；
[菜鸟教程参考](https://www.runoob.com/docker/docker-run-command.html)  

- -d: 后台运行容器，并返回容器ID；

- -i: 以交互模式运行容器，通常与 -t 同时使用；

- -P: 随机端口映射，容器内部端口随机映射到主机的端口

- -p: 指定端口映射，格式为：主机(宿主)端口:容器端口

- -t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；

- --name="nginx-lb": 为容器指定一个名称；

- --dns 8.8.8.8: 指定容器使用的DNS服务器，默认和宿主一致；

- --dns-search example.com: 指定容器DNS搜索域名，默认和宿主一致；

- -h "mars": 指定容器的hostname；

- -e username="ritchie": 设置环境变量；

- --env-file=[]: 从指定文件读入环境变量；

- --cpuset="0-2" or --cpuset="0,1,2": 绑定容器到指定CPU运行；

- -m :设置容器使用内存最大值；

- --net="bridge": 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；

- --link=[]: 添加链接到另一个容器
   - [容器参考](https://www.jianshu.com/p/21d66ca6115e)

- --expose=[]: 开放一个端口或一组端口；

- --volume , -v: 绑定一个卷


## 二、docker exec
此条命令即期望容器执行一条命令，如 "/bin/bash"， 从而生成一个假终端进行交互  
> 此命令失效时，可尝试 "sh"
> 使用export能够查看当前系统的环境变量

## 三、容器通信

用户自定义的网卡可以在容器之间提供自动的 DNS 解析，缺省的桥接网络上的容器只能通过 IP 地址互相访问，除非使用 --link 参数。在用户自定义的网卡上，容器直接可以通过名称或者别名相互解析



docker commit 得到镜像比 Dockerfile得到的更小

docker build -t image:tag <path container Dockerfile>

## 四、远程连接

```
$ vi /lib/systemd/system/docker.service
# add -H tcp://0.0.0.0:2375
# add -H tcp://127.0.0.1:2375
# -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock

# 重载配置信息
$ systemctl daemon-reload

# 重启docker
$ systemctl restart docker 
```

## 五、Docker Pull

pull 指定 digest (获取不同指令集架构镜像)
```shell
$ docker pull ubuntu:latest@sha256:f3113ef2fa3d3c9ee5510737083d6c39f74520a2da6eab72081d896d8592c078
```

## 六、检索

```shell
# 关键词搜索，返回容器id
# $ docker ps -a | awk '/key_word/'
$ docker ps -a | awk '/key_word/{print $1}'

# 检索已经关闭的容器
# docker rm `docker ps -a|grep Exited|awk '{print $1}'`
$ docker ps -a|grep Exited|awk '{print $1}'
```

## 七、查看已终止容器的log信息

- 容器状态为`stop`

```shell
# 获得容器id
$ docker ps -a | grep <target>

# 查看容器信息, 找到 LogPath
$ docker inspect <containerID>

$ cat <logpath>
```


# 赋予当前用户docker权限(minikube不推荐使用root启动)

```shell
$ sudo usermod -aG docker $USER && newgrp docker
```
