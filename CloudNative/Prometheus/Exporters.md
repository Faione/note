# Prometheus Exporters

- [Prometheus Exporters](https://blog.51cto.com/erdong/4770829)

## Node Exporter

- [Node Exporter](https://github.com/prometheus/node_exporter)
- 可设置日志的格式为 json，但无法控制 metric 的格式

```shell
# after download 
$ ./node_exporter
```

## eBPF Exporter

- [eBPF io](https://ebpf.io/)
- [eBPF Exporter](https://github.com/cloudflare/ebpf_exporter)


### eBPF

- Berkeley Packet Filter
  - 类 Unix 系统上数据链路层的一种原始接口，提供原始链路层封包的收发
  - tcpdump
    - 截取网络分组，并输出分组内容

- extended Berkeley Packet Filter
  - Linux 系统的观测工具
  - eBPF 是一套通用执行引擎，提供了可基于系统或程序事件高效安全执行特定代码的通用能力
  - eBPF 也逐渐在观测（跟踪、性能调优等）、安全和网络等领域发挥重要的角色
  - [eBPF概述](https://developer.aliyun.com/article/779357)

- bcc工具包
  - [BCC](https://github.com/iovisor/bcc)

### 火焰图

- 火焰图是帮助我们对系统耗时进行可视化的图表，能够对程序中那些代码经常被执行给出一个清晰的展现
  - 用来展示内核的程序调用栈

