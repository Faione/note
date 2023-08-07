## Baisc

### C++ 基础

#### 库

包括主要的算法库，input，output等

```c++
#include <bits/stdc++.h>
using namespace std;
```

#### vector

push_back(), emplace_back() 区别在于前者只进行值的拷贝，而后者则会根据参数调用目标类型的构造函数再进行拷贝

#### unordered_map

unordered_map 中的元素为 `pari<K, V>`, 可以通过for循环进行遍历

```c++
// key 为 const
for (pair<const string, int> &p : counts) {
    cout << p.first << " : " << p.second << endl;
}
```

unordered_map 本身无序且不可排序，如要进行排序，则可以将 pairs 保存到 vector 中然后定义 cmp 函数进行排列

```c++
// 按 v 从大到小， k 字典序进行排序
sort(tmp.begin(), tmp.end(),
        [](const pair<string, int> &a, const pair<string, int> &b) {
        if (a.second != b.second) {
            return a.second > b.second;
        }

        return a.first[0] < b.first[0];
        });
```
#### 排序函数

`sort` 是 c++ 中的排序函数，用来对容器中的元素进行排序

#### ACM 模式常用输入输出

核心在于组合 `cin`, `cin.get()`, `getline()`

`cin >> n`: 初始时缓冲区为空，cin 会阻塞，用户键入任意数据并输入enter后, 这些数据会写入缓冲区(包括enter), 此时cin处被唤醒, 然后从缓冲区开始读取数据, 读取数据时，cin会空格, 换行 或 制表符，并读取数据直到再遇到一个 空格, 换行 或 制表符, 将数据写入到 n 对应的内存中, 之后每次调用 `cin >>` 都会重复此操作， 而当缓冲区数据读取完毕时，则进入阻塞

`n = cin.get()`: 从缓冲区读取一个字符

`getline(cin, n)`: 从缓冲区读取数据直到遇到一个 `\n`， `getline` 会取走 `\n` 并一起处理， 而 `cin >> n` 不会将 `\n` 取走 


c++ 中并没有提供 split 的标准实现，如果希望对 string 进行 split 操作，可以使用 `istringstream` 进行处理

```c++
// spilt by ','
vector<string> split(const string &s, char c) {
  string str(s);
  replace(str.begin(), str.end(), c, ' ');
  istringstream input(str);

  vector<string> rlt;
  string tmp;
  while (input >> tmp) {
    rlt.push_back(tmp);
  }

  return rlt;
}
```

提高 c++ io效率
- `cin`需要于`stdin`同步，因此当数据量较大时，存在很大的同步开销，可设置 `ios::sync_with_stdio(false);` 来对 cin 进行加速
- 默认情况下 `cin` 与 `cout` 绑定，即 `cin` 之前会先flush `cout` 的缓冲区，以便快速的将信息进行输出，关闭此绑定能够进一步加快速度


[acm_in_out](https://zhuanlan.zhihu.com/p/494535515)



