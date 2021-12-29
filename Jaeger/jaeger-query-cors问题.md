# Cors问题

[产生原因](https://segmentfault.com/a/1190000012469713/)

web 前端 与 后端 不在同源上(简单理解为不在同一个主机上)

# query cors配置

参考
   - [jaeger query cors issue](https://github.com/jaegertracing/jaeger/issues/2039)

docker run -d --rm --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 14250:14250 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.25 --query.additional-headers "Access-Control-Allow-Origin:*"

注意，不同版本的jaeger，参数格式不同，1.25版本的参数使用 "Key: Value" 形式，其他版本可以从 --help中获得帮助

docker compose 
```yml
version: "3"
services: 
  jaeger-query:
    image: "jaegertracing/jaeger-query"
    ports: 
      - "10032:16686" 
    environment: 
      - "SPAN_STORAGE_TYPE=elasticsearch"
      - "ES_SERVER_URLS=http://152.136.134.100:9200" 
    command: ["--query.additional-headers","Access-Control-Allow-Origin:*"]
    restart: always
```