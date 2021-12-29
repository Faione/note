# Jaeger Span 中嵌入 GUID 信息

Span数据结构中的成员变量Process标识了追踪主体的应用程序的信息
   - ServiceName: 用户定义的进程名称
   - Tags: 可附加的KeyValues信息

## 容器 Guid 与 Span 数据绑定流程

1. * agent启动时，初始化 Jaeger Env, 并通过环境变量告知Span数据传出的URL
   
2. * agent收到启动命令，选择对应的容器镜像进行注册与启动
    - 分离注册 与 启动
   
3. * 注册完成之后，将得到 Guid 以环境变量 SUPB_GUID 的形式传入容器之中，同时配置Jaeger环境变量与 Jaeger Env 相通
   
4. * 容器中初始化tracer时，读取环境变量 SUPB_GUID，并添加到Process中
   - 当前是在用户程序中嵌入代码，读取环境变量并向Process添加
   - 后续：将此流程移动到Jaeger Client中，用户只需要导入修改过的Jaeger Client，就能实现此功能
      - Go版本 

5. * Span数据产生后，首先发送到Jaeger Env，并通过 jaeger-collector-agent-plugin 发送到Agent
   - 当前 plugin 将据直接发送给agent，agent则需要对数据进行解析
   - 后续：plugin 取出Span中的Guid信息，作为路径参数/request参数与Span数据一同发送给Agent
   
6. * Agent收到Span数据，解析并读出Span.Process中的GUID信息，以此对Span数据进行分类
   - agent不解析Span，而通过请求中的guid信息进行分类，并将span数据直接转发
   
7. Agent接收Stratege发送的监控命令，将指定Guid的Span数据发送到总线的指定Topic中
   
8. Stratege监听Topic，将Span数据存入后端ElasticSearch数据库
   
9.  数据最终通过Jaeger Query进行查询与展示
   - 提供 InitJaegerQuery 函数，启动Query UI，并通过环境变量链接到指定的 ElasticSearch 数据库

提供
  - Supb Jaeger Client

