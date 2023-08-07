# Boot

uboot 作为启动操作系统的前一阶段, 必须提供启动操作系统的能力, 最简单的方式就是将 操作系统读取到目标内存中, 然后直接使用 `go` 命令跳转到目标地址进行执行

通常而言, 跳转之后不会再返回, 而如果跳转的代码出现错误时, 则仍然会提供一些打印信息辅助debug, 如下异常是因为访问了 `0000000000000000` 指令所产生的

TVAL 寄存器的作用如下：
- 当处理器遇到无效指令（非法指令）时，TVAL 寄存器将会保存该指令的机器码
- 当处理器发生页故障（Page Fault）异常时，TVAL 寄存器将会保存导致页故障的虚拟地址
- 当处理器发生断点（Breakpoint）异常时，TVAL 寄存器将会保存触发断点异常的地址
- 其他类型的异常或中断也可以将相应的信息写入 TVAL 寄存器

EPC 反映的是异常发生时指令的地址

```
EPC: 0000000086000658 RA: 0000000043000038 TVAL: 0000000000000000
EPC: ffffffffc62bb658 RA: ffffffff832bb038 reloc adjusted

SP: 0000000086046f00 GP: 00000000ff734e00 TP: 0000000000000001
T0: 0000000000040000 T1: 00000000fff46288 T2: 0000000000000000
S0: 0000000000000001 S1: 00000000ff7495a8 A0: 0000000000000001
A1: 00000000ff7495a8 A2: 0000000086000658 A3: fffffffffffffffe
A4: 0000000000000002 A5: 0000000043000000 A6: 000000000000000f
A7: 00000000fffa8428 S2: 0000000043000000 S3: 00000000ff7495a0
S4: 0000000000000002 S5: 00000000ffff0bb4 S6: 0000000000000000
S7: 00000000ff749600 S8: 0000000000000000 S9: 0000000000000000
S10: 0000000000000000 S11: 0000000000000000 T3: 0000000000000010
T4: 0000000000000000 T5: 000000000001869f T6: 00000000ff734b20
```