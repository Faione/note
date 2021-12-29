# Reporter 接口设计

## 一、说明
Reporter作为agent的监控组件，直接或通过其他间接手段获得监控数据，并格式化为总线格式，调用agent的上报功能，将监控数据发送至数据中心


- 接口版本 /v1.0  
- URL示例: 
```http
http://<host>:<port>/v1.0/reporter/info
```

## 二、服务agent
### (1) 基础信息
[GET] /repoter/info   

**Request**   
- params:
  
- body: 
  
**Response**
- body:  
```json
{
    "reporter_verion": "v1.0", 
    "api_version": "v1.0", 
    "reporter_name": "container_reporter",  
    "reporter_port": "9001"
}
```

[GET] /repoter/status/{local_id} 

某一对象的监控信息统计(监控的时间、上报的log数量)

**Request**   
- params:
  
- body: 
  
**Response**
- body:  


### (2) 终止上报
[GET] /repoter/stop   

**Request**   
- params:
  
- body:  
  
**Response**
- body: 

[GET] /repoter/stop/{local_id}   
           
**Request**   
- params:
  
- body: 
  
**Response**
- body

### (3) 启动上报
[GET] /repoter/start   

**Request**   
- params:
  
- body: 
  
**Response**
- body: 

[GET] /repoter/start/{local_id}   

**Request**   
- params:
  
- body: 
  
**Response**
- body

### (4) 数据拉取
[GET] /repoter/pull/{local_id}     

**Request**   
- params:

| Key | Value |
|  ----  | ----  |
| duration  | 从当前时间向后的时间维度 |

- body: 
  
**Response**
- body: 


### (5) 监控同步
[POST] /repoter/synchronize   

**Request**   
- params:
  
- body: 
  
**Response**
- body: 

### (6) 重启reporter
[GET] /repoter/restart   

**Request**   
- params:
  
- body: 
  
**Response**
- body: 
