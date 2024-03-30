# Podman

## Diff

尽管podman不需要docker daemon 这样的常驻后台进程,但仍会为每个容器创建一个 `conmon` 守护进程, Conmon在容器中运行，协助容器与宿主机之间通信，并负责容器日志记录、镜像存储、网络配置和容器生命周期管理等任务.


Conmon是一个用于管理运行时容器的守护进程，可以将它看作是与容器运行时（如Docker或CRI-O）一起使用的辅助程序。Conmon在容器中运行，协助容器与宿主机之间通信，并负责容器日志记录、镜像存储、网络配置和容器生命周期管理等任务。

Conmon启动后会与容器运行时进行通信，并监听Unix套接字，以便容器运行时可以通过该套接字向Conmon发送命令。例如，当需要创建或销毁容器时，容器运行时就会向Conmon发送相应的指令。Conmon还将容器中的标准输入、输出和错误流定向至宿主机上的文件，以便用户可以查看容器日志，并且它还会为每个容器分配独立的网络命名空间，以便容器可以与宿主机隔离并拥有自己的IP地址。

总之，Conmon提供了一个轻量级而高效的方式来管理容器，这大大简化了容器的管理和部署过程。

## Pod

[^1]: [podman_network](https://github.com/containers/podman/blob/main/docs/tutorials/basic_networking.md)
[^2]: [podmna_on_alpine](https://wiki.alpinelinux.org/wiki/Podman)


## Podman Arch

podman中所有的运行时依赖都使用 `cmd/podman/registry/registry` pkg 进行管理
- `ContainerEngine`: 容器引擎, 按定义的规范[^1]实现的容器运行时, 如 runc \ crun \ youki 等
- `ImageEngine`: 镜像引擎, 能够根据[^2]中的规范对镜像进行操作, podman在 libpod 中对其进行了实现

registry 中维护了 `ContainerEngine` 与 `ImageEngine` 的全局变量, 同时两者都以 interface 的形式对外提供调用

`ContainerEngine` 的初始化在 `pkg/domain/infra/runtime_abi.go` 中 , 而无论 `ContainerEngine` 还是 `imageEngine`, 都是 `libpod.Runtime` 的包装, 实际上 `libpod.Runtime` 实现了一切功能


`libpod.Runtime` 本身同样由多个 interface 组成
- `State`: 负责管理容器的状态
- `OCIRuntime`: 负责容器的相关操作

`libpod.Runtime` 在 `libpod/runtime.go #299 makeRuntime` 中完成初始化, 其中 `State` 通常为 `libpod/boltdb_state.go`,  通过一个 boltdb 来管理容器的信息

`OCIRuntime` 为 `libpod/oci_conmon_common.go`, podman在初始化时, 会根据配置选择一个可用的容器运行时, 并将其地址保存到 `ConmonOCIRuntime` 中, `OCIRuntime` 通过拼接命令行的形式, 调用容器运行时来完成各种容器操作

podman采用 `DDD` 架构, `Runtime` \ `OCIRuntime` 与 `State` 被进一步封装到 `libpod.Container` 中, start容器的请求到来之后, 主要逻辑会在 `pkg/domain/infra/abi/containers.go` 中进行, 首先通过 namesOrIds 从 boltdb 中 获取容器的相关信息, 并构造 `containerWrapper`, 其中包含 `libpod.Container`, 最后只需要调用相应的方法就可以完成各种容器操作


[^1]: [container_spec_runtime](https://github.com/opencontainers/runtime-spec/blob/main/runtime.md)
[^2]: [opencontainer_image_spec](https://github.com/opencontainers/image-spec/blob/main/spec.md)


## Container Life Circle

start cmd
  -> init -> create -> start conmon -> start container

exit
  -> conmon exit -> podman cleanup


## Settings

podman 启动 pod 时依赖 `pause` infra 容器，4x版本中已将此容器内置，早期版本则需要从 `k8s.gcr.io` 中获取， 为解决 404 问题，需要对 `/usr/share/containers/containers.conf` 中 `infra_image` 进行修改， 如使用 docker hub 中的 `docker.io/dyrnq/pause:3.3`

[change_default_infra_container](https://serverfault.com/questions/1080486/how-to-change-the-default-infra-container-in-podman)



todo: [user-mode](https://docs.podman.io/en/latest/markdown/podman-run.1.html#userns-mode)


## Podamn Pause

Podman中的使用的pause容器为[catatonit](https://github.com/openSUSE/catatonit), 在创建容器时，由podman进行构建(较高版本)[build pause](https://github.com/containers/podman/blob/413819de0747b74219ec68f5a61e241886d10387/pkg/specgen/generate/pause_image.go#L48),其在进行一系列初始化操作后，进入为一个循环的核心逻辑，循环中会调用 `read` 并陷入等待信号的状态，此时不会在调度队列上，也几乎不会占用资源，仅作为一个cgroup与namespace的维护者， 标志Pod的生命周期

## Podman Storage

podman storage config
- runroot: 零时的容器存储目录
- graphroot: 可读可写的容器镜像存储目录
- imagestore: 从graphroot中分离出来的，专门用于存储容器镜像的目录

podman提供`imagestore`的目的在于允许用户将运行容器与存储镜像进行分离，前者对读写速度有要求，可以放置在SSD等高速存储介质上，后者对容量有要求，可以存放在HDD等大容量存储介质上
- 注意: podman并未因此提供`热插拔的`镜像存储机制，后续会分析得出此结论的理由

### imageroot 行为

通过在storage配置文件中声明，或者在命令行中声明， 可以使能`imagestore`功能，此后所有的容器镜像导入会执行如下过程
- 解压容器到`imagestore`中
- 在`graphroot`中通过overlayfs的形式，将`imagestore`对应的镜像层作为底层文件系统
- 在`imagestore`中的`overlay/l`中创建软链接，指向`graphroot`使用overlayfs挂载的可读可写镜像

查看镜像时读取`imagestore`中的数据，而运行容器时则依赖`graphroot`中的可读可写层，于是热插拔时会出现如下问题
- 卸载`imagestore`时，会导致`graphroot`中镜像不完整，容器无法启动
- 迁移`imagestore`时，无效软连接会产生文件无法找到的错误
- 使用 9p 作为文件系统时，由于overlayfs兼容性上的问题，导致podman启动失败，即不能成为 alternativeimagestore 的目录

综上可以认为podman虽然单独区分了镜像存储，但这种区分仅限于可靠的存储设备，即尚不支持可插拔容器镜像存储
