# Supb容器配置文件


## 模拟服务应用


containers:
  emu-service:
    appkey: emu_service
    parent: ""
    child: ""
    name: ""
    image: jaeger-env
    cid: ""
    guid: ""
    status: NotReady
    portmap:
      "80": "8080"
    envskey:
      SUPB_GUID: "123456"
    cmd:
    - /bin/sh
    - boot.sh
    - hello
  collector:
    appkey: trace_jaeger_collector
    parent: supb_agent
    child: trace_jaeger_client
    name: ""
    image: jaeger-collector
    cid: ""
    guid: ""
    status: NotReady
    portmap:
      "80": "8080"
    envskey:
      SUPB_GUID: "123456"
    cmd:
    - /bin/sh
    - boot.sh
    - hello


模拟服务应用、模拟干扰应用
小车服务、图像处理服务