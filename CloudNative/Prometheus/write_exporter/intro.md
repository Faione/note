# Metric

## 格式

metric格式[^1]一般为 `<name> {<label>} <value>`，主要由三部分组成
- name: 名称，通常用来唯一标识某一指标，并能一定程度上表达指标的含义，如`http_requests_total`表明此指标为http请求的总量
- labels: 标签，是一组 key="value" 对，为同一个指标提供多维度的信息，可以选择其中的一个或多个维度来对指标进行筛选
- value：值，通常为整数或浮点数，exporter在抓取数据的时候对value进行更新，而name和lalels通常是静态的文本描述信息

```
my_metric{label="a"} 1
```

## 类型

### 基本类型

Metric有四种类型[^2], Counter、Gauge、Histogram和Summary，用于不同数值特征的抓取数据

Counter: 表示单个单调递增的单个数值，对应的value只能增加或是通过重启来清0，如请求的次数，完成任务的数量，错误数量等
Guage: 表示单个数值，能够任意的增加或减少，如当前的温度，内存使用，并发请求的数量等
Histogram: 


### Vec类型

对于每种类型都有对应的Vec, 用来保存相同name而不同label的metric，而不必再一一单独定义


## 采集

exporter中可定义多个metric, 并依靠自己的抓取能力对value进行更新，同时对外暴露metric uri, 以上述格式返回当前metric的信息。而prometheus则通过配置文件，周期性的访问metric uri，将数据采集并持久化到时序数据库中，并提供PromQL来对metric进行查询

[^1]: [prometheus_metric_format](https://prometheus.io/docs/instrumenting/writing_exporters/)

[^2]: [prometheus_metric_types](https://prometheus.io/docs/concepts/metric_types/)

