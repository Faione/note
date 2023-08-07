# v2.1设计

- 思路
  - 以 RPC Server、Http Server 为出发点，基于配置文件定制agent的功能，为控制中心提供远程的间接方法调用
  - 在此基础上，保留心跳以及本地的 guid - object 映射，并尽量通过 guid 而不是特定的索引来对目标进行控制
  - 将 prometheus server、jaeger collector、jaeger agent、vector 等作为 collector，在agent启动时伴随启动，并赋予RPC功能(共享agent guid)

- default 日志硬编码到程序中