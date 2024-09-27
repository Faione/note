
## 背景

问题
- 资源利用率
- 用户使用体验

目标
- SLO保障机制

## 国内外研究


|          | 可观测性 | 调度机制 |
| :------: | :------: | :------: |
| 集群维度 |          |          |
| 节点维度 |          |          |

- 节点维度
  - 问题
    - 内核调度机制对应用的资源偏好感知有限
    - 内核的调度机制不够灵活，且修改麻烦
    - 基于资源划分的调度机制不够快速
  - 优势
    - 更靠近设备，更快地获取信息
    - 更细的调度粒度


携带标签的任务被调度 -> 用户态调度程序识别标签，启动eBPF程序收集指标，并提交调度事务 -> 内核调度类调度任务并执行
-> eBPF程序检测到指标劣化，通知用户态调度程序，用户态调度程序执行调度逻辑，并将结果提交给内核调度类

[17]Ousterhout A, Fried J, Behrens J, et al. Shenango: Achieving high {CPU} efficiency for latency-sensitive datacenter workloads[C]//16th USENIX Symposium on Networked Systems Design and Implementation (NSDI 19). 2019: 361-378.
[18]Prekas G, Kogias M, Bugnion E. Zygos: Achieving low tail latency for microsecond-scale networked tasks[C]//Proceedings of the 26th Symposium on Operating Systems Principles. 2017: 325-341.
[19]Delimitrou C, Kozyrakis C. Paragon: QoS-aware scheduling for heterogeneous datacenters[J]. ACM SIGPLAN Notices, 2013, 48(4): 77-88.
[20]Delimitrou C, Kozyrakis C. Quasar: Resource-efficient and qos-aware cluster management[J]. ACM SIGPLAN Notices, 2014, 49(4): 127-144.
[21]Lo D, Cheng L, Govindaraju R, et al. Heracles: Improving resource efficiency at scale[C]//Proceedings of the 42nd Annual International Symposium on Computer Architecture. 2015: 450-462.
[22]Patel T, Tiwari D. Clite: Efficient and qos-aware co-location of multiple latency-critical jobs for warehouse scale computers[C]//2020 IEEE International Symposium on High Performance Computer Architecture (HPCA). IEEE, 2020: 193-206.
[23]Zhou Z, Zhang Y, Delimitrou C. Aquatope: Qos-and-uncertainty-aware resource management for multi-stage serverless workflows[C]//Proceedings of the 28th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 1. 2022: 1-14.
[24]Xiang W, Li Y, Ren Y, et al. Gödel: Unified Large-Scale Resource Management and Scheduling at ByteDance[C]//Proceedings of the 2023 ACM Symposium on Cloud Computing. 2023: 308-323.
[25]Zhang Z, Ramanathan M K, Raj P, et al. {CRISP}: Critical Path Analysis of {Large-Scale} Microservice Architectures[C]//2022 USENIX Annual Technical Conference (USENIX ATC 22). 2022: 655-672.
[26]Wang Z, Zhu S, Li J, et al. DeepScaling: microservices autoscaling for stable CPU utilization in large scale cloud systems[C]//Proceedings of the 13th Symposium on Cloud Computing. 2022: 16-30.
[27]Tang W, Ke Y, Fu S, et al. Demeter: QoS-aware CPU scheduling to reduce power consumption of multiple black-box workloads[C]//Proceedings of the 13th Symposium on Cloud Computing. 2022: 31-46.
[28]Zheng Z, Li X, Tang M, et al. Web service QoS prediction via collaborative filtering: A survey[J]. IEEE Transactions on Services Computing, 2020, 15(4): 2455-2472.
[29]Ghafouri S H, Hashemi S M, Hung P C K. A survey on web service QoS prediction methods[J]. IEEE Transactions on Services Computing, 2020, 15(4): 2439-2454.
[30]Wu D, He Q, Luo X, et al. A posterior-neighborhood-regularized latent factor model for highly accurate web service QoS prediction[J]. IEEE Transactions on Services Computing, 2019, 15(2): 793-805.
[31]Newell A, Skarlatos D, Fan J, et al. RAS: continuously optimized region-wide datacenter resource allocation[C]//Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles. 2021: 505-520.
[32]Gan Y, Liang M, Dev S, et al. Sage: practical and scalable ML-driven performance debugging in microservices[C]//Proceedings of the 26th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. 2021: 135-151.
![![](2023-12-21-12-59-42.png)](image-1.png)
![](image.png)

![](2023-12-21-13-00-55.png)

![](image-2.png)

![](image-3.png)