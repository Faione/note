# Scheduling 

- [Scheduling](#scheduling)
  - [Container Scheduling](#container-scheduling)
    - [Problem & Background](#problem--background)
    - [Challenges](#challenges)
    - [State-of-the-arts](#state-of-the-arts)
    - [Key insights/ideas/techniques](#key-insightsideastechniques)
    - [Lessons learned from experiments](#lessons-learned-from-experiments)
  - [Kubernetes Scheduling](#kubernetes-scheduling)
    - [Problem & Background](#problem--background-1)
    - [Challenges](#challenges-1)
    - [State-of-the-arts](#state-of-the-arts-1)
    - [Key insights/ideas/techniques](#key-insightsideastechniques-1)
    - [Lessons learned from experiments](#lessons-learned-from-experiments-1)

## Container Scheduling

### Problem & Background

- 容器化环境中的作业调度和编排仍然是一个有待解决的问题

- 考虑了一个典型的场景，其中并发作业被调度在容器化工作负载调度的环境中，客户端发起计算请求，服务器从镜像注册表中提取相关的容器镜像，并启动容器来处理接收到的请求
  - 两种计算成本
    - 容器镜像传输成本
    - 运行容器的宿主机的计算成本


### Challenges



### State-of-the-arts



### Key insights/ideas/techniques

- 在为客户端和服务器匹配计算容量需求的前提下，将总成本最小化



### Lessons learned from experiments


## Kubernetes Scheduling


### Problem & Background



### Challenges



### State-of-the-arts



### Key insights/ideas/techniques



### Lessons learned from experiments
