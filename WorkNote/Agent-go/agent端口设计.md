# Agent端口设计

## 端口说明

agent:
   - agent自身使用的端口: 10010 - 10019
   - agent插件使用的端口: 10030 - 10999


## agent端口

agent-collector
   - 10011

## 插件端口
es:
   - 10030
   - 10031

kibana
   - 10033

jaeger-query
   - 10032

jaeger-env
   - 10034:5775
   - 10035:6831
   - 10036:6832
   - 10037:5778


gogs 10118 10119
