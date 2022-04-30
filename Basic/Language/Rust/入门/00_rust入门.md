# Rust 入门


## window安装

**安装c++工具链**

- 通过指示进行安装
  - 选择 win11 SDK、编译器即可


**通过环境变量配置安装路径**

```
# 可以配置为用户，也可以配置为系统
CARGO_HOME = 
RUSTUP_HOME = 
```
在 Path 中加入 cargo bin 路径

## 安装 rust 环境

```shell
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
**版本升级**

```shell
$ rustup update
```
**卸载**

```shell
# 卸载会删除 rustup 以及 cargo
$ rustup self uninstall
```

**开发环境**

- vscode
  - 安装 rust 扩展，并自动安装相应的工具

## Hello World

**编译**

```shell
# rustc name.rs -o target
$ rustc main.rs
```

**运行**

```shell
$ ./main
Hello World!
```

**格式规范化**

```shell
# 按标准格式规范代码
# Rust的风格是4个空格，而不是制表符
$ rustfmt main.rs
```


## Hello World 代码分析

- println!
  - 这是一个 rust 宏
  - 如果是一个方法，则不应该有"!"
- ";" 作为表达式的结尾

```rust
fn main() {
    println!("Hello, world!)
}
```

## Hello Cargo

- cargo是 rust 的构建系统和包管理工具

**使用cargo创建project**

- 创建project时，cargo的主要工作
  - 创建目录
  - 创建Cargo files
    - Cargo.toml
    - src directory
      - main.rs
  - 初始化git，以及 .gitinore
    - 如果已有 git 的目录，则不会进行创建
    - 可以通过 "cargo new --vcs=git" 进行修改

```shell
$ cargo new hello_cargo
```

- 得到的目录
  - cargo希望所有的源代码都在sr之中

```shell
├── .git
├── .gitignore
├── Cargo.toml
└── src
    └── main.rs
```
**TOML**

- Tom’s Obvious, Minimal Language
  - Cargo 配置文件的风格
- 构成 
  - `[package]`
    - 项目的配置
  - `[dependencies]`
    - 描述项目的依赖
    - rust 中的包称为 crate

**项目构造**

- build会创建 target 文件夹，并将可执行文件放入 target/debug 中

```shell
$ cargo build 
```

**构造 && 运行**

- 编译并允许代码

```shell
$ cargo run
```

**检查**

- 检查源代码，保证能够编译，但不生成可执行文件
  - 仍然会产生target文件夹

```shell
$ cargo check
```
**清除**

- 这将会清除 target 文件夹

```shell
$ cargo clean
```

**release**

- 相比于直接build，release会对源代码进行优化，因此消耗的时间也会更长
  - build: 开发环境，快速build，方便debug
  - release: 生成环境，优化程序运行
    - benchmark时使用


## Cargo 问题

- Blocking waiting for file lock on package cache

- 编译器避免数据争用

- 解决方法
  - 取消其余编译项目
  - 关闭 rls, `pkill rls`
  - 强制解除, `rm -rf ~/.cargo/registry/index/*`

## Cargo国内源

- 在 `~/.cargo` 文件夹中
  - 新建文件config

```config
[source.crates-io]
registry = "https://github.com/rust-lang/crates.io-index"
# 指定镜像
replace-with = 'tuna'

# 清华大学
[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"
```
