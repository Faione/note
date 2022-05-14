# 片上互联网络

## 互联网络结构

- 拓扑
- 路由
- 流量控制
- 路由器微体系结构
- 链路微体系结构

## 网络拓扑特性

- 网络直径(Diameter)
- 路由距离(Routing Distance)
- 平均距离(Average Distance)
- 网络分割(Partition)
- 等分带宽(Bisection Bandwidth)


## 传输数据

- Message
  - Packet：路由与顺序化的基础单元，大小在 64b - 64KB
    - Flit(flow control digit)：带宽/存储分片的最小单元，同一个packet中的Flit使用相同的路由，使用Flit以适应可变的Packet大小
      - Phit(physical transfer digit)：单个时钟内传输的数据

![message、packet、flit、phit](./img/2022-05-14-10-00-37.png)

## 路由算法

- 选择一条数据包从源节点到目的节点的传输路径

## 流量控制

- 在数据包传输的过程中，进行相关资源(缓冲区、传输链路、控制状态)分配的方法