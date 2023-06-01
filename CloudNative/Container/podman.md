# Podman

## Diff

尽管podman不需要docker daemon 这样的常驻后台进程,但仍会为每个容器创建一个 `conmon` 守护进程, Conmon在容器中运行，协助容器与宿主机之间通信，并负责容器日志记录、镜像存储、网络配置和容器生命周期管理等任务.


Conmon是一个用于管理运行时容器的守护进程，可以将它看作是与容器运行时（如Docker或CRI-O）一起使用的辅助程序。Conmon在容器中运行，协助容器与宿主机之间通信，并负责容器日志记录、镜像存储、网络配置和容器生命周期管理等任务。

Conmon启动后会与容器运行时进行通信，并监听Unix套接字，以便容器运行时可以通过该套接字向Conmon发送命令。例如，当需要创建或销毁容器时，容器运行时就会向Conmon发送相应的指令。Conmon还将容器中的标准输入、输出和错误流定向至宿主机上的文件，以便用户可以查看容器日志，并且它还会为每个容器分配独立的网络命名空间，以便容器可以与宿主机隔离并拥有自己的IP地址。

总之，Conmon提供了一个轻量级而高效的方式来管理容器，这大大简化了容器的管理和部署过程。

## Pod

[^1]: [podman_network](https://github.com/containers/podman/blob/main/docs/tutorials/basic_networking.md)