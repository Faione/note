# Agent设计说明
## 一、组织结构
## 二、功能需求
## 三、交互格式
1. 上报格式
- 说明
   - 固定字段: 
      - guid: 全局ID，由Sponge生成，唯一标识接入对象  
      - timestamp: 时间戳信息，标识此次上报的时间  
   - 可变字段: 
      - metric: 持续性、可聚合的指标型信息
      - logging: 诊断性的服务、设备调试、错误信息
      - tracing: 进行优化与排查的端到端链路追踪信息 
   - 具体内容:
      - 具体内容均为键值对序列
      - type: 该监控数据所属大类，方便聚合
         - 指定 "Not_AGGREGATED", 则content内容可不必遵守一类的规则，适用于log等信息
      - content: 以键值对的形式存放，具体的监控指标与值

- 范例
```json
{
    "guid": "123456",
    "timestamp": 1628834738016, 
    "metric": [
        {
            "type": "cpu",
            "content": {
                "cpu_core_allocated": 2,
                "cpu_utilization": 0.52
            }
        },
        {
            "type": "memory",
            "content": {
                "memory_allocated": 65536,
                "memory_usage": 37768,
                "memory_utilization": 0.5
            }
        }
    ]
}
```
#### 1.1 Metric上报数据

### 2. 控制格式
- 说明
   - 固定字段: 
      - guid: 全局ID，由Sponge生成，唯一标识接入对象  
      - timestamp: 时间戳信息，标识此次执行控制的时间
   - 可变字段: 
      - func: 方法名称，由双方约定
      - priority: 优先级
         - 收到多个控制指令时，agent按照指令优先级顺序进行执行, 同级指令依次执行
      - args: 方法参数, 由双方约定
- 范例
```json
{
    "guid": "123456",
    "timestamp": 1628834738016, 
    "command": [
        {
            "func": "func1",
            "priority": 1, 
            "args": {
                "args1": 0.5,
            }
        },
        {
            "func": "func3",
            "priority": 2, 
            "args": {
                "args1": "force",
                "args2": 0
            }
        }
    ]
}
```
## 四、监控器
## 五、控制器