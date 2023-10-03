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
