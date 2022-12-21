- [agent源码分析](#agent源码分析)
  - [flow](#flow)
  - [agent 源码](#agent-源码)

## agent源码分析


**flow**

- [x] flow是什么?
- [x] RED对应那些指标?

**架构**

- [ ] agent 如何运行?
- [ ] agent 和server之间有那些服务调用?
- [ ] 数据存放在那里?

**ebpf**

- [ ] 使用了那些 ebpf ? 
- [ ] 对从 ebpf 中采集的数据做怎样的处理?

**其他数据**

- [ ] otel 如何与agent 交换?


### flow


网络中一个 flow 对应一个 TCP/IP 五元组, 应用中一个 flow 对应一个 Request

> TCP/IP 五元组: <source_ip, source_port, dest_ip, dest_port, protocl>

其性能指标为RED(Request、Error、Delay)
- Request: 吞吐量
- Error: 异常
- Delay: 时延

| Field              | DBField      | Type       | Category   | Permission |
| ------------------ | ------------ | ---------- | ---------- | ---------- |
| request            | request      | counter    | Throuthput | 111        |
| response           | response     | counter    | Throuthput | 111        |
|                    |              |            |            |
| rrt                |              | delay      | Delay      | 111        |
| rrt_max            | rrt_max      | delay      | Delay      | 111        |
|                    |              |            |            |
| error              | error        | counter    | Error      | 111        |
| client_error       | client_error | counter    | Error      | 111        |
| server_error       | server_error | counter    | Error      | 111        |
| timeout            | timeout      | counter    | Error      | 111        |
| error_ratio        |              | percentage | Error      | 111        |
| client_error_ratio |              | percentage | Error      | 111        |
| server_error_ratio |              | percentage | Error      | 111        |


### agent 源码


```
===============================================================================
 Language            Files        Lines         Code     Comments       Blanks
===============================================================================
 C                      24        12362         9200         1412         1750
 C Header               28         5851         3352         1809          690
 Dockerfile              1           27           24            0            3
 Makefile                3          242          167           41           34
 RPM Specfile            3          211          173            6           32
 Shell                   1            5            3            1            1
 TOML                    8          216          172           11           33
 XML                     1          122          115            6            1
 YAML                    5          262          199           51           12
-------------------------------------------------------------------------------
 Markdown                6          840            0          723          117
 |- BASH                 2          115           84           19           12
 |- Go                   1            4            4            0            0
 (Total)                            959           88          742          129
-------------------------------------------------------------------------------
 Rust                  199        70637        58448         5543         6646
 |- Markdown            22          104            0           93           11
 (Total)                          70741        58448         5636         6657
===============================================================================
 Total                 279        90775        71853         9603         9319
===============================================================================
```

```
docker run --privileged --network host --rm -it \
    -e HTTP_PROXY="http://127.0.0.1:7890" \
    -e HTTPS_PROXY="http://127.0.0.1:7890" \
    -v $(pwd):/deepflow hub.deepflow.yunshan.net/public/rust-build bash -c \
    "source /opt/rh/devtoolset-8/enable && git clone --recursive https://github.com/deepflowys/deepflow.git /deepflow && cd /deepflow/agent && cargo build"
```