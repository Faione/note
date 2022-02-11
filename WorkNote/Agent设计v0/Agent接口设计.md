# Agent接口设计
此Agent指代微服务中的agent，而非整个Agent
- [Agent接口设计](#agent接口设计)
  - [说明](#说明)
  - [一、服务用户](#一服务用户)
    - [(1) 版本信息](#1-版本信息)
    - [(2) 初始化（弃用）](#2-初始化弃用)
    - [(3) 关闭](#3-关闭)
    - [(4) 重新启动（弃用）](#4-重新启动弃用)
    - [(5) 注册对象查询](#5-注册对象查询)
    - [(6) 注册方法查询](#6-注册方法查询)
    - [(7) 配置reporter](#7-配置reporter)
    - [(8) 启动上报](#8-启动上报)
    - [(9) 终止上报](#9-终止上报)
  - [二、服务上层](#二服务上层)
  - [三、服务对象](#三服务对象)
    - [(1) 注册/重连](#1-注册重连)
    - [(2) 注销](#2-注销)
    - [(3) 心跳](#3-心跳)
  - [四、服务reporter](#四服务reporter)
    - [(1) 请求reporter配置](#1-请求reporter配置)
    - [(2) 接收上报](#2-接收上报)
  - [五、服务regulator](#五服务regulator)
    - [(1) 请求regulator配置](#1-请求regulator配置)
    - [(2) 方法注册](#2-方法注册)
    - [(3) 方法注销](#3-方法注销)
    - [(4) 方法更新](#4-方法更新)


## 说明
- 接口版本 /v1.0  
- URL示例: 
```http
http://<host>:<port>/v1.0/agent/info
```
## 一、服务用户
### (1) 版本信息  
[GET] /agent/info   

**Request**   
- params:
  
- body: 
  
**Response**
- body:  
```json
{
    "agent_verion": "v2.0", 
    "api_version": "v1.0", 
    "agent_port": "9000"
}
```
### (2) 初始化（弃用）
[GET] /agent/init

**Request**   
- params:  

| Key | Value |
|  ----  | ----  |
| is_default  | false |
| config_path  | /home/aab/agent.config |

- body: 
  
**Response**
- body:

```json
{
    "code": 1, // 请求成功
    "msg": "初始化成功，使用自定义配置", 
    "data":"" 
}
```

### (3) 关闭
[GET] /agent/stop

**Request**   
- params:
  
- body: 
  
**Response**
- body:   

### (4) 重新启动（弃用）
[GET] /agent/restart

**Request**   
- params:
  
- body: 
  
**Response**
- body: 

### (5) 注册对象查询
 [GET] /agent/objects/{guid}

**Request**   
- params:

- body: 
  
**Response**
- body: 

 [GET] /agent/objects

**Request**   
- params:

| Key | Value | Describition|
| ---- | ---- | ---- |
| is_all  | false | 是否显示全部信息 |

- body: 
  
**Response**
- body:

### (6) 注册方法查询
 [GET] /agent/functions/{func_name}

**Request**   
- params:

- body: 
  
**Response**
- body: 


 [GET] /agent/functions

**Request**   
- params:

| Key | Value | Describition|
| ---- | ---- | ---- |
| is_all  | false | 是否显示全部信息 |

- body: 
  
**Response**
- body
  
```json
{
    "state": 0, // 0: success, 1: failure
    "code": 20001, // 错误码
    "msg": "default_regulator",
    "data": [
        {
            "name": "func1",
            "description": "increase cpu allocation"
        },
        {
            "name": "func2",
            "description": "shutdown target container"
        }
    ]
}
```

### (7) 配置reporter
[Post] /ctl/reporter/init

**Request**   
- params:
  
- body: 
```json
{
    "ContainerId":["id1", "id2"]
}
```
**Response**
- body: 
```json
{
"state": 0,  // 0: success, 1: failure
"code": 20001, // 错误码
"msg": "配置成功", 
"data":"" 
}
```

### (8) 启动上报
[Get] /ctl/reporter/start/{guid}

**Request**   
- params:
  
- body: 
  
**Response**
- body: 
  
### (9) 终止上报
[Get] /ctl/reporter/stop/{guid}

**Request**   
- params:
  
- body: 
  
**Response**
- body: 


## 二、服务上层
暂不使用RESTful接口，而使用RPC

## 三、服务对象
### (1) 注册/重连
[Post] /object/register

**Request**   
- params:
  
- body: 
  
```json
{
    "type": "service", 
    "identity_info": "192.168.1.10+8080", 
    "other_info": "containerId1"
}
```
**Response**
- body: 

```json
{
"state": 0,  // 0: success, 1: failure
"code": 20001, // 错误码
"msg": "注册成功", 
"data":"" 
}
```
### (2) 注销
[Post] /object/logout

**Request**   
- params:
  
- body: 

 ```json
{
    "type": "service", 
    "identity_info": "192.168.1.10+8080", 
    "other_info": "containerId1"
}
``` 

**Response**
- body: 
### (3) 心跳
[Post] /object/heartbeat

**Request**   
- params:
  
- body: 
  
**Response**
- body: 


## 四、服务reporter
reporter接入时，主动向agent询问需要监控的对象，并将自己能够监控到的数据上报给agent
### (1) 请求reporter配置
[get] /reporter/config

**Request**   
- params:
  
- body: 
  
**Response**
- body:


### (2) 接收上报
[Post] /reporter/report

**Request**   
- params:
  
- body: 
  
**Response**
- body: 

## 五、服务regulator
### (1) 请求regulator配置
[get] /regulator/config

**Request**   
- params:
  
- body: 
  
**Response**
- body:

  
### (2) 方法注册
[Post] /regulator/registerFunc

Regulator传入注册信息，由agent生成funcName，并返回给Regulator

**Request**   
- params:
  
- body: 
```json
{
    "data": [
        {
            "description": "increase cpu allocation",
            "[params]": [
                {
                    "type": "String",
                    "description": "guid"
                },
                {
                    "type": "boolean",
                    "description": "是否成功"
                }
            ]
        },
        {
            "description": "shutdown target container",
            "params": [
                {
                    "type": "String",
                    "description": "guid"
                }, 
                {
                    "type": "boolean",
                    "description": "是否成功"
                }
            ]
        }
    ]
}
```

**Response**
- body: 

### (3) 方法注销
[Get] /regulator/cancelFunc

**Request**   
- params:
  
- body: 
  
**Response**
- body

### (4) 方法更新
[Get] /regulator/updateFunc

**Request**   
- params:
  
- body: 
  
**Response**
- body
