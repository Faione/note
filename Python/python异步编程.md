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