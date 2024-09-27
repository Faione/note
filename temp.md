华为云项目所内资源:
1. 数据分析平台 Jupyter Lab:
  - url: http://10.208.130.243:8888/
  - token: f7dd7431c1dbce233bfe0cc9f5516277a6f272bc17784b55
  - 目录说明
    - appProfile: 当前用于进行应用画像，分析的代码
    - document: 相关文档
      - DoubleWeekReports: 双周汇报ppt
      - Metrics: 当前支持的指标及其说明
      - Papers: 相关论文
      - PreWorks: 所内相关工作
2. 数据展示平台 Grafana:
  - url: http://10.208.130.243:3001/
  - uname/passwd: admin/admin
  - DashBoards
    - ALL IN ONE!: 展示所有指标
    - Application: 展示app QoS指标
    - Host: 展示宿主机指标
    - Node: 同上
    - Offline Analysis: 0721竖亥benchmark数据展示
    - VM: 展示虚拟机指标
3. 数据查询平台 Prometheus:
   - url: http://10.208.130.243:9090/
   - 使用参考: https://prometheus.io/docs/prometheus/latest/querying/examples
   - 指标参考 Jupyter Lab 中的 Metrics 或 Grafana 中的正在使用的 Metric
4. 代码仓库
   - 内部仓库: http://10.208.130.243:3000/explore/repos
   - mirror仓库: 
     - AppProfile: https://github.com/Faione/WorkloadAnalysis
     - Grafana Dashboards: https://github.com/Faione/grafana_dashboards
5. 镜像仓库
   - Harbor: https://10.208.130.243/
   - uname/passwd: admin/Harbor12345
6. 服务器信息
   - Master: 运行分析平台，展示平台，查询平台以及代码，镜像仓库，发起业务负载
     - 10.208.130.243
   - Worker: 运行虚拟机，业务程序
     - 10.208.129.2

设置 editor.fontLigatures 以启用 vscode 连字


操作系统的8个重要问题
1. 可扩展性问题
2. 安全可信问题
3. 能效问题
4. 移动计算问题
5. 并行计算问题
6. 分布式计算问题（CAP）
7. 非易失性问题
8. 虚拟化问题