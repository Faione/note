# Ray框架初探

- [Ray框架初探](#ray框架初探)
  - [一、Ray Init](#一ray-init)
    - [ray集群操作](#ray集群操作)
  - [二、Remote Function](#二remote-function)
    - [(1) 创建与运行](#1-创建与运行)
    - [(2) 指定资源](#2-指定资源)
    - [(3) 多个返回值](#3-多个返回值)
    - [(4) 取消task](#4-取消task)
  - [三、Remote Object & Object Ref](#三remote-object--object-ref)
    - [(1) 取得 Remote Object](#1-取得-remote-object)
    - [(2) 对象溢出](#2-对象溢出)
  - [四、Remote Classes(Actor)](#四remote-classesactor)
    - [actor 命名](#actor-命名)
    - [actor 生命周期](#actor-生命周期)
    - [actor 池](#actor-池)

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

### ray集群操作

```shell
# 启动单节点的ray runtime，当前机器将会成为"head node" 
$ ray start --head --port=6379
```

连接当前节点的ray runtime
- 可以将其他机器与当前的 head node 连接从而构成集群，集群中的任何程序都可以通过以下方式连接到ray集群
- 默认情况下，Ray 将并行化其工作负载并在多个进程和多个节点上运行任务

```python 
import ray
ray.init(address='auto')
```

- 可以通过启用本地模式来强制所有 Ray 函数在单个进程上发生

```python 
import ray
ray.init(local_mode=True)
```

- 可以指定当前程序所允许的命名空间

```python 
import ray
ray.init(address="auto", namespace="test")
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
- 资源隔离
  - 指定cpu资源，ray不会强制进行隔离
  - 指定gpu资源，ray则能够提供资源的隔离
- 除了计算资源外，还可以指定要运行的任务的环境，其中可以包括 Python 包、本地文件、环境变量等
  - 可以指定 custom 自定义资源，前提是改资源在集群上已经定义(通过参数在启动时声明资源数量)
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
 
- Python future对象
  - 一个 Future 代表一个异步运算的最终结果
  - Future 是一个 awaitable 对象。协程可以等待 Future 对象直到它们有结果或异常集合或被取消

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

## 四、Remote Classes(Actor)

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

# 调用 remote class 的方法
counter.increment.remote()

------------------ 等同于 -----------------

class Counter(object):
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value

    def get_counter(self):
        return self.value

# ray.remote 接收一个类作为输入，并生成一个 Remote Class
Counter = ray.remote(Counter)

counter_actor = Counter.remote()
```

- 不同actor调用的方法可以并行执行，同一个actor调用的方法按照调用顺序依次执行(串行)
- 同一个actor上的方法会互相共享状态(上下文)


- 当actor被构造时
  - 集群中的一个节点将被选中并运行一个工作者进程，所有对于actor的方法调用将通过这个工作者进程来完成
  - 一个 actor 所指代的对象(原本对象)将在工作者进程中实例化，并调用其构造方法


- 同样的，actor也能指定所能使用的资源
  - 当一个GPU actor被创建时, 它会被调度到一个至少拥有一个GPU的节点上，且此GPU会在Actor的生命周期内持续为Actor保留(独占), 当actor终止时，GPU资源将被释放
  - 若不指定资源，则actor也不会去主动请求资源(默认)，此时无法对其中的方法进行资源分配

- 可以在 remote class 构造时动态的改变资源分配

```shell
a1 = Counter.options(num_cpus=1, resources={"Custom1": 1}).remote()
```

### actor 命名

- actor handle: actor 句柄，指向一个actor
  - 指针指向一个对象的内存地址，句柄则是由系统所管理的引用标识，可以被重定位到不同的对象

- actor 命名
  - 在 ray 集群中，可以通过 actor handle 得到一个 actor，然而实际上直接传递 actor handle 不一定方便
  - ray 允许对actor进行命名，该名称定义的namespace中唯一，可以在集群中的任何位置，通过命名获得该actor
    - 需要在一个namespace中
  - 但是，如果handle不在存在，则actor会被回收
    

```shell
ray.init(address="auto", namespace="test")
counter = Counter.options(name="some_name").remote()

# ---- somewhere in the cluster 

ray.init(address="auto", namespace="test")
counter = ray.get_actor("some_name")
```

### actor 生命周期

- 一般认为，actor随程序的退出而终结，然而actor的生命周期实际上与作业解耦，即允许actor在驱动进程退出之后仍然存在
- 反之，则原来的程序退出，actor终结

```shell
counter = Counter.options(name="CounterActor", lifetime="detached").remote()
```

### actor 池

ray 允许用户构造 actor 池用来进行任务调度

