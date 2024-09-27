## Data Flow Analysis Foundation

不动点：给定任意一个函数F，对于点X，如果输入与输出相同，则X是函数的不动点

### Partial Order


> partial的含义在于允许集合中存在没有关系的两个元素

- x: 集合中的元素
- $\sqsubseteq$: 在此处表示元素之间的关系（注意不是$\subseteq$），如 "<=", "substring"

![偏序关系](./img/image-23.png)

### Upper and Lower Bound

- S的Upper/Lower Bound: 都可以是S中的元素（符合条件的情况下）
![](./img/image-24.png)

- properties
- 1. 
- 2. 如有glb/lub, 则此b必然是唯一的，即不能同时存在两个或两个以上的glb/lub

![](./img/image-25.png)

### Lattice & Semilattice

一个poset是lattice的前提是，其中**任意**两个元素组成的pair，都有lub和glb

![](./img/image-26.png)

### Complete Lattice

![](./img/image-27.png)

### Product Lattice

![](./img/image-28.png)

### DFA Framework via Lattice

![](./img/image-29.png)

### FPT & Lattice

![](./img/image-30.png)

Proof:
- 鸽笼定理（抽屉定理）：如果有 n+1 个或更多的物体放入 n 个盒子（抽屉）里，那么至少有一个盒子里包含两个或更多的物体
- height of lattice：自底向上的高度（底为0）

![proof_of_fpt](./img/image-31.png)

- 最小不动点
  - 最大不动点证明类似
![least_fixed_point](./img/image-32.png)

### 迭代算法与不动点定理

![](./img/image-33.png)

转换函数的单调性证明
- Gen/Kill操作证明了f执行的单调性

![后继的最小上界单调性证明](./img/image-34.png)