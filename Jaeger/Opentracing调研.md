# Opentracing 调研


- [opentracing中文博客](https://wu-sheng.gitbooks.io/opentracing-io/content/pages/instrumentation/common-use-cases.html)

- [opentracing-tutorial](https://github.com/yurishkuro/opentracing-tutorial)

## 一、异步追踪

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


## 二、Python埋点示例


## 三、Go埋点示例






