# Common Collection

- Collection
  - 可以包含多种类型的数据
  - 与数组和元组类型不同，集合指向的数据存储在堆上，因此编译时不必知道数据长度，且可以在运行时伸缩
- 常用 Collection
  - Vector
    - 将可变数量的值彼此相邻存储
  - String
  - Hash Map

## Vector

- [手册](https://doc.rust-lang.org/std/vec/struct.Vec.html)
- [vec deref](https://www.codenong.com/32789069/)

- 允许存储多个相同类型数据的数据结构
  - 值彼此相邻存储，当扩大时，需要重新申请空间
    - 故当使用其中元素的引用时，不能进行扩大，否则会导致borrow的冲突

- 构建

```rust
let v: Vec<i32> = Vec::new();

// 使用宏
let v = vec![1, 2, 3];
```

- 增加元素

```rust
v.push(5);
```

- 读取元素

```rust
match v.get(2) {
    Some(third) => println!("The third element is {}", third),
    None => println!("There is no third element."),
}


let third: &i32 = &v[2];
```

- 遍历元素

```rust
let v = vec![100, 32, 57];
for i in &v {
    println!("{}", i);
}

let mut v = vec![100, 32, 57];
for i in &mut v {
    *i += 50;
}
```

- 使用Enm存储多个类型

## String

- str 是存储在二进制文件中数据类型，通过 `&str` 进行引用
- String 是可增长的、可变的、拥有的、UTF-8编码的字符类型

- push_str
  - 接收 字符串切片 作为输入

```rust
let mut s = String::from("foo");
s.push_str("bar");
```

- push

```rust
let mut s = String::from("lo");
s.push('l');
```

- 字符串拼接
  - add: `+`
    - 要求 String + &str ...
    - 发生 String ownership 的 move
  - `format!` 宏
    - 不会发生 ownership 的move

```rust
let s1 = String::from("tic");
let s2 = String::from("tac");
let s3 = String::from("toe");

let s = format!("{}-{}-{}", s1, s2, s3);
```

- 字符串索引
  - 字符串是 Vec<u8> 的包装器
    - s.len() 指的是 Vec<u8> 的长度，即 byte 大小
  - 字符串不允许使用 `[n]` 进行索引
  - 切片也允许使用 `[n]` 索引, 但考虑 utf-8 编码, 索引结果不一定符合预期(如 1byte 字符与 2byte 字符)
    - rust 不会编译这样的代码

- 使用 range []
  - `&str[0..4]` 获得最开始 4byte 的数据(4 * u8)
  - 如果range范围错误(考虑编码)，则无法编译

- 字符串遍历

```rust
// 遍历字符
for c in "नमस्ते".chars() {
    println!("{}", c);
}

// 遍历比特
for b in "नमस्ते".bytes() {
    println!("{}", b);
}
```
## Hash Map

- 默认使用 SipHash 散列函数

- 构建
  - Map 的键的类型必须相同，值的类型必须相同

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();

scores.insert(String::from("Blue"), 10);
```

- 使用 collect 方法将元组迭代器转化为 map

```rust
use std::collections::HashMap;

let teams = vec![String::from("Blue"), String::from("Yellow")];
let initial_scores = vec![10, 50];

let mut scores: HashMap<_, _> = teams.into_iter().zip(initial_scores.into_iter()).collect();
```

- ownership
  - 对于Copy特征对象，只进行值的拷贝
  - 对于owned对象，则会进行move

- 访问值
  - get的结果是`Option<&V>`

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();

scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);

let team_name = String::from("Blue");
let score = scores.get(&team_name);
```

- 遍历

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();

scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);

for (key, value) in &scores {
    println!("{}: {}", key, value);
}
```

- 仅在空时插入

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);

scores.entry(String::from("Yellow")).or_insert(50);
scores.entry(String::from("Blue")).or_insert(50);

println!("{:?}", scores);
```

- 基于旧值进行更新

```rust
use std::collections::HashMap;

let text = "hello world wonderful world";

let mut map = HashMap::new();

for word in text.split_whitespace() {
    // count 对原值的可变引用，否则 for 之外就会失效
    let count = map.entry(word).or_insert(0);
    *count += 1;
}

println!("{:?}", map);
```

- [continue](https://doc.rust-lang.org/book/ch08-03-hash-maps.html)


