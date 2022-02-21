- [curio异步编程](https://www.jianshu.com/p/78fac0669583)

- [python official](https://docs.python.org/zh-cn/3/library/asyncio-task.html)

```python
async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")
```


main作为主要的 async 方法, 其中创建tast但不等待task完成

# Python 异步编程

- async/await 为python提供的关键词，用来声明一个函数为协程
  - 协程的运行不同于函数, 直接调用并不能使其被调度执行
- 协程的执行方式
  - asyncio.run(): 输入参数为函数的入口点
    - asyncio.run()不可以在协程中使用
    - 此函数会运行传入的协程，负责管理 asyncio 事件循环，终结异步生成器，并关闭线程池，当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用
  - await: 等待协程执行完毕，协程将会串行执行
    - await必须在协程中使用，即协程中的 asyncio.run()
  - asyncio.create_task(): task 同样使用 await 等待执行完毕，但是task的执行是并发的  

- 可等待对象
  - 协程
    - 协程函数: 定义形式为 async def 的函数
    - 协程对象: 调用 协程函数 所返回的对象
  - 任务
    - 任务 被用来“并行的”调度协程
    - 当一个协程通过 asyncio.create_task() 等函数被封装为一个 任务，该协程会被自动调度执行
  - Futures
    - Future 是一种特殊的 低层级 可等待对象，表示一个异步操作的 最终结果
    - 当一个 Future 对象 被等待，这意味着协程将保持等待直到该 Future 对象在其他地方操作完毕
    - 在 asyncio 中需要 Future 对象以便允许通过 async/await 使用基于回调的代码