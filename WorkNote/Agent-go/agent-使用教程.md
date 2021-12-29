# Agent使用教程

- [Agent使用教程](#agent使用教程)
  - [一、环境说明](#一环境说明)
  - [二、安装与运行](#二安装与运行)
  - [三、使用agent](#三使用agent)
  - [(1) 创建](#1-创建)
  - [(2) 查询](#2-查询)
  - [(3) 删除](#3-删除)
  - [(4) 执行方法](#4-执行方法)

## 一、环境说明

源码编译要求go环境
> go version >= 1.15

agent启动默认容器时, 需要配置docker私有库
> 稍后

## 二、安装与运行


```shell
# 1. clone 项目
$ git clone https://gitee.com/info-superbahn-ict/superbahn.git supbproject

# 2. 执行编译脚本
$ cd supbproject/scripts/supbagent

$ ./build.sh

# 3. 运行agent
$ ./run.sh
```

run.sh 配置说明
   - 初期直接在脚本中配置, 后续提供配置文件

```shell
# workdir
work_dir="../.."

# server ip, 需要按照本机ip进行配置
ip="172.16.31.37"  
# docker port, 需要按照本机docker暴露的端口进行配置
host="2375"

NERVOUS=${work_dir}/config/nervous_config.json
LOG=/home/logs/control.log

# run
${work_dir}/build/bin/agent   --nvn=$NERVOUS --log $LOG --docker=tcp://${ip}:${host} --supb-collector-url=${ip}:10013 --supb-collector-route="/collector" --jaeger-agent=${ip}:10035
```

## 三、使用agent

agent cli 启动时优先从环境变量中的获得当前的Agent guid, 可以通过获得agent启动时注册的id, 设置环境变量

```shell
$ export SUPB_AGENT=test
```
## (1) 创建

- 创建容器
agent create [-c agent_guid] [-e environment_variable]... [-p ports]... [-n name] image

```shell
# $ ./main agent create -c 0162c01d00 jamming-cpu-core-1:v0.1
$ ./main agent create 39.101.140.145:5000/interference-cpu-core-1

# $ ./main agent create -c 0162c01d00 -e SUPB_T=120 -e SUPB_I=0.04 cpu-ctrl-core-1:v0.1
$ ./main agent create -e SUPB_T=120 -e SUPB_I=0.04 cpu-ctrl-core-1:v0.1
```

## (2) 查询

agent list [-a isAll] [-t objectType]

```
# $ ./main agent list -c 0162c01d00 -a
$ ./main agent list -a
```

agent get [-c agent_guid] [-t type] guid

```
# $ ./main agent get -c 0162c01d00 -t containers 01d6bc9b00
$ ./main agent get -t containers 01d6bc9b00
```

## (3) 删除

agent delete [-c agent_guid] guid

```shell
# $ ./main agent delete -c 0162c01d00 01d6bc9b00
$ ./main agent delete 01d6bc9b00
```


## (4) 执行方法

agent exec [-f funcName] [-g target_guid]  args...

```shell
# 列举支持的方法
$ ./main agent exec -f list_function -g 01d6bc9b00

# 暂停容器
$ ./main agent exec -f stop_function -g 01d6bc9b00

# 恢复容器
$ ./main agent exec -f run_function -g 01d6bc9b00

# 上报信息
$ ./main agent exec -f push_metrics_on_off -g 01d6bc9b00 test_topic

$ ./main agent exec -f push_log_on_off -g 01d6bc9b00 test_topic

$ ./main agent exec -f push_trace_on_off -g 01d6bc9b00 test_topic

# 资源调控
$ ./main agent exec -f get_limitation_config -g 01d6bc9b00

$ ./main agent exec -f set_cpu_ratio -g 01d6bc9b00 0.5

$ ./main agent exec -f set_cpu_sets -g 01d6bc9b00 0

$ ./main agent exec -f set_net_upstream_bandwidth -g 01d6bc9b00 10kbits

$ ./main agent exec -f set_net_latency -g 01d6bc9b00 50ms
```