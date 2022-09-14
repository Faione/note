
- [crate仓库](https://crates.io/)
- [格式化打印](https://blog.csdn.net/linysuccess/article/details/123971519)
- [rust构建脚本](https://course.rs/cargo/reference/build-script/intro.html)
- [rust月刊](https://rustmagazine.github.io/)

```rust
// 二进制
println!("0b{:b}", 0b11_01); // 0b1101
println!("{:#b}", 0b11_01); // 0b1101

// 八进制
println!("0o{:o}", 10); // 0o12
println!("{:#o}", 10); // 0o12

// 十六进制小写
println!("0x{:x}", 0xFF); //0xff
println!("{:#x}", 0xFF); //0xff

// 十六进制大写
println!("0x{:X}", 0xFF); // 0xFF
println!("{:#X}", 0xFF); // 0xFF

// 打印内存地址
println!("{:p}", &100); //0x7ff7794869c4

// 科学计数
println!("{:e}", 1000f32); // 1e3，科学计数(小写)
println!("{:E}", 1000f64); // 1E3，科学计数(大写)
```

- [rust位运算](https://www.twle.cn/c/yufei/rust/rust-basic-bitwise-operators.html)

| 名字 | 运算符 | 说明                                           | 范例              |
| ---- | ------ | ---------------------------------------------- | ----------------- |
| 位与 | &      | 相同位都是 1 则返回 1 否则返回 0               | (A & B) 结果为 2  |
| 位或 | \|     | 相同位只要有一个是 1 则返回 1 否则返回 0       | (A                | B) 结果为 3 |
| 异或 | ^      | 相同位不相同则返回 1 否则返回 0                | (A ^ B) 结果为 1  |
| 位非 | !      | 把位中的 1 换成 0 ， 0 换成 1                  | (!B) 结果 -4      |
| 左移 | <<     | 操作数中的所有位向左移动指定位数，右边的位补 0 | (A << 1) 结果为 4 |
| 右移 | >>     | 操作数中的所有位向右移动指定位数，左边的位补 0 | (A >> 1) 结果为 1 |


## Rust版本控制

- 

