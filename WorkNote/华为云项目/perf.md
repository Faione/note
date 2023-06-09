## metrics

IPC 
User / Sys / IO CPU% 
Instr Cache MPKI | 每千条指令（MPC）中发生的缓存失效次数（KI）的平均值，通常以“每千指令的缓存失效次数”来表示
LLC MPKI | 最后一级缓存(Last Level Cache)每千条指令(Instr)缓存失效(Miss)次数
Memory Capacity (G  B) 
Memory Bandwidth (GB/s)
Disk Bandwidth (MB/s)
Network Bandwidth (Gbps)

IPC/CPI
cache miss
iTLB miss
CPU使用率
内存使用率

pqos

## tools

`perf stat -G`能够计算Cgroup中的IPC 

```shell
perf stat -e instructions -I 1000 -G system.slice/docker-00d6a2eaef2268af48864b52e650667903e959cf89ca50e94e2dad6c7706cc81.scope
```

`/sys/fs/cgroup/cpuacct/{cg}/cpuacct.stat` 可以查看CPU在`user`, `system`, `io_wait` 上的时钟，而 `cpuacct.usage` 可以查看CPU的总时钟


`-e cache-misses -e instructions`可以获得 `cache-misses` 和 `instructinos` 的数量

```
MPKI = L1I 缓存失效总数 / 执行指令总数 * 1000
```

`-e LLC-load-misses -e LLC-loads`可以获得 `LLC-load-misses` 与 `LLC-loads`

```shell
# 查看CPU是否支持LLC计数器
$ perf list | grep LLC
```

```
LLC MPKI = LLC 缓存失效总数 / 执行指令总数 * 1000
```

```shell
sudo perf stat \
  -e instructions \
  -e cache-misses \
  -e LLC-load-misses \
  -e LLC-loads \
  -I 1000 -G fhl.slice
```

sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=18880:8080 \
  --detach=true \
  --name=cadvisor \
  --privileged \
  --device=/dev/kmsg \
  cadvisor:latest


## Perf Exporter

1. 能够进行perf数据采集(受限的, 基于util提供的event), 获取给定 cgroup 中的 perf event 事件计数, 并输出到命令行

2. 能以 server 模式启动, 提供 `add` `del` cgroup 接口, 动态增加计数器, 生成相应的metric指标

3. 能够指定一个root目录, 递归地对其中子目录进行 perf event 采集


```
curl -X POST -H "Content-Type: application/json" -d '{"cgroup": "/sys/fs/cgroup/perf_event/docker/6308ca09cdb3904341decd05233d4696799d5669419af8d92d5ba0801b800f9b"}' localhost:9991/api/v1/collector/perfevent

curl -X POST -H "Content-Type: application/json" -d '{"cgroup": "/sys/fs/cgroup/perf_event/docker/6308ca09cdb3904341decd05233d4696799d5669419af8d92d5ba0801b800f9b"}' localhost:9991/api/v1/collector/perfevent/del

curl localhost:9991/metrics
```


cgroup: 76

host: 55

qos: 

- rps
- latency per request
