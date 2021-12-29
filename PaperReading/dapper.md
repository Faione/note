# Paper： 

## 描述性信息 
1. 题目：
   - Dapper, a Large-Scale Distributed Systems Tracing Infrastructure 
2. 会议或期刊：
   1. Google Technical Report 
3. 作者：
   1. Benjamin H. Sigelman, Luiz Andre Barroso, Mike Burrows, Pat Stephenson,Manoj Plakal, Donald Beaver, Saul Jaspan, Chandan Shanbhag 
4. 所属研究团队：
   1. google
5. 论文所属领域: 
   1. distributed system, tracing system, monitoring platform

## 内容 
1. 应用场景 
   1. 分布式系统跟踪
2. 研究问题 
   1. 跟踪系统的泛用性与持续性
      - 泛用性: 即使是系统的很小一部分不被监控，跟踪系统的有用性也会收到很大影响
      - 持续性: 监控系统需要始终启动，因为不寻常或其他值得注意的系统行为往往难以复现
   2. 跟踪系统的三个要求
      - 低占用: 很小的监控开销对于高度优化的服务应用来说也是显而易见的，甚至阻碍了用户对于监控系统的使用
      - 应用级透明: 依赖开发者主动适配的跟踪系统十分脆弱且容易崩溃，违背了泛用性
      - 伸缩性: 追踪系统能够满足服务未来的扩展和集群规模的增长
   3. 快速分析
      - 追踪数据能够快速的应用在分析上，理想情况是一分钟以1内
      - 快速的分析新数据，使得对生产异常的反应更加迅速
3. 相关研究与不足 
4. 本文的贡献
   1. 使用样本采样的方法，提供足够信息的同时，降低性能开销
   2. 实现更高的软件透明度，大规模分布式系统也可以在没有额外的注解的情况下进行跟踪
   3. Adaptive Sampling  
      - 对于每个进程而言，Dapper的开销与进程单位时间内采样的trace数量成正比，采样率高则会影响性能，而采样率低则会错失关键的事件
      - 自适应采样下，采样率基于单位时间内的期望采样数量，而不是均匀的采样率, 低流量的工作负载将自动提高采样率，而那些非常高流量的工作负载将降低采样率，从而保持开销处于控制之下
5. 本文所提方法概述
   1. 真实的应用级延时
      - 限制Dapper核心的实现在随处运行的线程、控制流、以及RPC库中
   2. 伸缩性、低占用
      - 自适应的采样实现 
   3. 追踪树
      - 结点: span
         - 同时也是一个简单的日志记录
            - span的开始与结束时间戳
            - RPC 时间记录
            - 其他注解    
      - 边：span之间的关联关系
      - 其他规约
         - 创建时没有父结点的span称为 root span
         - 属于某一次trace的所有span都共享一个trace id(span id 与 trace id 都是唯一的64b int)
            - 如何产生？ 
         - 通过client和server通信时，请求固有的先后顺序，来确定span时间戳的上界和下界
         - 系统本身不保证时间的同步，因此需要注意服务区之间的时间漂移
     - 生成追踪树
        - 找到每个RPC共有的root span, 以及每层的结点以增加树的深度
   4. 低应用侵入
      - trace context
         - trace context 占用小且易复制，每个trace id都与TLS关联
         - ?TLS: 构造线程独占的变量
         - [Thread Local Storage](https://www.cnblogs.com/stli/archive/2010/11/03/1867852.html)  
      - 透明的异步操作跟踪
         - Google开发者使用一个公有异步操作库来进行Callback的管理与调度，Dapper保证所有的Callback都存储其构造者的trace context, 当Callback回调时，trace context能够与正确的线程关联
      - RPC框架集成
   5. trace信息收集
      - span data 写入到本地的log文件中
      - dapper collector 从所有产生log的host读取span data, 并写入到 Dapper Bigtable 存储中
6. 本文如何验证方法有效性 
7. 本文还有什么不足 
8. 未来的研究方向有哪些 

## 个人 
1. 是否推荐（10分） 
2. 我近期关注的研究问题 
3. 本文和我的研究有什么关系/读文感触 
4. 针对本文我可以做哪些进一步的工作 