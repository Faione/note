# Regulator 接口设计

## 一、说明
Regulator作为agent的控制组件，直接或通过其他间接手段对目标的资源进行调控，并维护改对象当前的资源分配状态，同步给agent


- 接口版本 /v1.0  
- URL示例: 
```http
http://<host>:<port>/v1.0/regulator/info
```

## 二、服务agent
### (1) 基础信息
[GET] /regulator/info   

**Request**   
- params:
  
- body: 
  
**Response**
- body:  
```json
{
    "reporter_verion": "v1.0", 
    "api_version": "v1.0", 
    "regulator_name": "contaienr_regulator",  
    "regulator_port": "9002"
}
```

[GET] /regulator/status/{local_id} 

某一对象的控制信息统计(当前资源状态、调控次数)

**Request**   
- params:
  
- body: 
  
**Response**
- body:  

### (2) 控制同步
[GET] /regulator/synchronize   

**Request**   
- params:
  
- body: 
  
**Response**
- body:  

### (3) 控制监听
[GET] /regulator/exec   

**Request**   
- params:
  
- body:

```json
{
    "func_queue": [
        {   "func_name": "func1", 
            "description": "localId",
            "params": ["add"] // add cpu core
        },
        {   "func_name": "func1", 
            "description": "localId2",
            "params": [true] // stop container
        },
        {   "func_name": "func2", 
            "description": "localId3",
            "params": ["reduce"] // reduce cpu core
        }
    ]
}
``` 
  
**Response**
- body: 

```json
{
    "response_queue": [
        {   "func_name": "func1", 
            "description": "localId",
            "params": ["add"] // add cpu core
        },
        {   "func_name": "func1", 
            "description": "localId2",
            "params": [true] // stop container
        },
        {   "func_name": "func2", 
            "description": "localId3",
            "params": ["reduce"] // reduce cpu core
        }
    ]
}
``` 
