# Opentracing 使用

- [Opentracing 使用](#opentracing-使用)
  - [一、Python埋点示例](#一python埋点示例)
    - [(1) client配置与tracer创建](#1-client配置与tracer创建)
      - [Client配置](#client配置)
      - [tracer创建](#tracer创建)
    - [(2) span 创建](#2-span-创建)
      - [创建与结束](#创建与结束)
      - [with语法](#with语法)
      - [关联span](#关联span)
      - [使用scope](#使用scope)
    - [(3) tag 与 log](#3-tag-与-log)
      - [Tag](#tag)
      - [Log](#log)
    - [(4) 追踪RPC](#4-追踪rpc)
      - [inject](#inject)
      - [extract](#extract)
    - [(5) baggage](#5-baggage)
      - [添加baggage](#添加baggage)
      - [取出baggage](#取出baggage)
  - [二、Go埋点示例](#二go埋点示例)
  - [三、异步追踪](#三异步追踪)

- [opentracing中文博客](https://wu-sheng.gitbooks.io/opentracing-io/content/pages/instrumentation/common-use-cases.html)

- [opentracing-tutorial](https://github.com/yurishkuro/opentracing-tutorial)


## 一、Python埋点示例

### (1) client配置与tracer创建

#### Client配置

```python
import logging
from jaeger_client import Config


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'reporter_batch_size': 1,
            'local_agent': {
                'reporting_host': "10.16.0.180", # jaeger agent host
                'reporting_port': 5775, # jaeger agent port
            }
        },
        service_name=service,
    )

    return config.initialize_tracer()

```
#### tracer创建

```python
import opentracing


# 只定义，而不初始化
# tracer = opentracing.tracer

# 使用上述配置构造并初始化
tracer = init_tracer('service name')
```

### (2) span 创建

#### 创建与结束

```python
span = tracer.start_span('test_process')

...
do_process()
...

span.finish()
```

#### with语法

```python
with tracer.start_span('test_process') as span:
    ...
    do_process()
    ...
```

#### 关联span

```python
# 改方法会创建一个span, 并声明 root_span 依赖此span
def get_data(root_span, url):
    with tracer.start_span('test_process', child_of=root_span) as span:
        ...
        do_process()
        ...   
```

#### 使用scope

使用 start_span() 需要显示的要求传入 root_span 参数, 侵入性较高  
而 opentracing 提供了scope, 用来隐式地构造span之间的关联关系
  - 如果调用发生在一个span中，则此构造方式会自动的指定 child_of 关系, 否则则将创建一个 root span

```python
def get_data(root_span, url):
    with tracer.start_active_span('test_process') as scope:
        # 获得当前的span
        span = scope.span

        ...
        do_process()
        ...
```

### (3) tag 与 log

opentracing提供方法，为span打上tag或增加log来丰富span所表达的内容

#### Tag

- 一组键值对构成的标签集合
- 用来对当前的Span对象进行描述

```python
span.set_tag('url', '/data')
```

#### Log

- 一组日志集合
- 记录 span 所包含的trace过程的log信息，类似于通常log的使用，span
- 区分 Tag 与 Log 的一般性原则: 描述整个Span的信息应当记录为标签, 而与时间戳相关的事件应当记录为日志

```python
span.log_kv('event'：'do sum' )
```

### (4) 追踪RPC

追踪RPC需要在进程之间传递span, 因此需要对span进行打包/解包, 并在请求中携带  
opentracing提供成对的 inject/extract 方法进行以上操作, 并对常规RPC框架提供支持

opentracing 提供了三种span打包的 Format
- HTTP_HEADERS: http请求头
- TEXT_MAP: 文本字典
- BINARY: 二进制

#### inject

Up Stream

```python
def http_get(url, param, value):
    span = tracer.active_span # 获得当前没有结束的span

    headers = {}
    tracer.inject(span, Format.HTTP_HEADERS, headers) # 将span注入到请求头中

    r = requests.get(url, params={param: value}, headers=headers) # 携带含有span的请求头进行请求
    assert r.status.code == 200
    return r.text
```

#### extract

Down Stream

```python
def handle_get(request):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers) # 从请求头中解析出span
    with tracer.start_span('test_process', child_of=span_ctx) as span: # 与上游span关联
        ...
        do_handle()
        ...
```

### (5) baggage

span也可以在上游->下游中传递信息
- 区别与 Tag 与 Log, baggage信息只在上游->下游间传递，不会在trace中保留

#### 添加baggage

Up Stream

```python
def http_get(url, param, value):
    span = tracer.active_span 
    span.set_baggage_item('user_name', 'fhl') # 将信息放入baggage

    headers = {}
    tracer.inject(span, Format.HTTP_HEADERS, headers) 

    r = requests.get(url, params={param: value}, headers=headers) 
    assert r.status.code == 200
    return r.text
```

#### 取出baggage

Down Stream

```python
def handle_get(request):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers) 
    user_name = span_ctx.get_baggage_item('user_name')  # 取出baggage中的信息
    with tracer.start_span('test_process', child_of=span_ctx) as span:
        ...
        do_handle()
        ...
```

## 二、Go埋点示例


## 三、异步追踪

opentracing的异步追踪基于对RPC框架的支持，以http请求为例, 构造http请求时通过 tracer.inject()将当前的span注入到http请求头中

**往请求信息中注入span**

```python

parent_span = get_current_span()

# start a new span to represent the RPC
span = tracer.start_span(
    operation_name=operation,
    child_of=parent_span.context,
    tags={'http.url': request.full_url}
)

# propagate the Span via HTTP request headers
tracer.inject(
    span.context,
    format=opentracing.HTTP_HEADER_FORMAT,
    carrier=request.headers)

```

同时, 设置回调方法, 在其中进行span的关闭

**http回调方法**

```python
# define a callback where we can finish the span
def on_done(future):
    if future.exception():
        span.log(event='rpc exception', payload=exception)
    span.set_tag('http.status_code', future.result().status_code)
    span.finish()

try:
    future = http_client.execute(request)
    future.add_done_callback(on_done)
    return future
except Exception e:
    span.log(event='general exception', payload=e)
    span.finish()
    raise
```

因此，如果需要进行异步追踪, 使用的RPC/IPC框架必须支持回调







