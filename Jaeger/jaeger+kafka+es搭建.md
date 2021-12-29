# jaeger+kafka搭建
kafka可以作为collector与实际数据库之间的数据缓冲，数据最终仍然需要写入数据库中，kafka不用于存储而用于缓冲

[配置参考](https://juejin.cn/post/7015416476446228494)  

## 使用 docker-compose 搭建

```yml
version: "3"
services: 
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
      - "./es/data:/usr/share/elasticsearch/data"

  logstash:
    image: "logstash:7.10.1"
    container_name: logstash
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - ./logstash/pipeline/:/usr/share/logstash/pipeline/
      - ./logstash/config/:/usr/share/logstash/config/
    restart: on-failure
    depends_on:
      - es
      - jaeger-collector

  jaeger-agent:
    image: "jaegertracing/jaeger-agent" 
    ports: 
        - "5775:5775/udp"
        - "6831:6831/udp"
        - "6832:6832/udp"
        - "5778:5778"
    # 数据最终给到collector，并由其发送给数据存储中心
    command: ["--reporter.grpc.host-port=jaeger-collector:14250"]
    restart: on-failure
    depends_on: 
      - jaeger-collector
      
  jaeger-collector:
    image: "jaegertracing/jaeger-collector"
    ports:
      - "14269"
      - "14268:14268"
      - "14250"
      - "9411:9411"
    environment: 
    # 配置使用kafka缓存
      - SPAN_STORAGE_TYPE=kafka
      - KAFKA_PRODUCER_BROKERS=152.136.134.100:9092
      - KAFKA_TOPIC=jaeger_kafka_test
    restart: on-failure
  
  jaeger-query:
    image: "jaegertracing/jaeger-query"
    ports: 
      - "16686:16686" 
      - "16687"  
    environment: 
      - "SPAN_STORAGE_TYPE=elasticsearch"
      - "ES_SERVER_URLS=http://es:9200" 
       
      # 配置agent以进行收集trace数据
      - "JAEGER_AGENT_HOST=jaeger-agent"
      - "JAEGER_AGENT_PORT=6831"
    restart: on-failure
    depends_on: 
      - es

  # 测试jaeger的程序
  hotrod:
      image: jaegertracing/example-hotrod:latest
      ports:
      - '8080:8080'
      - '8083:8083'
      command: ["-m","prometheus","all"]
      environment:
      - JAEGER_AGENT_HOST=jaeger-agent
      - JAEGER_AGENT_PORT=6831
      - JAEGER_SAMPLER_TYPE=remote
      - JAEGER_SAMPLING_ENDPOINT=http://jaeger-agent:5778/sampling
      depends_on:
      - jaeger-agent
```

- 存在问题
1. kafka收发缺少
2. kafka格式解析