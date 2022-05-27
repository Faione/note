# 面向云原生的组合工具与一站式可观测性方案

## 云原生的"瑞士军刀"

- cgroup, docker, kubernetes, helm
- 一种通用的方式: http
  - 非常灵活，但需要进行相应的配置
  - 输入、输出的编码、解析不便,需要进行相应的封装
- 另一种方式: client/SDK
  - 官方提供的封装

## 可观测性方案

- metric、log、trace

- 原生可观测性
  - opentelementry
- 非原生可观测性
  - 