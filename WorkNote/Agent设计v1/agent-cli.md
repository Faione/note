
# Agent CLI

- [Agent CLI](#agent-cli)
  - [(1) 创建](#1-创建)
  - [(2) 查询](#2-查询)
  - [(3) 删除](#3-删除)
  - [(4) 执行方法](#4-执行方法)

agent cli 启动时优先从环境变量中的获得当前的Agent guid

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