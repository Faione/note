# 环境配置

- [tutorial](http://rcore-os.cn/rCore-Tutorial-Book-v3/)
- [2022训练营](https://learningos.github.io/rust-based-os-comp2022/)
- [guidence](https://github.com/LearningOS/rCore-Tutorial-Code-2022S)
- [blogos](https://os.phil-opp.com/freestanding-rust-binary/)

**RiscV**

- [guidence](https://github.com/riscv-non-isa/riscv-asm-manual/blob/master/riscv-asm.md)
- [参考](https://riscv.org/wp-content/)


qemu
- `ctrl` + `a` then `x` to quit from qemu

- 解决vscode rust报错`can't find crate for `test``
  - [](https://www.cnblogs.com/dou-fu-gan/p/15870905.html)

- 当前工作区中增加配置

```json
{
	"rust-analyzer.checkOnSave.allTargets": false,
	"rust-analyzer.checkOnSave.extraArgs": [
			"--target",
			"riscv64gc-unknown-none-elf"
	]
}
```

## ELF数据格式

查看elf文件中的内容

```shell
$ rust-readobj -all <target_file>
```

ELF内容构成(?不区分顺序)
- ELF header
- 若干个 program header
- 程序各个段的实际数据
- 若干的 section header

示例

```
File: target/debug/os
Format: elf64-x86-64
Arch: x86_64
AddressSize: 64bit
LoadName:
ElfHeader {
Ident {
   Magic: (7F 45 4C 46)
   Class: 64-bit (0x2)
   DataEncoding: LittleEndian (0x1)
   FileVersion: 1
   OS/ABI: SystemV (0x0)
   ABIVersion: 0
   Unused: (00 00 00 00 00 00 00)
}
Type: SharedObject (0x3)
Machine: EM_X86_64 (0x3E)
Version: 1
Entry: 0x5070
ProgramHeaderOffset: 0x40
SectionHeaderOffset: 0x32D8D0
Flags [ (0x0)
]
HeaderSize: 64
ProgramHeaderEntrySize: 56
ProgramHeaderCount: 12
SectionHeaderEntrySize: 64
SectionHeaderCount: 42
StringTableSectionIndex: 41
}
......
```

- Magic: 魔数，一个独特的常数，存放在 ELF header 的一个固定位置
  - 当加载器将 ELF 文件加载到内存之前，通常会查看 该位置的值是否正确，来快速确认被加载的文件是不是一个 ELF 
- Entry: 给出可执行文件的入口点
- 除了 ELF header 之外，还有另外两种不同的 header，分别称为 program header 和 section header，ELF header 中给出了其他两种header 的大小、在文件中的位置以及数目，以 `*EntrySize/*Offset/*Count` 的条目给出

Section head
- 名为 `.text` 的代码段将要被加载到地址 `0x5070` 处，大小为 `208067`

```
Section {
   Index: 14
   Name: .text (157)
   Type: SHT_PROGBITS (0x1)
   Flags [ (0x6)
      SHF_ALLOC (0x2)
      SHF_EXECINSTR (0x4)
   ]
   Address: 0x5070
   Offset: 0x5070
   Size: 208067
   Link: 0
   Info: 0
   AddressAlignment: 16
   EntrySize: 0
}
```

程序符号表

```
Symbol {
  Name: _start (37994)
  Value: 0x5070
  Size: 47
  Binding: Global (0x1)
  Type: Function (0x2)
  Other: 0
  Section: .text (0xE)
}
 Symbol {
    Name: main (38021)
    Value: 0x51A0
    Size: 47
    Binding: Global (0x1)
    Type: Function (0x2)
    Other: 0
    Section: .text (0xE)
 }
```



机制和策略分离
- 进程的机制 与 进程的调度

操作系统软件与硬件如何配合

- 抓住主干, 完善细节
- 先分层次, 后写功能

向上取整
- x / y = a, 结果是向下去整, 意味 a 个 y 在加上一个 余数 b, 才与x相等
  - b 的取值范围是 [0, y)
- 向上取整, 意味着得到的结果 c * y >= x, 要想得到这个c, 不妨这样思考, x/y 的余数取值范围是 [0, y)
  - 若余数为 0, 则a即是c, 若余数 (0, y), 则c = a + 1
  - 若将 x 增加 y-1, 则余数也会增加 y-1, 而只有当余数为0 时, 才不会使得商+1, 满足要求 
