# Jaeger搭建
## 一、Jaeger概述
- agent提供library供应用使用，而collector则接收来自agent的数据，并写向后端存储，本身不做业务处理  
- agent与应用强绑定，collector与后端存储方式强绑定，而agent与collector弱绑定(并不一定在一个节点上)  
- 因此，对于存储的配置，应当写在collector的配置之中，从而agent与存储方式解耦

## 二、Jaeger搭建
### (1) 使用 docker-compose
[官方yaml文档](https://github.com/jaegertracing/jaeger/blob/master/docker-compose/jaeger-docker-compose.yml)

```yml
version: '2'

services:
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
 
    jaeger-collector:
      image: jaegertracing/jaeger-collector
      command: 
        - "--cassandra.keyspace=jaeger_v1_dc1"
        - "--cassandra.servers=cassandra"
        - "--collector.zipkin.host-port=9411"
        - "--sampling.initial-sampling-probability=.5"
        - "--sampling.target-samples-per-second=.01"
      environment: 
        - SAMPLING_CONFIG_TYPE=adaptive
      ports:
        - "14269:14269"
        - "14268:14268"
        - "14250"
        - "9411:9411"
      restart: on-failure
      depends_on:
        - cassandra-schema

    jaeger-query:
      image: jaegertracing/jaeger-query
      command: ["--cassandra.keyspace=jaeger_v1_dc1", "--cassandra.servers=cassandra"]
      ports:
        - "16686:16686"
        - "16687"
      restart: on-failure
      depends_on:
        - cassandra-schema

    jaeger-agent:
      image: jaegertracing/jaeger-agent
      command: ["--reporter.grpc.host-port=jaeger-collector:14250"]
      ports:
        - "5775:5775/udp"
        - "6831:6831/udp"
        - "6832:6832/udp"
        - "5778:5778"
      restart: on-failure
      depends_on:
        - jaeger-collector

    cassandra:
      image: cassandra:4.0

    cassandra-schema:
      image: jaegertracing/jaeger-cassandra-schema
      depends_on:
        - cassandra
    ```

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
  kibana:
    image: "kibana:7.10.1"
    ports: 
      - "5601:5601"
    environment: 
      ELASTICSEARCH_HOSTS: http://es:9200
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
      - "SPAN_STORAGE_TYPE=elasticsearch"
      - "ES_SERVER_URLS=http://es:9200"
      # tags 也作为field，便于在 es 中进行聚合分析时根据 tag 分析 
      - "ES_TAGS_AS_FIELDS_ALL=true"
    depends_on: 
      - es
    restart: on-failure

  jaeger-query:
    image: "jaegertracing/jaeger-query"
    ports: 
      - "16686:16686" 
      - "16687"  
    environment: ··     - "SPAN_STORAGE_TYPE=elasticsearch"
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

```yml
version: "3"
services: 
  es:
    image: "elasticsearch:7.14.1" 
    ports: 
      - "9200:9200"
      - "9300:9300"
    environment: 
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"  
      - "discovery.type=single-node"
    volumes: 
    # 注意需要给"/data/docker/es/data" 赋予777权限，否正es会启动失败
      - "/data/docker/es/data:/usr/share/elasticsearch/data"
      
  kibana:
    image: "kibana:7.14.1"
    ports: 
      - "5601:5601"
    environment: 
      - ELASTICSEARCH_HOSTS=http://es:9200

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
      - "SPAN_STORAGE_TYPE=elasticsearch"
      - "ES_SERVER_URLS=http://es:9200"
      # tags 也作为field，便于在 es 中进行聚合分析时根据 tag 分析 
      - "ES_TAGS_AS_FIELDS_ALL=true"
    depends_on: 
      - es
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