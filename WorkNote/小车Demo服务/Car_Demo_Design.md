# 小车 Demo 设计

## 整体概览

Web UI
   - 提供 web ui 供用户操作
   - Web UI 基于浏览器, 无法插入trace, 因此也不会出现在tupo中

Service
   - frontend
      - 接收来自UI的用户请求
      - 将请求发送给对应的执行对象  
   - engine
      - 接收frontend的操控指令
      - 执行实际的运动控制
   - camera
      - 接收frontend的启动指令
      - 发送请求给 image_processer, 携带目标地址
      - 抓取图片并发送给 image_processer
   - image_processer
      - 接收camera的连接指令
      - 处理图片并发送到camera要求的地址   

## Tupo

frontend、engine、camera既可以微服务化, 也可以作为小车Demo程序的子模块

### (1) 当前Tupo

- 视为子模块Tupo

```
Demo -> DarkNet
```

### (2) 微服务Tupo

- 视为微服务Tupo

```
frontend -> engine

         -> camera -> DarkNet
```

### (2) 端到端追踪Tupo

当前图片传输为线性流程, Demo 将图片发送至 DarkNet, DarkNet再将图片发送给 Web UI，请求没有闭环

- 视为子模块Tupo

```
Demo -> DarkNet -> UI 
```

- 视为微服务Tupo

```
frontend -> camera -> DarkNet -> UI

         -> engine
```

## 功能需求

当前数据传输均是单向，不存在返回，因而构成的 span 只有时间上的连续，而不存在包含关系, 而为实现整条链路的追踪，需要在 图片抓取、发送、处理、展示 各个阶段中增加返回操作

### (1) nnmsg 回写通道

### (2) 帧追踪流程

区别与以用户为起始点, 帧追踪以 camera 为起始, 以用户最终确认看到为终止 构成一个完整的trace, 该 trace可为如下两种流程
   - 帧追踪可作为单独的一个功能区别于原来的过程

- 栈式响应

Demo -> DarkNet -> Web UI 
Demo <- DarkNet <- Web UI

需要提供基于nnmsg, websock 的通用 "请求 -> 响应" 方案

- 环式响应

Demo -> DarkNet -> Web UI -> Demo

保留原始方案, camera 提供api给 Web UI 调用, 图片中需要增加是否追踪的标识


### (3) 其他需求

- DarkNet镜像可以适度的缩小体积, 方便可能的迁移

- Demo程序需要适当的调整以接入 camera 程序

- 增加更多的埋点位以提供更丰富的trace信息


### 

保留流程不变
图片加序号


图像处理服务更加通用
   - 提供接口, 启动控制, 告知处理之后的图片所能取的地址

camera服务
   - 提供接口, 启动控制, 告知前端取图片的地址

异步的 msg ack
   - 参考 tcp 链接 ack
   - 异步的span追踪 


提供云服务 trace 接入规约
/root/boot.sh
  - 自己开发的都需要进行埋点


使用队列存储请求以及span, 等待响应后结束span






