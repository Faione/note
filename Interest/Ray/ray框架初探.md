# Ray框架初探

- [Ray框架初探](#ray框架初探)
  - [一、Ray Init](#一ray-init)
  - [二、Remote Function](#二remote-function)
    - [(1) 创建与运行](#1-创建与运行)
    - [(2) 指定资源](#2-指定资源)
    - [(3) 多个返回值](#3-多个返回值)
    - [(4) 取消task](#4-取消task)
  - [三、Remote Object & Object Ref](#三remote-object--object-ref)
    - [(1) 取得 Remote Object](#1-取得-remote-object)
    - [(2) 对象溢出](#2-对象溢出)
  - [四、Remote Classes](#四remote-classes)

## 一、Ray Init 


- 运行ray程序之前，必须使用 ray.init() 进行初始化
  - 一个进程中, init() 函数只能够调用一次, 否则出现error
    - init() 函数为当前进程初始化了一个 ray 单例对象以及其所依赖的其他运行环境
  - 不同进程中，init() 函数构造的ray对象在端口、node id 上都不同, 也就是说，不同进程 init() 的ray相互之间没有关联，不会干扰

ray init 信息

```json
{'node_ip_address': '127.0.0.1',
 'raylet_ip_address': '127.0.0.1',
 'redis_address': '127.0.0.1:6379', // redis 用来保存 ray 的运行信息, ray status --address 127.0.0.1:6379 即指当前的 ray 的信息
 'object_store_address': 'tcp://127.0.0.1:53081',
 'raylet_socket_name': 'tcp://127.0.0.1:29239',
 'webui_url': None,
 'session_dir': 'C:\\Users\\ICTNJ\\AppData\\Local\\Temp\\ray\\session_2022-02-18_17-08-25_585262_3008',
 'metrics_export_port': 33062,
 'gcs_address': '127.0.0.1:4370',
 'node_id': '67e7fbcd76a272f7a2189b065bb12816caf86f8e011b2f6f5f122f76'
 }
```

## 二、Remote Function

### (1) 创建与运行
- 普通函数使用 "@ray.remote" 修饰之后，就称为一个 remote function

```python
@ray.remote
def f():
   ...

# 等于

f = ray.remote(f)

# 此时 f 已经是 ray.remote() 函数所输出的对象，而非原本的函数
```

- remote function 的执行必须通过 "func.remote(args...)" 进行，无法直接调用
- remote() 的执行过程是异步的
  - 因此，多个 remote() 可以并发的执行
- remote() 的结果是 object ref, 搭配 ray.get() 得到最终的结果(Object)
  - remote function 的执行是异步的过程，ray.get() 则是同步的过程，get() 会等待 remote funtion 中的过程完全结束再输出结果
  - 同时，若 remote function 所返回的 object ref 所指代的对象并未在当前节点上，get() 过程中则还包括将结果下载到本地的过程
- remote function 接收静态的输入，同时也接收 object ref 作为输入
  - 接收 object ref 作为输入时, remote() 的执行则会自动同步, 即下游 remote function 会自动地等待上游 remote function 执行完毕之后再执行

### (2) 指定资源

- ray.init() 接收资源参数, 指定当前进程所能够使用的资源
  - 默认分配 cpu=1 
  - 可以指定超过实际资源数量的资源
- @ray.remote() 同样也能够接收资源参数，为remote function指定资源
  - 指定的资源必须在 ray.init() 所允许的范围之中, 否则 remote function 不会被调度
- 指定cpu资源，ray不会强制进行隔离
- 指定gpu资源，ray则能够提供资源的隔离
- 除了计算资源外，还可以指定要运行的任务的环境，其中可以包括 Python 包、本地文件、环境变量等

### (3) 多个返回值

- @ray.remote(num_returns=3) 适用于函数具有多个返回值的情况, 否则会产生错误

### (4) 取消task

- ray.cancel(obj_ref)

## 三、Remote Object & Object Ref

- 在ray的计算框架中，object是构造与计算的主要对象，并使用 object ref 指向某一个object(类似于指针)
  - Object ref 本质上是一个唯一 ID，可用于引用 Remote Object
    - 进行 remote function call 构造
    - 通过 ray.put() 构造
- Object存储在共享内存的object store中，集群中的每一个节点都部署有一个object store，并且，集群中object所分配的机器是无法提前得知的
- Remote Object是不可变的，因而得以在不同的Object store中复制却不必同步

TODO [python future](https://docs.python.org/zh-cn/3/library/asyncio-future.html)

### (1) 取得 Remote Object

- 使用 get 方法从Object Ref中获取Remote Object的结果，如果当前节点的对象存储不包含该对象，则下载该对象
  - 如果对象是 numpy 数组或 numpy 数组的集合，则 get 调用是零拷贝的，并通过共享对象存储内存返回此数组。否则，我们将对象数据反序列化为 Python 对象
- 在 ray.get(obj_ref, timeout=4) 设置超时
- 使用 ray.wait()来检查当前 ref 的完成状态

```python
ready_refs, remaining_refs = ray.wait(object_refs, num_returns=1, timeout=None)
```

### (2) 对象溢出

单节点上，share memory 有限，若 object store 满，则会与硬盘交换

## 四、Remote Classes

```python
@ray.remote
class Counter(object):
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value

# Create an actor from this class.
counter = Counter.remote()
```

- 同样的，actor也能指定所能使用的资源
- 不同actor调用的方法可以并行执行，同一个actor调用的方法按照调用顺序依次执行。同一个actor上的方法会互相共享状态

