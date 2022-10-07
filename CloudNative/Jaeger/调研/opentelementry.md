- [opentelementry](https://opentelemetry.io/docs/instrumentation/python/getting-started/)
- [架构简析](https://izsk.me/2021/10/27/OpenTelemetry-Introduct/)
- [架构简析](https://jimmysong.io/opentelemetry-obervability/architectural-overview.html)


## 发展时间线

- Dapper
  - Google Technical Report dapper-2010-1, April 2010
  - 作者: Benjamin H. Sigelman, Luiz Andr´e Barroso, Mike Burrows, Pat Stephenson, Manoj Plakal, Donald Beaver, Saul Jaspan, Chandan Shanbhag
- Opentracing
  - 2016年的12月25日圣诞节，OpenTracing 发布了1.0的版本，提供了面向 Tracing 的规范用于兼容微服务调用之间不同平台的中立 API，之后的2年里，各种外部组件，各种语言，各种框架，不断的贡献到了 OpenTracing 的生态里来，OpenTracing 也成为了 CNCF incubating 的项目
- OpenCensus
  - 2018年的1月17日，谷歌发布 OpenCencus（微软在2018年6月加入） ，作为一款独立于厂商的，面向微服务架构的性能采集和链路追踪平台
  - 从定位上来说，OpenCencus 不仅仅提供 Tracing 标准和 API 规范，还自集成了性能采集的组建，目标是打造一个集性能监控和链路追踪为一体的方案。而在生态上，OpenCensus 直接提供了大部分语言所对应的 SDK 和普遍使用的 Framework 的支持。从此开始，业界对于到底使用 OpenTracing 还是 OpenCensus 开始了一轮又一轮的讨论
- OpenTelemetry 
  - 2019年的5月21日，一条来自谷歌的官方声明传来，OpenCensus 和 OpenTracing 被并入到新的 CNCF 项目，新项目的名字叫OpenTelemetry。而 OpenTelemetry 不仅仅做 Tracing，Metrics，还要针对 Logging 实现类似的中立解决方案，这个方案基本上吃下了排障流程的上中下游，致力于打造全方位的排障定位的规范
- Apache SkyWalking, Zipki, Jaeger
  - 基于 OpenTracing 发展起来的，也有逐步向 OpenTelemetry 拓展的趋势
  - 这些开源组建一般都是从客户端接入开始，同时提供数据收集的方案（Data Collector）和数据处理的方案（Data Aggregator），最后把数据倒入到其他开源组建中，比如 Elasticsearch 和 Cassandra 等

- [沿革简介](https://cloud.tencent.com/developer/article/1805933)
- [opentracing , openCensus -> OpenTelemetry](https://opensource.googleblog.com/2019/05/opentelemetry-merger-of-opencensus-and.html)
- [what is opentelemetry](https://epsagon.com/tools/introduction-to-opentelemetry-overview/)
- [what is opentracing](https://medium.com/opentracing/towards-turnkey-distributed-tracing-5f4297d1736?source=user_profile---------22-------------------------------)
- [jaeger & opentelemetry](https://medium.com/jaegertracing/jaeger-and-opentelemetry-1846f701d9f2)
- [jaeger adaptive sampling](https://medium.com/jaegertracing/adaptive-sampling-in-jaeger-50f336f4334)