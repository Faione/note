[centos7 docker更新](https://www.cnblogs.com/GAO321/p/16723147.html)

注意需要重新启动docker

[升级docker导致runC变化](https://blog.csdn.net/AiL598/article/details/103334232)

[docker容器网络代理](https://blog.csdn.net/styshoo/article/details/106189327)

```shell
# env
docker run --network host --rm -it \
    -e HTTP_PROXY="http://127.0.0.1:7890" \
    -e HTTPS_PROXY="http://127.0.0.1:7890" \
```

```json
# ~/.docker/config.json
{
	"proxies": {
		"default": {
			"httpProxy": "http://127.0.0.1:7890",
			"httpsProxy": "http://127.0.0.1:7890"
		}
	}
}
```

Docker是一种容器化技术，可以在Linux系统上运行容器。容器是一种轻量级的虚拟化技术，可以在单个操作系统内运行多个独立的应用程序。

Docker运行容器的步骤如下：

1.首先，使用Docker镜像创建容器，镜像包含了容器所需的所有程序、配置文件和依赖项。

2.然后，启动容器，并将容器添加到Docker引擎的容器管理器中。

3.接着，Docker引擎会为容器分配CPU和内存资源，并创建容器的网络连接和存储卷。

4.最后，Docker引擎会将容器中的应用程序加载到内存中，并运行容器中的程序。

当您使用 docker run 命令运行容器时，Docker 会执行以下操作：

检查本地主机是否已经存在指定的镜像。如果不存在，Docker 会从镜像仓库中下载该镜像。
创建并启动一个新容器，并从指定的镜像中加载应用程序和依赖项。
将容器的输入/输出连接到本地主机的标准输入/输出设备。
在容器中运行应用程序。