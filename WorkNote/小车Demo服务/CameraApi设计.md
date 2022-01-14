# Camera Service 功能设计


## 一、功能需求

### (1) 启动开关

`/camera/start?addr="10.5.0.35:13131"`

启动开关之后
   - 构造 nnmsg
   - 创建cv
      - 当前: main方法中构造 cv, nnmsg 构造完成之后，每次都用cv获得图片并发送
      - 设计1: cv在启动之后就开始不断的抓取图片，放到一个循环队列中, nnmsg通道建立之后，直接取图片并发送(延迟增加)

追踪设计
  - nnmsg send提供回调, 在回调中进行span的关闭

### (2) 

docker run -itd --rm --privileged -p 10039:8000 -e JAEGER_AGENT_PORT=5775 -e JAEGER_AGENT_HOST=10.16.0.180 -e DARK_NET_HOST=10.118.0.35 car-ctrl-service:v0.1 /bin/bash /root/bo
ot.sh

docker run -it --rm --privileged -p 10039:8000 -e JAEGER_AGENT_PORT=5775 -e JAEGER_AGENT_HOST=10.16.0.180 -e DARK_NET_HOST=10.118.0.35 -e FRAME_RATE=15 car-ctrl-service:latest /bin/bash /root/boot.sh

docker run -itd --privileged -p 10039:8000 -e JAEGER_AGENT_PORT=5775 -e JAEGER_AGENT_HOST=10.16.0.180 -e DARK_NET_HOST=10.118.0.35 -e FRAME_RATE=15 -e SAMPLING_RATE=0.02 car-ctrl-service:latest /bin/bash 

10.30.5.119:10039/car/camera/start


docker run -itd --privileged -p 10050:8000 -e JAEGER_AGENT_PORT=5775 -e JAEGER_AGENT_HOST=10.16.0.180 -e DARK_NET_HOST=10.118.0.35 -e FRAME_RATE=15 -e SAMPLING_RATE=0.02 car-pwm-ctrl-service:latest /bin/bash