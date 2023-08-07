


## relative_docs

[bao's_blog](https://justadogistaken.github.io/posts/handle-interference/)
[ali_cache_isolation](https://www.alibabacloud.com/help/zh/ack/ack-managed-and-ack-dedicated/user-guide/resource-isolation-based-on-the-l3-cache-and-mba)
[bytedance_rdt](https://www.intel.cn/content/www/cn/zh/customer-spotlight/cases/bytedance-performance-evaluation-optimization.html)


Alioth: A Machine Learning Based Interference-Aware Performance Monitor for Multi-Tenancy Applications in Public Cloud  
[yunlong_chen](https://www.ipdps.org/ipdps2023/2023-advance-program.html)

## Tools
[intel_vtune_profiler](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html)

## VM vs Container

Redis

VM

```
8         Threads
50        Connections per thread
20        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec 
----------------------------------------------------------------------------------------------------------------------------
Sets         1506.40          ---          ---        24.84894        26.75100        59.90300        77.31100       115.89 
Gets        14967.33         0.00     14967.33        24.20363        26.49500        40.95900        49.40700       583.24 
Waits           0.00          ---          ---             ---             ---             ---             ---          --- 
Totals      16473.73         0.00     14967.33        24.26264        26.49500        41.21500        59.64700       699.13 
```

Container

```
8         Threads
50        Connections per thread
20        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec 
----------------------------------------------------------------------------------------------------------------------------
Sets        10129.37          ---          ---         3.70090         3.15100         6.04700        64.76700       779.87 
Gets       101195.35         0.00    101195.35         3.57971         3.15100         5.95100        16.51100      3942.21 
Waits           0.00          ---          ---             ---             ---             ---             ---          --- 
Totals     111324.72         0.00    101195.35         3.59074         3.15100         5.95100        16.89500      4722.08
```


VM on Bridge

```
8         Threads
50        Connections per thread
20        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec 
----------------------------------------------------------------------------------------------------------------------------
Sets         5271.62          ---          ---         6.96790         6.65500        14.84700        21.88700       405.70 
Gets        52616.79         0.00     52616.79         6.89905         6.65500        13.31100        21.11900      2049.86 
Waits           0.00          ---          ---             ---             ---             ---             ---          --- 
Totals      57888.41         0.00     52616.79         6.90532         6.65500        13.37500        21.11900      2455.56 
```

```
8         Threads
50        Connections per thread
20        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec 
----------------------------------------------------------------------------------------------------------------------------
Sets         6008.77          ---          ---         6.21645         6.04700        14.59100        58.36700       462.42 
Gets        59986.31         0.00     59986.31         6.04082         6.01500        14.20700        20.09500      2337.01 
Waits           0.00          ---          ---             ---             ---             ---             ---          --- 
Totals      65995.07         0.00     59986.31         6.05681         6.01500        14.27100        20.99100      2799.43 

```


libvirt
- 可配置的perf事件
  - "virsh perf --enable/--disable"
- 同步内存监控间隔, 同步 scrape time 到内存数据刷新间隔上
  - "virsh dommemstat 17 --period 5"