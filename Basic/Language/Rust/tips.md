
- [rust base](https://doc.rust-lang.org/book)

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

## range

exclusive range 与 inclusive range
- match 中仅支持 exclusive range

1..5 // 1, 2, 3, 4
1..=5 // 1, 2, 3, 4, 5

## ref 关键字

[ref](https://doc.rust-lang.org/std/keyword.ref.html)


## install

```shell
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 中科大源
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup
```

## 易失性读写 read/write_volatile

有些时候，编译器会对一些访存行为进行优化。举例来说，如果我们写入一个内存位置并立即读取该位置，并且在同段时间内其他线程不会访问该内存位置，这意味着我们写入的值能够在 RAM 上保持不变。那么，编译器可能会认为读取到的值必定是此前写入的值，于是在最终的汇编码中读取内存的操作可能被优化掉。然而，有些时候，特别是访问 I/O 外设以 MMIO 方式映射的设备寄存器时，即使是相同的内存位置，对它进行读取和写入的含义可能完全不同，于是读取到的值和我们之前写入的值可能没有任何关系。连续两次读取同个设备寄存器也可能得到不同的结果。这种情况下，编译器对访存行为的修改显然是一种误优化

于是，在访问 I/O 设备寄存器或是与 RAM 特性不同的内存区域时，就要注意通过 read/write_volatile 来确保编译器完全按照我们的源代码生成汇编代码而不会自作主张进行删除或者重排访存操作等优化

[](https://doc.rust-lang.org/stable/std/ptr/fn.read_volatile.html#notes)

## 自旋

Rust 提供了 spin_loop_hint 函数，我们可以在循环体内调用该函数来通知 CPU 当前线程正处于忙等待状态，于是 CPU 可能会进行一些优化（比如降频减少功耗等），其在不同平台上有不同表现

## Atomics and Locks

[](https://marabos.nl/atomics/)