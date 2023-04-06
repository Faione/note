# OS2ATC

[living](https://live.csdn.net/room/Hansen666666/wIIp8dGq)

## Microverification of the Linux KVM Hypervisor

00:28:04

Speaker: Ronghui Gu

Content:

papers
- [A secure and formally verified Linux KVM hypervisor](https://ieeexplore.ieee.org/abstract/document/9519433/)
- [Formally verified memory protection for a commodity multiprocessor hypervisor](https://www.usenix.org/conference/usenixsecurity21/presentation/li-shih-wei)
- [Formal verification of a multiprocessor hypervisor on arm relaxed memory hardware](https://dl.acm.org/doi/abs/10.1145/3477132.3483560)
- Spoq: Scaling Machine-Checkable Systems Verification in Coq(to appear)

Deep Specification vs Microverification

将复杂系统区分为 core 与 serve 部分，core是核心部分的代码，serve部分使用到core的内容但并不影响系统安全，仅对core进行形式化验证能够降低工作量

## 基于AIGC的智能编程技术

01:03:23

Speaker：Ge Li

Content:

```
       comprehension
         +------->
+------+           +------+
| code |           |intent|
+------+           +------+
         <-------+
         generation
```

专家知识不可取代

### Rust Monitor 形式化验证

01:35:06

Speaker: 刘双

不太明白，似乎是相比于硬件，Rust Monitor的形式化验证更容易适配多种平台

### 内核漏洞挖掘技术

02:16:56

Speaker: 张超

Content:

类似强化学习的思路，利用生成好的片段来进行攻击，迭代出最有效的片段

## 多样性算力时代下的OS思考

02:47:10

Speaker: 张攀

- [John Hennessy and David Patterson 2017 ACM A.M. Turing Award Lecture](https://www.youtube.com/watch?v=3LVeEjsn8Ts&t=4s)

Content:

> 在有限的时间内，让尽可能多的任务获得其想要的输出结果，然而事实上遍历所有组合以获得全局最优解是不可接受的
> Linux的调度算法不是严格意义上的数学算法，而是一种启发式的算法，即归纳总结

- 从数学原理角度，OS可抽象为JSP+KP双NP难问题，通过化归可得为多对象、多目标优化的JSP问题
- 而从物理角度, OS是对硬件管理的抽象，为应用提供服务并进行管理

基本算力形态: 标量、矢量、矩阵、空间

## 分会

arceos

对于整体而言，减少模块能够减少系统中的调用链路，但并不会减少整体调用

unikernel相比于精简linux的意义更多在于模块化


