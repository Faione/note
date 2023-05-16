
- [rust base](https://doc.rust-lang.org/book)

- [crate仓库](https://crates.io/)
- [格式化打印](https://blog.csdn.net/linysuccess/article/details/123971519)
- [rust构建脚本](https://course.rs/cargo/reference/build-script/intro.html)
- [rust月刊](https://rustmagazine.github.io/)


- [rustup](https://rust-lang.github.io/rustup/cross-compilation.html)
- [rust_platform_support](https://doc.rust-lang.org/nightly/rustc/platform-support.html)

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

## WorkSpace

[](https://kaisery.github.io/trpl-zh-cn/ch14-03-cargo-workspaces.html)

在 Rust 中，! 被称为 never type，表示一个永远不会有值的类型。 它可以用作函数的返回类型，表示函数永远不会正常返回，而是在运行时发生 panic

## Global Variablesk


[](https://www.sitepoint.com/rust-global-variables)

## Reference

[string_vs_str](https://blog.thoughtram.io/string-vs-str-in-rust/)

[ownership](https://blog.thoughtram.io/ownership-in-rust/)

## Deref

?`*<*T>` 对应方法 `<*T>.deref()`, 会返回T, 这是一个栈上数据 

## 裸指针转化

智能指针(Smart Pointer)和 Rust 中的其他两类指针：裸指针 `*const T/*mut T` 和引用 `&T/&mut T` 一样，都指向地址空间中的另一个区域并包含它的位置信息。但它们携带的信息数量不等，需要经过编译器不同等级的安全检查，所以它们在可靠性和灵活程度也有所不同
- 裸指针`*const T/*mut T`基本等价于 C/C++ 里面的普通指针`*T`，它自身的内容仅仅是一个地址。它最为灵活，但是也最不安全。编译器只能对它进行最基本的可变性检查(只读的数据不能写)，通过裸指针解引用来访问数据的行为是 unsafe 行为，需要被包裹在 unsafe 块中
- 引用`&T/&mut T`实质上只是一个地址范围，但是 Rust 编译器会在编译的时候进行比较严格的借用检查 (Borrow Check)，来确保在编译期就解决掉很多内存不安全问题
- 智能指针不仅包含它指向区域的地址范围，还含有一些额外的信息，因此这个类型的大小大于裸指针的大小，属于一种"胖"指针。从用途上看，它不仅可以作为一个媒介来访问它指向的数据，还能在这个过程中起到管理和控制的功能

将`usize`转化为裸指针是允许的，但是任何对于裸指针数据的访问都是`unsafe`的



第一个 `as` 用于消除类型， 第二个 `as` 则从一个无类型的应用转化为 `u8`

```
&T as *const _ as *mut
```