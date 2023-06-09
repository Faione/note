# Utils

## elf & strip-all

一般而言, 代码编译之后所得到的可执行文件通常是 `elf` 格式的, 这意味着二进制文件中除代码, 数据以外, 还包含有额外的信息, 这些信息有助于操作系统在为进程创建虚拟地址空间时将各个段映射到正确的位置上, 并获取程序入口等信息, 以正确地加载, 运行程序, 这些信息包括[^1]
- `ELF header`: 是 ELF 文件中的第一个部分，它包括了 ELF 文件的基本描述信息，例如机器类型、字节顺序、文件版本、入口地址、段表信息等。它还包括了可执行文件的大小、节表偏移量和节表数量等重要信息，以及其他对于 ELF 文件格式全局性质的描述
- `Program Header`: 可以视为 ELF 文件中的元数据，它包含了 ELF 文件在内存中的布局信息，描述了 ELF 文件中各个 Segment 的位置、类型、权限等属性。Segment 按照程序逻辑被映射到进程的虚拟地址空间中，所以也可以理解成是 ELF 文件被载入内存后在进程地址空间内的表示
- `Section Header`: 一个ELF文件中到底有哪些具体的 sections，由包含在这个ELF文件中的 section head table(SHT)决定。每个section描述了这个段的信息，比如每个段的段名、段的长度、在文件中的偏移、读写权限及段的其它属性

[^1]: [elf_intro](https://zhuanlan.zhihu.com/p/286088470)

## readelf

通过 `readelf -h`, `readelf -l`, `readelf -S` 可以分别获取 `ELF header`, `Program Header`, `Section Header`

通过 `readelf -s` 可以获取 elf 文件中的符号表, 这些符号可在debug提供帮助, 但并非是必要的

## objcopy

objcopy可用于裁剪elf的信息, 如使用 `strip-all` 将 elf 文件中所有的符号和调试信息进行删除, 而 `-O binary` 将会清楚所有的 elf 头, 只保留代码段和数据段, 这样的代码可以直接在裸机上加载运行

```shell
objcopy --strip-all <elf> -o binnary <bin>
```

## objdump

objdump 提供了一种从二进制视角观察代码的方式, 对于 elf 文件, 可以直接通过 `objdump -D` 来反汇编elf文件, 这是因为 elf 头中提供了关键的架构和格式信息, 而对于 binary 文件, 由于没有 elf 头, 因此需要手动提供架构与格式信息, 如 `objdump -m i386:x86-64 -b binary -D` 来进行反汇编, 当前系统中的 objdump 所支持的架构可以通过 `objdump --help` 进行查询, 其中 `targets` 是文件格式, 如 `binary`, 而 `architectures` 是架构, 如 `i386:x86-64`

```
objdump: supported targets: elf64-x86-64 elf32-i386 elf32-iamcu elf32-x86-64 pei-i386 pe-x86-64 pei-x86-64 elf64-little elf64-big elf32-little elf32-big pe-bigobj-x86-64 pe-i386 pdb elf64-bpfle elf64-bpfbe srec symbolsrec verilog tekhex binary ihex plugin

objdump: supported architectures: i386 i386:x86-64 i386:x64-32 i8086 i386:intel i386:x86-64:intel i386:x64-32:intel iamcu iamcu:intel bpf xbpf
```

而对于elf文件, 可以进一步通过 `objdump -j .text -d` 对目标 section 进行反汇编

对于 riscv 体系结构, 则可以通过 `riscv64-linux-gnu-objdump` 工具进行反汇编