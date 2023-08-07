- 壮壮
    - agent 对接 sponge 部分
        - 注册
           - 根据注册的对象，获得相应的注册信息   
        - agent 启动 ，为自己注册 guid 
           - superbahnAgent\internal\supbagent\root\root.go
           - container 启动， 为container 注册 guid 
        - Host，构造 Host Manager 时进行注册
            - 初期可以与agent使用同一个guid(agent使用host信息进行注册)
        - 心跳
           -  定时向sponge汇报自己以及管理的容器(暂时只收集容器)的信息
           -  internal\supbagent\plugins\heartbeat
        - 注销
           - 删除容器时调用 
           -  pkg\supbagent\resources\manager_containers\containers_manager.go
        - 重连  
           - 暂时不需要提供 

注册信息参考，具体需要参考当前RPC与桂老师的设计

```
info: 
   Host:host_name+mac
   Containter:镜像名称 + 随机数

type: services_container / agent / strategy _container

// 支持监控、控制的描述
mod: none /  collect  / control / collect_control 

// 宿主信息
host: none / guid

// 关联关系注册的需要
otherInfo:
    appKey:	 
    parentApp: 
    childApp: 
```