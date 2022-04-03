# Programe -- guessing game

## 库引用

- rust提供标准库，包含一系列基础功能
  - 默认情况下，Rust会将标准库中一些东西放入到任何项目中，这些东西的集合称为 prelude
    - 如 String
  - 不在 prelude 中的类型，需要手动的引入到项目中

```rust
use std::io
```

## 变量声明

- Rust 中 使用 let 语法进行变量声明
  - 默认情况下，所有变量都是不可改变的
  - 如果要让变量可变，则需要加上声明 "mut"

-  "::" 语法
   -  "::new" 表明 new 是String相关的方法

```rust
let mut guess = String::new()
```

## 库方法使用

- "io::stdin()"
  - 如果不引入 io， 也可以使用 "std::io::stdin"
  - 方法将返回一个 "std::io::Stdin" 实例
    - 代表终端标准输入的类型
  - ".read_line(&mut guess)"
    - 调用实例的 read_line 方法，获得用户的输入
    - 将可变参数传入，用来保存用户的输入
    - "&" 表明参数是一个指针
    - 返回一个 "io::Result" 结果
  - 对于 "io::Result" 不做处理，则无法通过编译
    - "expect"

```rust
io::stdin()
    .read_line(&mut guess)
    .expect("Failed to read line");
```

## 占位符 {}

- prinln! 中使用

```shell
println!("You guessed: {}", guess);
```

## 外部库引用

- 在 Cargo.toml 中添加相应的依赖
  - 首次build时，cargo会增加 Cargo.lock 文件
    - cargo 检查所有依赖的版本，并写入 Cargo.lock 文件
    - 之后的每次 build， cargo 都会检查 Cargo.lock 文件，并使用其中定义的依赖版本
- Cargo update 则会忽视 Cargo.lock中的内容，并将最新的内容更新到 Cargo.lock 中

## 生成文档

- cargo doc --open

## 类型转换

- 声明类型
  - `let guess: u32`
- trim()
  - 消除字符两端的空格或换行
- parse()
  - 将字符转化为目标类型

```shell
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

## 循环

```rust
loop {

}
```


- TODO: [next](https://doc.rust-lang.org/book/ch03-01-variables-and-mutability.html)

