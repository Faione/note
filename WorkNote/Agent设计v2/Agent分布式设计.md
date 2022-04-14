# Agent同步机制

## 技术选型

- 服务发现技术选型
  - ETCD
    - 服务发现
    - 维护全局 prometheus 配置
    - 存储全局 collector 配置
- 局域网通信技术
  - http
    - 暂时提供 Sync 方法
  - gRPC
 
- 安全机制
  - tls