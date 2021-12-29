## 端到端追踪策略页面API

- [端到端追踪策略页面API](#端到端追踪策略页面api)
  - [(1) 基础说明](#1-基础说明)
    - [基础信息](#基础信息)
    - [通用返回](#通用返回)
    - [错误代码](#错误代码)
  - [(2) traces信息查询接口](#2-traces信息查询接口)
      - [简要描述](#简要描述)
      - [请求路径](#请求路径)
      - [请求方式](#请求方式)
      - [请求参数](#请求参数)
      - [返回示例](#返回示例)
      - [返回参数说明](#返回参数说明)
      - [备注](#备注)
  - [(3) trace具体信息查询接口](#3-trace具体信息查询接口)
      - [简要描述](#简要描述-1)
      - [请求路径](#请求路径-1)
      - [请求方式](#请求方式-1)
      - [请求参数](#请求参数-1)
      - [返回示例](#返回示例-1)
      - [返回参数说明](#返回参数说明-1)
      - [备注](#备注-1)
  - [(4) service信息查询接口](#4-service信息查询接口)
      - [简要描述](#简要描述-2)
      - [请求路径](#请求路径-2)
      - [请求方式](#请求方式-2)
      - [请求参数](#请求参数-2)
      - [返回示例](#返回示例-2)
      - [返回参数说明](#返回参数说明-2)
      - [备注](#备注-2)
  - [(5) dependencies信息查询接口](#5-dependencies信息查询接口)
      - [简要描述](#简要描述-3)
      - [请求路径](#请求路径-3)
      - [请求方式](#请求方式-3)
      - [请求参数](#请求参数-3)
      - [返回示例](#返回示例-3)
      - [返回参数说明](#返回参数说明-3)
      - [备注](#备注-3)
  - [(6) operation信息查询接口](#6-operation信息查询接口)
      - [简要描述](#简要描述-4)
      - [请求路径](#请求路径-4)
      - [请求方式](#请求方式-4)
      - [请求参数](#请求参数-4)
      - [返回示例](#返回示例-4)
      - [返回参数说明](#返回参数说明-4)
      - [备注](#备注-4)

### (1) 基础说明

#### 基础信息

- 演示页面: `http://47.108.237.20:16686/`
- 基础接口入口: `http://47.108.237.20:16686/api`
- 服务端已开启 CORS 跨域支持
- 数据返回格式统一使用 JSON

#### 通用返回

- 结果示例

```json
{
    "data": [],
    "total": 0,
    "limit": 0,
    "offset": 0,
    "errors": null
}
```

- 参数说明

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| data | - | 查询得到的结果, 无结果则值为"[]", 出错时为"null" |
| errors | - | 当前请求的错误描述, 无错误则值为"null"|
| total | int | 部分接口中使用, 标识当前查询结果的总数, 默认为 0 |
| limit | int | 部分接口中使用, 当前查询结果的数量限制, 默认为 0 |
| offset | int | 部分接口中使用, 描述当前序号的偏移, 默认为 0 |

#### 错误代码

- 结果示例

```json
{
    "data": null,
    "total": 0,
    "limit": 0,
    "offset": 0,
    "errors": [
        {
            "code": 404,
            "msg": "trace not found"
        }
    ]
}
```

- 参数说明

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| code | int | 错误码 |
| msg | string | 错误描述 |


### (2) traces信息查询接口

##### 简要描述

- traces信息查询接口

##### 请求路径

- `traces`

- 示例: `http://47.108.237.20:16686/api/traces?end=1640046900000000&limit=20&lookback=custom&maxDuration=300ms&minDuration=100ms&service=frontend&start=163828800000000`
  
##### 请求方式
- GET 

##### 请求参数

|参数名|必选|类型|说明|
|:---|:---|:---|---|
| service | 是 | string | 需要进行追踪的服务名称, eg: frontend |
| operation | 否 | string | 需要进行追踪的服务的具体操作的名称, eg: "HTTP GET /dispatch" |
| start | 否 | timeStamp(16位) | 时间区间开始 |
| end | 否 | timeStamp(16位) | 时间区间结束  |
| lookback | 否 | string{"1h", "2h", "3h", "6h", "12h", "24h", "2d", "custom"}| 以endTime为终止, 回溯的时间区间, "custom" 指手动选择时间区间 |
| maxDuration | 否 |string | 最小持续时间, eg: 100ms |
| minDuration | 否 | string | 最大持续时间, eg: 1s |

##### 返回示例 

``` json
{
    "data": [
        {
            "traceID": "365a12035b3313b1",
            "spans": [
                {
                    "traceID": "365a12035b3313b1",
                    "spanID": "3e386f81a4524427", 
                    "flags": 1,
                    "operationName": "HTTP GET /customer", 
                    "references": [
                        { 
                            "refType": "CHILD_OF",
                            "traceID": "365a12035b3313b1", 
                            "spanID": "6065a57f239aee5f" 
                        }
                    ],
                    "startTime": 1638339993336574,
                    "duration": 422459, 
                    "tags": [
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "/customer?customer=123"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "net/http"
                        },
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1638339993336602, 
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "HTTP request received"
                                },
                                {
                                    "key": "level",
                                    "type": "string",
                                    "value": "info"
                                },
                                {
                                    "key": "method",
                                    "type": "string",
                                    "value": "GET"
                                },
                                {
                                    "key": "url",
                                    "type": "string",
                                    "value": "/customer?customer=123"
                                }
                            ]
                        },
                        {
                            "timestamp": 1638339993336676,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "Loading customer"
                                },
                                {
                                    "key": "customer_id",
                                    "type": "string",
                                    "value": "123"
                                },
                                {
                                    "key": "level",
                                    "type": "string",
                                    "value": "info"
                                }
                            ]
                        }
                    ],
                    "processID": "p1",
                    "warnings": null
                }
            ]
        }
    ],
    "total": 0,
    "limit": 0,
    "offset": 0,
    "errors": null
}
```

##### 返回参数说明 

- Traces：

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| traceID | string | 标记整个trace |
| spanID | string | 标记当前span, 起始span使用traceID |
| operationName | string | 标记当前span所追踪的过程/方法名称 |
| references | - | 描述span之间的关联关系，即span图中的边定义 |
| startTime | timeStamp(16位) | 标记当前span的开始时间 |
| duration | long | 标记当前span的持续时间 |
| tags | - | 描述当前span |
| logs | - | 描述span追踪的过程/方法 |
| processID | string | 当前span所属的进程 |


- References: 

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| refType | string | 关联关系说明，取值有 "CHILD_OF","FollowsFrom" |
| traceID | string | 标识当前 span 所属的trace |
| spanID | string | 当前refType的对象, eg: 当前Span CHILD_OF spanID, 当前Span是spanID的孩子节点 |



##### 备注 

- 更多返回错误代码请看首页的错误代码描述


### (3) trace具体信息查询接口

##### 简要描述

- trace具体信息查询接口

##### 请求路径

- `traces/{traceID}`

- 示例: `http://47.108.237.20:16686/api/traces/4cf9ef098354ab97`

##### 请求方式

- GET 

##### 请求参数

|参数名|必选|类型|说明|
|:---|:---|:---|---|
| traceID | 路径参数 | string | 标记整个trace |

##### 返回示例 

```json

{
    "data": [
        {
            ...

            "processes": {
                "p1": {
                    "serviceName": "customer",
                    "tags": [
                        {
                            "key": "client-uuid",
                            "type": "string",
                            "value": "19ba86210b28aa95"
                        },
                        {
                            "key": "hostname",
                            "type": "string",
                            "value": "863368f4a924"
                        },
                        {
                            "key": "ip",
                            "type": "string",
                            "value": "172.18.0.3"
                        },
                        {
                            "key": "jaeger.version",
                            "type": "string",
                            "value": "Go-2.29.1"
                        }
                    ]
                },
               
               ...

                "p6": {
                    "serviceName": "route",
                    "tags": [
                        {
                            "key": "client-uuid",
                            "type": "string",
                            "value": "24852e81e60e17f8"
                        },
                        {
                            "key": "hostname",
                            "type": "string",
                            "value": "863368f4a924"
                        },
                        {
                            "key": "ip",
                            "type": "string",
                            "value": "172.18.0.3"
                        },
                        {
                            "key": "jaeger.version",
                            "type": "string",
                            "value": "Go-2.29.1"
                        }
                    ]
                }
            },
            "warnings": null
        }
    ],
    "total": 0,
    "limit": 0,
    "offset": 0,
    "errors": null

```
##### 返回参数说明

- processes

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| serviceName | string | 微服务的名称 |
| tags | - | 对当前微服务进行描述 |

- tag

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| key | string | key名称 |
| type | string | value类型 |
| value | string | value值 |

##### 备注 

- 更多返回错误代码请看首页的错误代码描述


### (4) service信息查询接口

##### 简要描述

- service信息查询接口

##### 请求路径

- `services`

- 示例: `http://47.108.237.20:16686/api/services`
  
##### 请求方式

- GET 

##### 请求参数

|参数名|必选|类型|说明|
|:---|:---|:---|---|

##### 返回示例 

``` json
{
    "data": [
        "mysql",
        "redis",
        "frontend",
        "driver",
        "customer",
        "route"
    ],
    "total": 6,
    "limit": 0,
    "offset": 0,
    "errors": null
}
```

##### 返回参数说明 

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| total | int | 微服务个数计数 |

##### 备注 

- 更多返回错误代码请看首页的错误代码描述


### (5) dependencies信息查询接口

##### 简要描述

- dependencies信息查询接口
   - 描述过去一段时间内的微服务依赖图谱 

##### 请求路径

- `dependencies`

- 示例: `http://47.108.237.20:16686/api/dependencies?endTs=1640052650859&lookback=604800000`
  
##### 请求方式

- GET 

##### 请求参数

|参数名|必选|类型|说明|
|:---|:---|:---|---|
| endTime | 是 | timeStamp(16位) | 时间区间结束, 一般指当前时间戳 |
| lookback | 是 | long | 回溯的时间长度 |

##### 返回示例 

``` json
{
    "data": [
        {
            "parent": "frontend",
            "child": "customer",
            "callCount": 7
        },
        {
            "parent": "frontend",
            "child": "route",
            "callCount": 70
        },
        {
            "parent": "frontend",
            "child": "driver",
            "callCount": 7
        },
        {
            "parent": "customer",
            "child": "mysql",
            "callCount": 7
        },
        {
            "parent": "driver",
            "child": "redis",
            "callCount": 94
        }
    ],
    "total": 0,
    "limit": 0,
    "offset": 0,
    "errors": null
}
```

##### 返回参数说明 

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| callCount | int | parent向child请求的次数计数 |
| total | int | 涉及到的微服务个数计数 |

##### 备注 

- 更多返回错误代码请看首页的错误代码描述

### (6) operation信息查询接口

##### 简要描述

- operation信息查询接口

##### 请求路径

- `services/{service}/operations`

- `http://47.108.237.20:16686/api/services/customer/operations`
  
##### 请求方式

- GET 

##### 请求参数

|参数名|必选|类型|说明|
|:---|:---|:---|---|
| service | 路径参数 | string | 需要进行追踪的服务名称, eg: frontend |

##### 返回示例 

``` json
{
    "data": [
        "HTTP GET /",
        "HTTP GET /config",
        "HTTP GET /dispatch",
        "HTTP GET: /route",
        "HTTP GET: /customer",
        "/driver.DriverService/FindNearest",
        "HTTP HEAD /",
        "HTTP POST /",
        "HTTP GET"
    ],
    "total": 9,
    "limit": 0,
    "offset": 0,
    "errors": null
}
```

##### 返回参数说明 

| 参数名 | 类型 | 说明 |
| :-- | :-- | --- |
| total | int | 请求的方法个数计数 |

##### 备注 

- 更多返回错误代码请看首页的错误代码描述





