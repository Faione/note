# NES CPU

- [6502指令集](https://www.nesdev.org/obelisk-6502-guide/reference.html)
- [6502 CPU 状态](https://www.nesdev.org/wiki/Status_flags)
- [6502汇编](https://wusiyu.me/6502-cpu%e6%b1%87%e7%bc%96%e8%af%ad%e8%a8%80%e6%8c%87%e4%bb%a4%e9%9b%86/)
## 工作模式

- 取指、译码
- 56种操作，151条指令

## 相关crate

- bitflags
  - 进行比特位的操作
    - 设置bit位、判断bit位

## 指令 LDA/LDX/LDY

- [load Accumulator](https://www.nesdev.org/obelisk-6502-guide/reference.html#LDA)

- 功能
  - 从指定地址读取值到寄存器 accumulator/x/y
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

## 指令 STA/STX/STY

- 将寄存器 accumulator 存储到指定地址
- STX - Store X Register
- STY - Store Y Register
 
## 指令 BRK

- 中断程序的执行
  - 跳出 CPU 指令循环即可

## 指令Tranfer

- TAX - Transfer Accumulator to X
  - 复制 Accumulator 中的数据到寄存器 X8
- TXA - Transfer X to Accumulator
  
- TAY - Transfer Accumulator to Y
- TYA - Transfer Y to Accumulator

- TSX - Transfer Stack Pointer to X
  - 将当前的栈指针复制到X寄存器中
- TXS - Transfer X to Stack Pointer

## 指令 INX

- 寄存器X自加1
- 修改标志位

```rust
self.register_x = self.register_x.wrapping_add(1);
```

## 指令ADC/SBC

- ADC - Add with Carry
  - A,Z,C,N = A+M+C
  - 将内存中的值，寄存器A中的值，与进位相加
  - 如果发生溢出，则设置进位
  - 用来进行多byte的加法

- SBC - Subtract with Carry
  - 用来进行多byte的减法
  - 对于减法而言，只需要将操作数转化为取负，并提前减去1，就能复用加法
    - A,Z,C,N = A-M-(1-C)
    - A,Z,C,N = A+(-M-1)+C
  - ？负数补码无符号数字越大，负数越大
    - 无进位，则说明上一步计算有借位，故多减1
    - 有进位，则说明上一步计算够减，无需多减去1

- [6502 加法规则](http://www.righto.com/2012/12/the-6502-overflow-flag-explained.html)
- [6502 溢出规则](http://www.righto.com/2013/01/a-small-part-of-6502-chip-explained.html)

## 指令AND/EOR/ORA

- Logical AND运算
  - 读出一个内存值，与寄存器A中的值按位与
  - 将结果写入寄存器A中

- EOR - Exclusive OR
  - 逻辑异或运算，读出一个内存值，与寄存器A中的值按位异或
  - 将结果写入寄存器A中

- ORA - Logical Inclusive OR
  - 逻辑或运算，读出一个内存值，与寄存器A中的值按位或
  - 将结果写入寄存器A中

## 指令ASL/LSR/ROL/ROR

- Arithmetic Shift Left
  - 将寄存器A或内存中的值左移1一个bit
    - 新值的bit `0` 设为 `0`, A中旧值的bit `7` 放置在 carry flag 中

- LSR - Logical Shift Right
  - 将寄存器A或内存中的值右移1一个bit
    - 旧值的bit`0`移动到carry flag中，因移动所产生的bit`7`用`0`填充

- ROL - Rotate Left
  - 将寄存器A或内存中的值左移1一个bit
  - 新值的bit`0`由carry flag填充，而旧值的bit`7`则移动到carry flag

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

## BIT指令

- Bit test
  - 测试在目标内存位置，一个或多个bit位是否被设置
  - 寄存器A中的值作为掩码，与目标内存位置的值相与
  - 结果中的第7位和第6位复制到N、V中
    - 位数从右往左编码
  - 结果并不保存
  - 影响Z、V、N的值

## CLEAR && SET FLAGS指令

- CLC - Clear Carry Flag
- CLD - Clear Decimal Mode
- CLI - Clear Interrupt Disable
- CLV - Clear Overflow Flag
- SEC - Set Carry Flag
- SED - Set Decimal Flag
- SEI - Set Interrupt Disable
  
## Compare指令

- CMP - Compare
  - 将内存中的值与寄存器A中的值进行比较
- CPX - Compare X Register
  - 将内存中的值与寄存器X中的值进行比较
- CPY - Compare Y Register
  - 将内存中的值与寄存器Y中的值进行比较
- 影响C、Z、N的值
  - 计算`A-M`的结果，并进行Z、N的设置
    - 使用`wrapping_sub`
  - 如果`A>=M`，则将C置为1

## Decrement Memory指令

- DEC - Decrement Memory
  - 将指定内存中的值减去1
  - 影响Z、N
- DEX - Decrement X Register
  - 将寄存器X中的值减去1
- DEY - Decrement Y Register
  - 将寄存器Y中的值减去1

## Increment

- INC - Increment Memory
  - 将指定内存中的值增加1
  - 影响Z、N
- INX - Increment X Register
  - 将寄存器X中的值增加1
- INY - Increment Y Register
  - 将寄存器Y中的值增加1

## JMP指令

- JMP - Jump
  - 设置PC为JMP指令的操作数 

## JSR & RTS指令

- JSR - Jump to Subroutine
  - 将下一条将要执行的指令地址减1压入栈中，并跳转到操作数所给地址
  - 进入子例程，此处即将JSR的操作数的高位地址压入栈中
- RTS - Return from Subroutine
  - 在子例程的结尾处执行，从栈中读出被压入的地址并加1，
  - 离开子例程，此处即将上次JSR的下一条指令的地址设为当前PC，程序继续运行

## NOP指令

- NOP - No Operation
  - 不做任何操作，仅仅让PC加1(对于当前指令而言)

## PHA/PLA

- PHA - Push Accumulator
  - 将当前accumulator数据压入栈中
- PLA - Pull Accumulator
  - 从栈中读出数据写入寄存器a，并设置Z、N

## PHP/PLP

- PHP - Push Processor Status
  - 将当前CPU的状态数据压入栈中
  - 需要置 `BREAK` 与 `BREAK2`
- PLP - Pull Processor Status
  - 从栈中读出CPU的状态数据，并设置为当前CPU的状态
  - `BREAK`与`BREAK2`恢复初始状态，即`0`, `1`

## RTI

- RTI - Return from Interrupt
  - 在中断例程结束时使用，用于恢复CPU状态位
  - 首先从栈中弹出cpu status，然后再弹出pc

## TAY