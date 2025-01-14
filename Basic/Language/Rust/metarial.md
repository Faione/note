[stf](https://reberhardt.com/cs110l/spring-2020/)

[rust syscall](https://docs.rs/nix/latest/nix/index.html)
- [使用说明](https://rustcc.cn/article?id=3bc21774-241d-434d-96b2-e06adafa1be5)

[rust版本控制](https://blog.csdn.net/TowerOs/article/details/104088324)
- 项目目录下的`rust-toolchain.toml`声明了此项目的工具链版本
- nightly相比于stable，提供了unsafe的支持

[rust内联](https://nihil.cc/posts/translate_rust_inline/)
- 指示编译将函数进行内联，而非调用，从而消除函数调用开销

[rustlings](https://github.com/rust-lang/rustlings)

[macros](https://veykril.github.io/tlborm/introduction.html)



[](https://doc.rust-lang.org/nomicon/coercions.html)

```rust
# 数组地址可以与引用地址相同
assert_eq!([2, 3, 4], nice_slice)
```

[ownership & lifecircle](https://blogs.harvard.edu/kapolos/rusty-ownership-and-the-lifecycles-stone/)
[cargo config](https://doc.rust-lang.org/cargo/index.html)