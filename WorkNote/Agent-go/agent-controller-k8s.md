
- deployment、service、pod CURD
  - 聚合简单
  - 用于agent本身处理聚合查询的请求，如心跳等
  - 控制中心可以不提供 k8s 风格的配置文件，由agent进行适配
- Object CURD
  - 聚合困难
  - 用于控制中心直接的配置文件控制
  - 控制中心必须提供完整的 k8s 风格的配置文件


