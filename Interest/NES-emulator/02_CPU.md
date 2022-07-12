# NES CPU

- [6502指令集](https://www.nesdev.org/obelisk-6502-guide/reference.html)

## 工作模式

- 取指、译码

## 相关crate

- bitflags
  - 进行比特位的操作
    - 设置bit位、判断bit位

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
  - 将内存中的值，寄存器A中的值，与进位相加
  - 如果发生溢出，则设置进位
  - 用来进行多byte的加法


- [6502 加法规则](http://www.righto.com/2012/12/the-6502-overflow-flag-explained.html)
- [6502 溢出规则](http://www.righto.com/2013/01/a-small-part-of-6502-chip-explained.html)

## 指令AND

- Logical AND运算
  - 读出一个内存值，与寄存器A中的值按位与
  - 将结果写入寄存器A中

## 指令ASL

- Arithmetic Shift Left
  - 将寄存器A或内存中的值左移1一个bit
  - bit `0` 设为 `0`, bit `7` 放置在 carry flag 中

## Branch指令

- BCC - Branch if Carry Clear
  - 如果carry flag未使能，则向当前PC增加一个偏移
  - 使得程序执行流跳转至新的位置
  - 此时pc指向偏移量的地址，取出偏移后，pc应当+1, 因此，jump的地址应当为 pc + offset + 1 

- BCS - Branch if Carry Set
- BEQ - Branch if Equal
- BNE - Branch if Not Equal
- BMI - Branch if Minus
- BPL - Branch if Positive
- BVC - Branch if Overflow Clear
- BVS - Branch if Overflow Set
  

