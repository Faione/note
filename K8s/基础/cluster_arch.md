## Controllers

- [controllers](https://kubernetes.io/docs/concepts/architecture/controller/)

在机器人与自动化中，控制回路(control loop)是调节系统状态的非终止回路, 其作用类似于房间中的恒温器
在k8s中，控制器(controller)是监控集群状态的控制回路，并根据需要进行更改或请求更改，每个控制器都试图将集群状变化至接近所要达到的状态

### 控制器模式

控制器至少追踪一种k8s资源类型。k8s中的对象包含标识期望状态的spec(specification规约)字段，而该资源对应的控制器负责让对象当前的状态更接近所要求的状态
控制器可能会自己直接进行相关的操作，但在k8s中，更常见的是，控制器发送消息给能够在边侧产生有效影响的API server
