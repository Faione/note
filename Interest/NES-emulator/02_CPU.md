# NES CPU

- [6502指令集](https://www.nesdev.org/obelisk-6502-guide/reference.html)

## 工作模式

- 取指、译码

## 指令 LDA

- [load Accumulator](https://www.nesdev.org/obelisk-6502-guide/reference.html#LDA)

- 功能
  - 从指定地址读取值到寄存器 accumulator
  - 修改 寄存器A 的值
  - 修改状态 `Z` `N`
    - 符合条件置 `1`
    - 反之置 `0`

- tips
  - 掩码运算
    - 或 `|`
      - 掩码为 `0` 不会产生任何影响
      - 掩码为 `1` 处置1
    - 与 `&`
      - 掩码为 `1` 不会产生任何影响
      - 掩码为 `0` 处置0

## 指令 STA

- 将寄存器 accumulator 存储到指定地址

 
## 指令 BRK

- 中断程序的执行
  - 跳出 CPU 指令循环即可

## 指令TAX

- 复制 Accumulator 中的数据到寄存器 X8


## 指令 INX

- 寄存器X自加1
- 修改标志位

```rust
self.register_x = self.register_x.wrapping_add(1);
```

## 指令ADC

- Add with Carry
  - 将内存中的值，与进位值相加



