# Agent微服务架构

- [Agent微服务架构](#agent微服务架构)
  - [High Performance and Presistent Cache](#high-performance-and-presistent-cache)
  - [RPC FrameWork](#rpc-framework)
  - [Daemon Server](#daemon-server)
  - [Driver Server](#driver-server)
    - [Docker](#docker)
    - [k8s](#k8s)
    - [Helm](#helm)
    - [Cgroup](#cgroup)
  - [Exporter](#exporter)
  - [Observerty Scripts](#observerty-scripts)
    - [Docker](#docker-1)
    - [K8s](#k8s-1)

## High Performance and Presistent Cache

- 配置
- 运行时对象

- k,v 存储
- sdk

## RPC FrameWork

- 类似gin

## Daemon Server

- 注册
- Cache初始化
- Plug in/Plug out
  - 分发Agent Guid, Cache Token
  - 管理Driver Server(Stateful)
  - 管理Scripts(Stateless)


## Driver Server

- 依赖注入
- [ ]driver获取工厂化

### Docker

### k8s

### Helm

### Cgroup

## Exporter

## Observerty Scripts

### Docker

### K8s

