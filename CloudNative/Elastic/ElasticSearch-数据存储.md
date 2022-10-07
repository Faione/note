# 基于Docker搭建Es
- [官方参考文档](https://www.elastic.co/guide/en/elasticsearch/reference/6.0/docker.html)  
- [elk+kibana+metricbeat+filebeat使用docker搭建](https://blog.csdn.net/u011665991/article/details/109494752)

## 一、概述
ElasticSearch是一种索引存储的数据库

## 二、使用docker-compose
### (1)) docker-compose.yml 文件配置

```yml
version: "3"
services: 
  # 根据 https://www.jianshu.com/p/ffc597bb4ce8  
  es:
    image: "elasticsearch:7.10.1" 
    ports: 
      - "9200:9200"
      - "9300:9300"
    environment: 
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"  
      - "discovery.type=single-node"
    volumes: 
    # 注意需要给"/data/docker/es/data" 赋予777权限，否正es会启动失败
      - "/data/docker/es/data:/usr/share/elasticsearch/data"
```



