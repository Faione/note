# Prometheus基础

## Metric

- Metric
  - 时间序列的数据
  - prometheus将所有数据存储为时间序列数据
    - 属于同一指标和同一组标记维度的时间戳值流

### Data Model

- 每个时间序列都通过`metric name`与可选的`labels`k-v对进行区分
- metric name 
  - 指定被测量相同的一般性特征
    - http_requests_total
- labels
  - 用于构造Prometheus的维度数据模型
  - 同一metric name的任何给定标签组合标识该metric的特定维度实例化
    - 指定某一label维度

```
<metric name>{<label name>=<label value>, ...}

eg

api_http_requests_total{method="POST", handler="/messages"}
```

### Metric Types

- prometheus client 提供4种基础metric类型

- Counter
  - 计数器是一个累积度量，它代表一个单调递增的计数器，其值只能在重新启动时增加或重置为零
- Gauge
  - 表示可以任意上下的单个数值, 可增可减
- Histogram
  - 对观察结果进行采样，并将它们计入可配置的存储桶中
    - 通常是请求持续时间或响应的大小等
- Summary
  - 对观察结果进行采样（通常是请求持续时间和响应大小等）。虽然它还提供了观察总数和所有观察值的总和，但它计算了滑动时间窗口上的可配置分位数

### Jobs and Instances

- Prometheus 术语中，可以抓取的端称为实例，通常对应于单个进程
  - 具有相同目的的实例集合，例如为可扩展性或可靠性而复制的流程，称为作业