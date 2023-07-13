# Config

通过 ssh config 能够定义一系列登陆脚本, 更方便地在节点间进行登陆

`Host` 代表一个连接块, 可以使用 `name*` 的形式, 将一些公共的逻辑提取放在此处

`SendEnv` 与 `SetEnv` 允许在连接建立时, 为目标 terminal 初始化一组环境变量, 前提是目标主机的 sshd_config 中, 配置了对应的 `AcceptEnv`

[^1]: [ssh_client_config](https://www.ssh.com/academy/ssh/config)