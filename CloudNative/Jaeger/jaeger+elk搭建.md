# jaeger+elk搭建

## 一、使用 docker-compose
[elk+jaeger基于docker-compose搭建](https://kebingzao.com/2021/01/08/jaeger-es/  
[Filebeat+Kafka+Logstash+Elasticsearch+Kibana](https://juejin.cn/post/7015416476446228494)

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
      - "/data/docker/es/data:/usr/share/elasticsearch/data"
      
  kibana:
    image: "kibana:7.10.1"
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