# Network


## Rootless

slirp是一种网络协议栈，用于为虚拟机提供网络连接。当主机没有直接物理网络连接可供虚拟机使用时，可以使用slirp网络协议栈来提供网络访问, 而一般通过 `libslirp` 库来实现用户态的协议栈处理, 该库通常用于 qemu 中的网络虚拟化

对于 `rootless` 容器, podman 使用 `slirp4netns` 来实现容器网络. `slirp` 是用户态网络栈的实现, 而 `slirp4netns` 会在 容器/pod 的 netns 中创建一张 `tap0` 网卡, 用来接收网络包数据, 同时会在 host 上启动一个进程, 用于接收 `tap0` 网卡的网络包, 并通过host网卡发送, 而当host上接收到数据是, 会在 `slirp4netns` 中进行协议栈处理, 通过 `tap0` 返回给容器

slirp4netns 源代码中主要有两个部分

main 中哦会通过 `socketpair` 函数创建一对 sock 用于父子进程之间的信息传递, 随后则进行 fork, 在子进程中执行 `child()` 方法, 首先会通过 `nsenter` 进入目标命名空间, 并创建 `tap0` 网卡, 同时将网卡的 fd 通过 sock 发送给父进程, 一切完毕之后, 子进程退出.

父进程会一直等待直到子进程退出, 在检查子进程执行状态正确后, 执行 `parent` 方法, 其中首先会从 sock 中读取 tapfd, 按照配置进行一系列操作后, 进入 `do_slirp` 主循环

`slirp` 主循环主要进行如下工作
- 初始化队列, 缓存
- 不断尝试从 `tapfd` 中读取数据, 并将数据通过 `slirp_input` 进行处理


简单而言, `slirp4netns` 通过一个在容器 net ns 中的 tap0 设备, 与在 host 中的进程一同来为容器提供网络支持 


[^1]: [slirp4netns_source_code](https://github.com/rootless-containers/slirp4netns)