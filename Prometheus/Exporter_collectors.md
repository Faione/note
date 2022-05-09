# Exporter Collector

- 设置Exporter的collector启动参数可以进行监控项的设置

## 一、Node Exporter

- [node exporter](https://github.com/prometheus/node_exporter)

### (1) Enabled by default

| Name             | Description                                                                                                   | OS                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| arp              | Exposes ARP statistics from `/proc/net/arp`.                                                                  | Linux                                                                                                 |
| bcache           | Exposes bcache statistics from `/sys/fs/bcache/`.                                                             | Linux                                                                                                 |
| bonding          | Exposes the number of configured and active slaves of Linux bonding interfaces.                               | Linux                                                                                                 |
| btrfs            | Exposes btrfs statistics                                                                                      | Linux                                                                                                 |
| boottime         | Exposes system boot time derived from the `kern.boottime` sysctl.                                             | Darwin, Dragonfly, FreeBSD, NetBSD, OpenBSD, Solaris                                                  |
| conntrack        | Shows conntrack statistics (does nothing if no `/proc/sys/net/netfilter/` present).                           | Linux                                                                                                 |
| cpu              | Exposes CPU statistics                                                                                        | Darwin, Dragonfly, FreeBSD, Linux, Solaris, OpenBSD                                                   |
| cpufreq          | Exposes CPU frequency statistics                                                                              | Linux, Solaris                                                                                        |
| diskstats        | Exposes disk I/O statistics.                                                                                  | Darwin, Linux, OpenBSD                                                                                |
| dmi              | Expose Desktop Management Interface (DMI) info from `/sys/class/dmi/id/`                                      | Linux                                                                                                 |
| edac             | Exposes error detection and correction statistics.                                                            | Linux                                                                                                 |
| entropy          | Exposes available entropy.                                                                                    | Linux                                                                                                 |
| exec             | Exposes execution statistics.                                                                                 | Dragonfly, FreeBSD                                                                                    |
| fibrechannel     | Exposes fibre channel information and statistics from `/sys/class/fc_host/`.                                  | Linux                                                                                                 |
| filefd           | Exposes file descriptor statistics from `/proc/sys/fs/file-nr`.                                               | Linux                                                                                                 |
| filesystem       | Exposes filesystem statistics, such as disk space used.                                                       | Darwin, Dragonfly, FreeBSD, Linux, OpenBSD                                                            |
| hwmon            | Expose hardware monitoring and sensor data from `/sys/class/hwmon/`.                                          | Linux                                                                                                 |
| infiniband       | Exposes network statistics specific to InfiniBand and Intel OmniPath configurations.                          | Linux                                                                                                 |
| ipvs             | Exposes IPVS status from `/proc/net/ip_vs` and stats from `/proc/net/ip_vs_stats`.                            | Linux                                                                                                 |
| loadavg          | Exposes load average.                                                                                         | Darwin, Dragonfly, FreeBSD, Linux, NetBSD, OpenBSD, Solaris                                           |
| mdadm            | Exposes statistics about devices in `/proc/mdstat` (does nothing if no `/proc/mdstat` present).               | Linux                                                                                                 |
| meminfo          | Exposes memory statistics.                                                                                    | Darwin, Dragonfly, FreeBSD, Linux, OpenBSD                                                            |
| netclass         | Exposes network interface info from `/sys/class/net/`                                                         | Linux                                                                                                 |
| netdev           | Exposes network interface statistics such as bytes transferred.                                               | Darwin, Dragonfly, FreeBSD, Linux, OpenBSD                                                            |
| netstat          | Exposes network statistics from `/proc/net/netstat`. This is the same information as `netstat -s`.            | Linux                                                                                                 |
| nfs              | Exposes NFS client statistics from `/proc/net/rpc/nfs`. This is the same information as `nfsstat -c`.         | Linux                                                                                                 |
| nfsd             | Exposes NFS kernel server statistics from `/proc/net/rpc/nfsd`. This is the same information as `nfsstat -s`. | Linux                                                                                                 |
| nvme             | Exposes NVMe info from `/sys/class/nvme/`                                                                     | Linux                                                                                                 |
| os               | Expose OS release info from `/etc/os-release` or `/usr/lib/os-release`                                        | _any_                                                                                                 |
| powersupplyclass | Exposes Power Supply statistics from `/sys/class/power_supply`                                                | Linux                                                                                                 |
| pressure         | Exposes pressure stall statistics from `/proc/pressure/`.                                                     | Linux (kernel 4.20+ and/or [CONFIG\_PSI](https://www.kernel.org/doc/html/latest/accounting/psi.html)) |
| rapl             | Exposes various statistics from `/sys/class/powercap`.                                                        | Linux                                                                                                 |
| schedstat        | Exposes task scheduler statistics from `/proc/schedstat`.                                                     | Linux                                                                                                 |
| sockstat         | Exposes various statistics from `/proc/net/sockstat`.                                                         | Linux                                                                                                 |
| softnet          | Exposes statistics from `/proc/net/softnet_stat`.                                                             | Linux                                                                                                 |
| stat             | Exposes various statistics from `/proc/stat`. This includes boot time, forks and interrupts.                  | Linux                                                                                                 |
| tapestats        | Exposes statistics from `/sys/class/scsi_tape`.                                                               | Linux                                                                                                 |
| textfile         | Exposes statistics read from local disk. The `--collector.textfile.directory` flag must be set.               | _any_                                                                                                 |
| thermal          | Exposes thermal statistics like `pmset -g therm`.                                                             | Darwin                                                                                                |
| thermal\_zone    | Exposes thermal zone & cooling device statistics from `/sys/class/thermal`.                                   | Linux                                                                                                 |
| time             | Exposes the current system time.                                                                              | _any_                                                                                                 |
| timex            | Exposes selected adjtimex(2) system call stats.                                                               | Linux                                                                                                 |
| udp_queues       | Exposes UDP total lengths of the rx_queue and tx_queue from `/proc/net/udp` and `/proc/net/udp6`.             | Linux                                                                                                 |
| uname            | Exposes system information as provided by the uname system call.                                              | Darwin, FreeBSD, Linux, OpenBSD                                                                       |
| vmstat           | Exposes statistics from `/proc/vmstat`.                                                                       | Linux                                                                                                 |
| xfs              | Exposes XFS runtime statistics.                                                                               | Linux (kernel 4.4+)                                                                                   |
| zfs              | Exposes [ZFS](http://open-zfs.org/) performance statistics.                                                   | [Linux](http://zfsonlinux.org/), Solaris                                                              |

### (2) Disabled by default

| Name          | Description                                                                                                                                                                   | OS                 |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| buddyinfo     | Exposes statistics of memory fragments as reported by /proc/buddyinfo.                                                                                                        | Linux              |
| devstat       | Exposes device statistics                                                                                                                                                     | Dragonfly, FreeBSD |
| drbd          | Exposes Distributed Replicated Block Device statistics (to version 8.4)                                                                                                       | Linux              |
| ethtool       | Exposes network interface information and network driver statistics equivalent to `ethtool`, `ethtool -S`, and `ethtool -i`.                                                  | Linux              |
| interrupts    | Exposes detailed interrupts statistics.                                                                                                                                       | Linux, OpenBSD     |
| ksmd          | Exposes kernel and system statistics from `/sys/kernel/mm/ksm`.                                                                                                               | Linux              |
| lnstat        | Exposes stats from `/proc/net/stat/`.                                                                                                                                         | Linux              |
| logind        | Exposes session counts from [logind](http://www.freedesktop.org/wiki/Software/systemd/logind/).                                                                               | Linux              |
| meminfo\_numa | Exposes memory statistics from `/proc/meminfo_numa`.                                                                                                                          | Linux              |
| mountstats    | Exposes filesystem statistics from `/proc/self/mountstats`. Exposes detailed NFS client statistics.                                                                           | Linux              |
| network_route | Exposes the routing table as metrics                                                                                                                                          | Linux              |
| ntp           | Exposes local NTP daemon health to check [time](./docs/TIME.md)                                                                                                               | _any_              |
| perf          | Exposes perf based metrics (Warning: Metrics are dependent on kernel configuration and settings).                                                                             | Linux              |
| processes     | Exposes aggregate process statistics from `/proc`.                                                                                                                            | Linux              |
| qdisc         | Exposes [queuing discipline](https://en.wikipedia.org/wiki/Network_scheduler#Linux_kernel) statistics                                                                         | Linux              |
| runit         | Exposes service status from [runit](http://smarden.org/runit/).                                                                                                               | _any_              |
| supervisord   | Exposes service status from [supervisord](http://supervisord.org/).                                                                                                           | _any_              |
| systemd       | Exposes service and system status from [systemd](http://www.freedesktop.org/wiki/Software/systemd/).                                                                          | Linux              |
| tcpstat       | Exposes TCP connection status information from `/proc/net/tcp` and `/proc/net/tcp6`. (Warning: the current version has potential performance issues in high load situations.) | Linux              |
| wifi          | Exposes WiFi device and station statistics.                                                                                                                                   | Linux              |
| zoneinfo      | Exposes NUMA memory zone metrics.                                                                                                                                             | Linux              |

### (3) Config

**Cli options**

- 启动参数中，进行 collector 的配置

```shell
--collector.<name> \n
--no-collector.<name>
```

- 一些collector能够进行更细的指标筛选

```shell
--collector.netclass.ignored-devices 
--collector.tapestats.ignored-devices="^$" 
--collector.systemd.unit-include=".+"
--collector.systemd.unit-include=".+"
--collector.systemd.unit-exclude=".+\\.(automount|device|mount|scope|slice)"

```

**Filtering enabled collectors**

- prometheus server对于 scrapy job 中，配置 collect list

```yaml
params:
collect[]:
    - cpu
```

## 二、Kube State Metric

- [cli options](https://github.com/kubernetes/kube-state-metrics/blob/master/docs/cli-arguments.md)


- 启动参数中配置 metric

```shell

--metric-allowlist string  # 允许的metric
--metric-denylist string 
--metric-annotations-allowlist string  # 允许的附加在resource上的 k8s annotations 
--metric-labels-allowlist string  # 允许的附加在resource上的其他 Kubernetes 标签键
--metric-opt-in-list string  # 增加可选但默认关闭的metric

--namespaces string  # 采集的namespace
--namespaces-denylist string  # 不采集的namespace
--resources string  # 采集的资源
```

- default resource 

```
"certificatesigningrequests,configmaps,cronjobs,daemonsets,deployments,endpoints,horizontalpodautoscalers,ingresses,jobs,leases,limitranges,mutatingwebhookconfigurations,namespaces,networkpolicies,nodes,persistentvolumeclaims,persistentvolumes,poddisruptionbudgets,pods,replicasets,replicationcontrollers,resourcequotas,secrets,services,statefulsets,storageclasses,validatingwebhookconfigurations,volumeattachments"
```