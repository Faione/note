# Envoy

Envoy 是一个使用 c++ 编写的反向代理软件，支持L7协议的解析以及负载均衡

对于所支持的 L7 协议解析，Envoy还能够统计详细的Metric信息，以观测服务状态

## L7 解析

Envoy 允许用户编写 Network filters 来对 L7 协议进行解析，从而实现应用层的数据获取，目前支持绝大多数常见的云负载

[^1]: [redis](https://www.envoyproxy.io/docs/envoy/v1.26.1/configuration/listeners/network_filters/redis_proxy_filter)


## 可观测性

对于基础的协议， envoy提供基本的stats[^2]

[^2]: [stats](https://www.envoyproxy.io/docs/envoy/v1.26.1/configuration/listeners/stats)

通常 envoy 内部会周期性地将统计数据转化为metric，以防止占用太多的资源，但相对的会降低实时性，因此可以在 bootstrap 中 打开 `stats_flush_on_admin`, 使得只要访问 admin 接口获取统计信息时，就立刻生成metric

[^3]: [flush_on_admin](https://www.envoyproxy.io/docs/envoy/v1.26.1/api-v3/config/bootstrap/v3/bootstrap.proto#envoy-v3-api-field-config-bootstrap-v3-bootstrap-stats-flush-on-admin)