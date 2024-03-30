# Bpf

[bpf_doc](https://www.kernel.org/doc/html/latest/bpf/index.html)

Bpf是内核提供的一种机制，允许用户向内核中的特定位置插入定制化的代码来实现对内核的探测或修改。当前Bpf主要适用场景在于网络子系统中

Bpf程序流程
- 编写bpf程序
- 编译为字节码
- BPF_PROG_LOAD: 验证并将BTF metadata加载到内核中
- BPF_LINK_CREATE: 将一个 bpf prog attach 到指定目标，并获取其fd用以管理
  - BPF_PROG_ATTACH: 仅 attach
- 其他BPF操作
- 当持有LINK的用户进程结束时，BPF程序也会被回收

## Prog Type

[prog_type](https://www.kernel.org/doc/html/latest/bpf/libbpf/program_types.html#program-types-and-elf)

开发者编写bpf prog时声明的`ELF Section Name`实质上就决定了prog的`Program Type`与`Attach Type`。开发者在attach bpf prog时也可以修改`Attach Type`，bpf系统调用会进行相应的检查

## Libbpf

libbpf中定义了一系列对bpf_prog/bpf_map进行操作的函数，用户在编写代码时依赖其中的内容

## Syscall

[bpf_syscall](https://www.kernel.org/doc/html/latest/userspace-api/ebpf/syscall.html)

libbpf中与内核交互的部分通过[`bpf`](https://elixir.bootlin.com/linux/latest/source/kernel/bpf/syscall.c#L5418)系统调用实现， 枚举[`bpf_cmd`](https://elixir.bootlin.com/linux/latest/source/include/uapi/linux/bpf.h#L866)中定义了所有操作Bpf的命令。

## Running 

未开启JIT时，ebpf字节码将有BPF虚拟机进行解释执行，[`___bpf_prog_run`](https://elixir.bootlin.com/linux/latest/source/kernel/bpf/core.c#L1694)

而如果使能了JIT，则eBPF字节码被加载之后，还会进行编译，并在触发时直接运行编译好的机器码，从而提升执行效率
