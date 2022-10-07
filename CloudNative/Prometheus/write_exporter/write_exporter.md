# Write Exporter

- [tuitorial](https://prometheus.io/docs/instrumenting/writing_exporters/)
- [example-haproxy](https://github.com/prometheus/haproxy_exporter/)
- [go client blog](https://mojotv.cn/go/prometheus-client-for-go)

## 

- Exporter接口
  - Describe
    - 获取metric信息
  - Collector
    - metric信息+值

```shell
$ docker run -d -p 27182:9091 prom/pushgateway
```