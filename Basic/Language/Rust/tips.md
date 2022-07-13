

- [格式化打印](https://blog.csdn.net/linysuccess/article/details/123971519)

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

