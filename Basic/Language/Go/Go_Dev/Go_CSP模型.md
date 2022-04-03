# Go CSP模型


## 一、CSP概念

- CSP: Communicating Sequential Process 
  - 通信顺序进程，是一种并发编程模型
  - 用于描述两个独立并发的并发实体通过共享的通讯**Channel**进行通信的并发模型
  - Process/Channel
    - 这两个并发原语之间没有从属关系
    - Process 可以订阅任意个 Channel，Channel 也并不关心是哪个 Process 在利用它进行通信
    - Process 围绕 Channel 进行读写，形成一套有序阻塞和可预测的并发模型

## 二、Go CSP

- go语言中的协程 goruntime 与 管道 channel 对应于CSP模型中的 Process 和 Channel
  - 不要通过共享内存来通信，而要通过通信来实现内存共享

### Goruntime 调度器

- Go并发调度: G-P-M模型
