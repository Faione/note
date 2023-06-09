# Expended Apps

## Apps

|               |         |                |           |
| :-----------: | :-----: | :------------: | :-------: |
| Key-Value Db  |  redis  |     keydb      | memcached |
|     RBDMS     |  mysql  |   clickhouse   |           |
|   NoSQL Db    | mongoDB | elasitc search |           |
| Message Queue |  kafka  |                |           |
|    Server     |  nginx  |
|    BigData    |  Spark  |      Hive      |           |

常规应用基本都包含在 docker.io/library 中, 常见的部署方案可基于 bitnami [^1] 的开箱即用方案

大数据应用相对复杂, 主流 Spark 可以在 bitnami [^1] 中找到开箱即用的方案, 但相对更复杂的 hadoop 则可以参考 big data eu [^2] 这个组织的仓库


## Benchmark


memtier_benchmark: 一个通用的 kv 数据库压测工具, 底层兼容 redis/memcached 的协议, 可充当两者的 client 并按照所设置的方案进行压力测试


[^1]: [bitnami_containers](https://github.com/bitnami/containers)
[^2]: [big_data_europe](https://github.com/big-data-europe)