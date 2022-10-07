# Kibana-数据展示与分析
## 一、概述
kibana可以作为elasticsearch数据库的前端界面，用以直观地展示数据，并对数据进行实时分析

## 二、搭建
### (1) 使用docker-compose

```yml
version: "3"
services: 
  kibana:
    image: "kibana:7.10.1"
    # 提供外部访问的入口
    ports: 
      - "5601:5601"
    environment: 
      # 配置后端存储的es数据库
      ELASTICSEARCH_HOSTS: http://es:9200
```

### (2) 配置kibana中文
[kibana中文](https://blog.csdn.net/weixin_46035332/article/details/113857284)

1. 执行kibana容器的bash
2. 进入config目录下，找到配置文件kibana.yml
3. 添加一行配置

```yml
i18n.locale: "zh-CN"
```
4. 重新启动容器，使得配置被应用