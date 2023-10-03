# DevContainer

与 github codespace 效果类似，允许用户定义一个 dev container(image or Dockerfile)，插件会首先构造此镜像，然后将 workspace(项目目录) 以及一个存储卷 vscode 挂载到其中，并随后根据 DevContainer 中的定义安装 code server 以及设置的插件

[devcontainer_vscode](https://code.visualstudio.com/docs/devcontainers/containers)
[devcontainer_spec](https://containers.dev/)