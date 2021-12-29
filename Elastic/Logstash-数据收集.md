# Logstash数据收集
## 一、概述
Logstash收集日志数据，并最终写向es数据库，logstash能够配置多种不同的数据输入源，同时能够搭配filter进行数据的过滤  
[ELK-Stach中文指南](https://elkguide.elasticsearch.cn/logstash/get-start/hello-world.html)

## 二、搭建
### (1) 基于 docker-compose
#### 1. docker-compose.yml 文件
```yml
version: "3"
services: 
  logstash:
    image: "logstash:7.10.1"
    container_name: logstash
    volumes:
      - ./logstash/pipeline/:/usr/share/logstash/pipeline/
      - ./logstash/config/:/usr/share/logstash/config/
```

#### 2. pipline
pipline文件夹中包含 *.conf 文件，用以定于logstash的输入输出  

pipline 必须包含两个元素: input 与 output，同时也可包含一个可选项 filter  
> 通过pipline能够定义logstash的数据流出、流出方向，以及可选的过滤操作  
> [pipline配置参考](https://www.elastic.co/guide/en/logstash/current/configuration-file-structure.html) 

- 示例
```log
# 用docker-compose构建，则容器之间通过服务名进行dns
input{
        kafka{
                bootstrap_servers=>"152.136.134.100:9092"
                topics=>["jaeger_kafka_test"]
                group_id=>"jaeger_kafka_logstash"
        }
}
output{
        elasticsearch{
                hosts=>["http://es:9200"]
        }
}
```

#### 2. config
config文件夹中包括 logstash.yml, pipeline.yml, log4j2.properties 文件，三者分别用以对 logstash、pipeline 及日志打印进行配置
- logstash.yml配置
logstash本身的一些参数配置  
>[logstash.yml参考](https://www.elastic.co/guide/en/logstash/current/logstash-settings-file.html)  

```yml

```


- pipeline.yml配置


- log4j2.properties配置