# Intro

## Perf


```json
{
  "core": {
    "events": [
      "instructions",
      "cycles"
    ]
  }
}
```

##

> 使用 `NewMetricWithTimestamp()` 创建的 metric 会带有一个时间戳

cadvisor内置 `housekeeping interval` 定时刷新并根据 `storage_duration` 进行缓存, 而每次采集时, 会从时间序列缓存中取出最新的进行返回, 默认情况下, prometheus会以采集metric的时间戳(如果提供的话)为准, 但在两端时间不一致的情况下会导致prometheus与exporter之间数据的时间差, 为此可以通过 `honor_timestamp` 配置强制使用 promehteus 端的时间戳, 这一定程度上能够解决此问题


        "uid": "d6943a6e-38bf-483b-b138-7074a0bad9f1"
        "uid": "d81ac485-08ce-47e6-a359-0c21bd819a21"