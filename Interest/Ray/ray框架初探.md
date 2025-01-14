# Ray框架初探

- [Ray框架初探](#ray框架初探)
  - [一、Ray Init](#一ray-init)
    - [ray集群操作](#ray集群操作)
  - [二、Remote Function (Tasks)](#二remote-function-tasks)
    - [(1) 创建与运行](#1-创建与运行)
    - [(2) 指定资源](#2-指定资源)
    - [(3) 多个返回值](#3-多个返回值)
    - [(4) 取消task](#4-取消task)
  - [三、Objects in Ray](#三objects-in-ray)
    - [(1) 取得 Remote Object](#1-取得-remote-object)
    - [(2) 对象溢出](#2-对象溢出)
  - [四、Remote Classes(Actor)](#四remote-classesactor)
    - [actor 命名](#actor-命名)
    - [actor 生命周期](#actor-生命周期)
    - [actor 池](#actor-池)
    - [worker \&\& actor](#worker--actor)
  - [五、Namespaces](#五namespaces)
    - [匿名空间](#匿名空间)
  - [六、Runtime Environment](#六runtime-environment)
    - [核心概念](#核心概念)
    - [运行时环境](#运行时环境)
    - [为每个job指定运行时环境](#为每个job指定运行时环境)
    - [为每个Task或Actor指定运行时环境](#为每个task或actor指定运行时环境)
  - [七、Ray Job Submission](#七ray-job-submission)
    - [目标](#目标)
    - [概念](#概念)
    - [Ray Job APIs](#ray-job-apis)
    - [CLI](#cli)
    - [SDK](#sdk)
    - [REST API](#rest-api)
  - [八、Ray Serve](#八ray-serve)
  - [九、其他](#九其他)
    - [task \&\& trace](#task--trace)
    - [actor模型](#actor模型)
    - [接入策略](#接入策略)

## 一、Ray Init 


- 运行ray程序之前，必须使用 ray.init() 进行初始化
  - 使用 ray.init() 将会创建一个 job, 在这个job的上下文中，不允许再次使用 ray.init()
  <!-- - 一个进程中, init() 函数只能够调用一次, 否则出现error
    - init() 函数为当前进程初始化了一个 ray 单例对象以及其所依赖的其他运行环境
  - 不同进程中，init() 函数构造的ray对象在端口、node id 上都不同, 也就是说，不同进程 init() 的ray相互之间没有关联，不会干扰 -->
- ray init() 作用是进行资源分配、命名空间创建、连接到ray集群，以及其他初始化工作

ray init 信息

```json
{'node_ip_address': '127.0.0.1',
 'raylet_ip_address': '127.0.0.1',
 'redis_address': '127.0.0.1:6379', 
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

## 二、Remote Function (Tasks)

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

## 三、Objects in Ray

Remote Object & Object Ref
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

# 构造一个 Remote Class
counter = Counter.remote()

# 调用 Remote Class 的方法
counter.increment.remote()

---------------- 等同于 ----------------

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

### worker && actor

- 每个 Ray worker 都是一个 python进程
- worker因 tasks 和 actor 而被不同地对待，任何 ray workeer
  - 用来执行多个 ray tasks
  - 被启动作为一个专门的 ray actor

- Tasks
  - Ray 启动时会自动的根据CPU数量启动一定数量的 ray workers(1 per cpu), 类似于进程池，这些 worker 被用来执行 tasks, 而一旦任务执行完成，则 worker进入闲置状态，直到被指派新的 task
- Actor
  - Ray actor 同样是一个 "ray worker", 但在运行时被实例化，他的所有方法将在同一个进程中运行，使用相同的资源，不同于 tasks, 运行 actors 的 python 进程不会被复用，且在actor被删除时终止

- 无状态的 task 调度起来更加灵活，如果不需要有状态的 actor, 则为更高的利用率，应当使用 task

## 五、Namespaces

- 命名空间是job和actor的逻辑分组, 一个actor被命名时，此名称在同一个命名空间中必须唯一

```python 
import ray
ray.init(address="auto", namespace="test")
```

### 匿名空间

- ray.init() 是不指定命名空间，ray将会将job放置一个匿名空间中，在此匿名空间中，此job会有自己的命名空间，且无法访问其他命名空间
  - 匿名空间实际上的实现类似于UUID's, 这使得其他job可以手动地连接到一个匿名空间中的job的命名空间，但ray不推荐这种做法

```python
# 获得当前的命名空间
namespace = ray.get_runtime_context().namespace
```

## 六、Runtime Environment

- 适用情况
  - 运行分布式的 ray 库 或者 程序
  - 运行引用本地文件的分布式的 ray 脚本
  - 快速迭代在 ray 集群中运行的，有变化依赖和文件的工程

- 解决的问题
  - ray script 引用\依赖 一些python库
  - ray script 查询一些特定环境变量
  - ray script 引入script以外的文件
- ray 期望依赖在集群中的所有节点上都存在

### 核心概念

- Ray Application:
  - 包含调用 ray.init() 的ray script 并使用 ray tasks/actor 的程序
- Dependencies/Environment
  - 应用程序需要运行的 Ray 脚本之外的任何内容，包括文件、包和环境变量
- Files
  - ray应用程序所需要的 Code files、data files or other files 
- Packages
  - Ray 应用程序所需的外部库或可执行文件，通常通过 pip 或 conda 安装
- Job
  - 在使用 ray.init() 连接到集群和通过调用 ray.shutdown() 或退出 Ray 脚本断开连接之间的一段执行时间
  - 用户调用ray的进程的运行周期就是一个job

### 运行时环境

- 运行时环境描述了 Ray 应用程序需要运行的依赖项，包括文件、包、环境变量等，他在集群上动态地进行安装
- 运行时环境使得开发者能够将运行在本地的ray app 翻译为能够运行在远程集群中的程序，而不需要要任何手动的环境设置

```python
runtime_env = {"working_dir": "/data/my_files", "pip": ["requests", "pendulum==2.1.2"]}

# To transition from a local single-node cluster to a remote cluster,
# simply change to ray.init("ray://123.456.7.8:10001", runtime_env=...)
ray.init(runtime_env=runtime_env)
```
### 为每个job指定运行时环境

- 指定运行环境的两种选项
  - default 当 job 开始时(ray.init（）)，就会立刻下载并安装依赖项
  - 仅当带调用task或创建actor时才开始安装依赖项

```json
# evn 中增加以下配置以启动第二个选项
"eager_install": False 
```

### 为每个Task或Actor指定运行时环境

- 可以让actor和task在自己的环境中运行，而与周围环境无关
  - 周边环境可以是作业的运行环境，也可以是集群的系统环境
- Ray 不保证具有冲突运行时环境的任务和参与者之间的兼容性

```python
# 调用一个 task
f.options(runtime_env=runtime_env).remote()

# 实例化一个 actor
actor = SomeClass.options(runtime_env=runtime_env).remote()

# Specify a runtime environment in the task definition.  Future invocations via
# `g.remote()` will use this runtime environment unless overridden by using
# `.options()` as above.
@ray.remote(runtime_env=runtime_env)
def g():
    pass

# Specify a runtime environment in the actor definition.  Future instantiations
# via `MyClass.remote()` will use this runtime environment unless overridden by
# using `.options()` as above.
@ray.remote(runtime_env=runtime_env)
class MyClass:
    pass
```

## 七、Ray Job Submission

### 目标

- 为用户提供一种轻量级的机制，将他们在本地开发和测试过的应用程序提交到正在运行的远程 Ray 集群，从而使用户能够将他们的 Ray 应用程序作为 Job 打包、部署和管理。这些作业可以由他们选择的作业经理提交。

### 概念

- Package
  - 定义应用程序的文件和配置的集合，从而允许它在不同的环境中远程执行（理想情况下是独立的）
  - 在 Job 提交的上下文中，打包部分由 Runtime Environments 处理，可以在其中动态配置 Ray 集群环境，提交的作业的actor或task级别的运行时环境
- Job
  - 提交给 Ray 集群执行的 Ray 应用程序
  - 提交作业后，它会在集群上运行一次以完成或失败。重试或不同参数的不同运行应由提交者处理
  - 作业绑定到 Ray 集群的生命周期，因此，如果 Ray 集群出现故障，该集群上所有正在运行的作业都将终止
- Job Manager
  - Ray 集群外部的一个实体，它管理 Job 的生命周期以及可能还有 Ray 集群的生命周期，例如调度、杀死、轮询状态、获取日志和持久化输入/输出
  - 可以是具有这些能力的任何现有框架，例如 Airflow。

### Ray Job APIs

- 确保有一个本地 Ray 集群, 终端中显示的地址和端口应该是我们提交作业请求的地方

```shell
$ pip install "ray[default]"

# http://127.0.0.1:8265 即是api入口
$ ray start --head
 Local node IP: 127.0.0.1
 INFO services.py:1360 -- View the Ray dashboard at http://127.0.0.1:8265

```

### CLI

**提交一个 job**

- 需要指定 "ray_init_test.py" 所在的工作目录，如有非基础库的依赖库，则还需要增加 "pip": ["requests==2.26.0"] 声明依赖
- windows下，处理json字符串需要注意转义

```shell
$ ray job submit --runtime-env-json='{"working_dir": "./"}' -- "python ray_init_test.py"
```

### SDK

```python
from ray.dashboard.modules.job.sdk import JobSubmissionClient
from ray.dashboard.modules.job.common import JobStatus, JobStatusInfo
import time

client = JobSubmissionClient("http://127.0.0.1:8265")

job_id = client.submit_job(
    # Entrypoint shell command to execute
    entrypoint="python ray_init_test.py",
    # Working dir
    runtime_env={
        "working_dir": "./"
    }
)


def wait_until_finish(job_id):
    start = time.time()
    timeout = 5
    while time.time() - start <= timeout:
        status_info = client.get_job_status(job_id)
        status = status_info.status
        print(f"status: {status}")
        if status in {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED}:
            break
        time.sleep(1)


wait_until_finish(job_id)
logs = client.get_job_logs(job_id)
print(logs)
```

### REST API

- 在后台，Job Client 和 CLI 都对运行在 ray 头节点上的作业服务器进行 HTTP 调用。因此，如果需要，用户也可以通过 HTTP 直接向相应的端点发送请求
- 测试尚未成功

```url
http://127.0.0.1:8265/api/jobs/submit
```

## 八、Ray Serve

```python
import ray
import requests

runtime_env = {"working_dir": "/data/my_files", "pip": ["requests", "pendulum==2.1.2"]}

ray.init(runtime_env=runtime_env)

@ray.remote()
def f():
  open("my_datafile.txt").read()
  return requests.get("https://www.ray.io")

```

```python

ray.init(num_cpus=4, num_gpus=2)

@ray.remote(num_cpus=2, num_gpus=1)
def f():
  return 1

@ray.remote(runtime_env=runtime_env)
def g():
    pass
    
@ray.remote(runtime_env=runtime_env)
class MyClass:
    pass
```


## 九、其他

### task && trace

ray && opentelementry

### actor模型

### 接入策略

计算任务以 job 为核心单位进行管理，使用 rest api 将用户的源代码进行提交

