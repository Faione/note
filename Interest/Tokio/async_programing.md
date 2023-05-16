# Async Programing

## Intro

当一个任务是计算密集型时，通常表现为单个CPU占用率较高，我们可以通过并行化来让任务利用更多的计算资源，以加快计算过程，如采用多线程

当一个任务是I/O密集型时，CPU往往因等待IO中断而占用率不高，此时可以通过异步编程的方式在一个CPU允许多个并发的I/O，增加CPU的占用率

异步编程核心是用户态的绿色线程，相比于多线程，创建/回收，以及切换的开销都更低，同时也正因为是绿色线程，面对计算密集型任务无法像多线程一样运用多核资源，需要按照情况进行选择

与异步编程相对的是同步编程，前者包含有一个用户态线程调度器，允许并发的执行多个任务，而后者则必须按照顺序依次执行，在高并发场景下，异步编程能够减少有效减少延迟

## Async in Rust

rust标准库中提供了 `Future` trait, `async`, `await` 关键字，能够在编译时，将一个异步函数编译为Future对象，作为异步编程的调度单位，但是rust本身并没有提供官方的调度器实现

tokio是一个异步运行时的实现，提供了常见I/O库的异步实现，实现异步网络编程，异步文件读写等

### Future

Future是一个trait[^1], 用来表示可能在将来完成的某个异步操作，同时提供了一些方法，如`poll`来检查异步操作是否已经完成

```rust
pub trait Future {
    /// 表示异步计算的最终输出结果
    type Output;

    /// poll意为轮询
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

> Pin in Rust: 如果一个结构体同时保存了数据与指向数据的指针(裸指针)，在move时，结构体进行copy/clone, 此时尽管数据的值没有变，但是地址却发生了变化，而仅复制了值的指针就会指向的一个错误的位置，而使用Pin对目标进行包裹，则增加了一个 !Unpin 特征，移动实现了 !Unpin 特征的变量时，会发编译错误

rust async标记的方法/代码块就会自动的编译一个 future 状态机，调用 `poll` 方法，则future会尝试推动其到下一个状态，如果future被完成，则会返回一个 `Poll::Ready`，并讲异步调用的结果保存在其中

而如果 future 无法被完成，如其等待的资源尚未准备好，则调用 `poll` 方法会返回 `Poll::Pending` , 表示 future 将会在之后完成，调用者应当稍后在调用 `poll` 方法

### Executors

异步方法会返回一个 Future 对象，并通过调用 `poll` 方法推动状态的变化, 同时一个 Future对象可以由其他future组成

而调用 `poll` 方法的，通常是异步执行器(Executors), 异步执行器中会维护一个 future 队列，并不断地从其中取出 future 进行 `poll`， 当然，如果执行器只是不停地轮询，这样显然是非常低效的，因此在还需要信号手段来优化这一过程

### Waker

`poll` 中的另一个参数 `cx` 中保存了一个 `waker`， 这使得当 `future` 认为自己能够改变状态时，可以通过 `waker` 向执行器发送信号来请求调度


### async && await

`async` 关键字可用于方法或代码段，其本身是语法糖，能够将函数或代码块转化为一个 Future 对象，这一过程发生在编译阶段，其会将一个函数转化为一个 future 状态机， 调用 `poll` 方法能够推动状态机的状态变化

```rust
// This function:
async fn foo(x: &u8) -> u8 { *x }

// Is equivalent to this function:
fn foo_expanded<'a>(x: &'a u8) -> impl Future<Output = u8> + 'a {
    async move { *x }
}
```

状态机主要由三部分组成
- 保存变量状态的结构体: 原本的变量将会保存到此结构体中，以便在来回切换时能保存状态
- 状态的枚举: 表示 future 的状态
- 对结构体实现的Future trait: 依据状态处理

`await` 关键字同样是一个语法糖，其只能对Future对象使用， 实际过程是等待 Future 对象执行完毕，否则则中断当前future的执行

## Tokio


### basic

Tokio除了提供一个执行器以及配套的宏, 如下 `main` 方法实际被封装为一个 Future 对象，`#[tokio::main]`宏展开之后是真正的 `main` 函数，其会初始化一个执行器，并将当前的 future `main` 提交到执行器中，并开始执行

```rust
#[tokio::main]
async fn main() -> Result<()> {
    ...
    Ok(())
}
```
用户也可以自己将future提交给执行以实现并发
- 执行器会选择一个可执行的 future 进行执行， 如果直接写在一个 future 中，则通常只能串行执行

```rust
// spawn task
tokio::spawn(<future>);

// spawn task and get the result
let handle = tokio::spawn(async {
    // Do some async work
    "return value"
});

// Do some other work

let out = handle.await.unwrap();
```
### Network && I/O

tokio 提供了与标准库完全相同的异步I/O实现，使用思路与标准库一致，只不过都是异步的

### Channels && Select

线程之间可以通过 Channel 进行消息传递，而 tokio 则提供了一套异步的消息传递方案，用于在异步task之间进行消息传递

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);
    let tx2 = tx.clone();

    tokio::spawn(async move {
        tx.send("sending from first handle").await;
    });

    tokio::spawn(async move {
        tx2.send("sending from second handle").await;
    });

    while let Some(message) = rx.recv().await {
        println!("GOT = {}", message);
    }
}
```

同样的，对于存在多个管道时，tokio 提供了类似go selec的机制

```rust
use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx1, rx1) = oneshot::channel();
    let (tx2, rx2) = oneshot::channel();

    tokio::spawn(async {
        let _ = tx1.send("one");
    });

    tokio::spawn(async {
        let _ = tx2.send("two");
    });

    tokio::select! {
        val = rx1 => {
            println!("rx1 completed first with {:?}", val);
        }
        val = rx2 => {
            println!("rx2 completed first with {:?}", val);
        }
    }
}
```

### stream

Iterator的异步实现

```rust
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() {
    let mut stream = tokio_stream::iter(&[1, 2, 3]);

    while let Some(v) = stream.next().await {
        println!("GOT = {:?}", v);
    }
}
```



[1]: [std_future](https://rust-lang.github.io/async-book/02_execution/02_future.html)