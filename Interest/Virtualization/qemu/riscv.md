# Boot Process

如下命令会通过 qemu 创建一个虚拟机, 包括一颗 risc-v cpu, 128M 内存, 以及各种外设

```
qemu-system-riscv64 -nographic -m 128M -smp 1 -machine virt -bios default -kernel <img>
```

## 初始化

而在命令键入之后, qemu 首先会对所设置的虚拟机进行初始化, 在内存起始处放置 opensbi 代码, 并将 img 读取到内存地址 `0x80200000` 处

> `0x80000000`: 物理内存的位置
> `0x80200000`: opensbi/qemu 默认的内核位置?

通过如下命令可以获取qemu模拟设备的设备树

```shell
qemu-system-riscv64 -machine virt -machine dumpdtb=riscv64-virt.dtb -bios default

dtc -I dtb -O dts -o riscv64-virt.dts riscv64-virt.dtb

cat riscv64-virt.dts | less
```

很容易就可以找物理内存的起始地址 `0x80000000`

```
memory@80000000 {
        device_type = "memory";
        reg = <0x00 0x80000000 0x00 0x8000000>;
};
```

## OpenSBI

随后CPU读取内存中的第一条指令并开始执行, 而这部分代码一般是opensbi, 用以进行初步的设备发现与内存初始化, 而在完成这些基础工作后, OpenSBI会将当前正在使用的cpu hardid, 以及设备树的地址分别保存到 `a0`, `a1` 寄存器中, 并跳转到 `0x80200000` 处执行内核代码

## Kernel

不同内核代码的执行思路各不相同, 取 demo 内核进行分析, 通过 `readelf -h` 读取内核代码的elf头, 通过 `readelf -S`可以看到内核代码的各个段及其地址, 通过 `objdump -d` 可以反汇编各个段以观察汇编文件.可以看到设置的起始地址为 `0xffffffc080200000`, 对于一般应用而言, 内核会在进程初始化时创建单独的虚拟地址空间, 并将通过解析elf文件, 加载段到对应的位置, 这样CPU就能够正常地通过地址读取到期望的值

```
// 1. save hartid & dtb_ptr
mv      s0, a0
mv      s1, a1

// 2. setup boot stack
la      sp, {boot_stack}
li      t0, {boot_stack_size}
add     sp, sp, t0

// 3. setup boot page table
call    {pre_mmu}
// 4. enable paging
call    {enable_mmu}
// 5. post process paging
call    {post_mmu}
```

而在 demo 内核中, qemu只是将代码放置在了 `0x80200000` 处, 并不存在地址空间, 理论上来说, 在内核设置 `satp` 开启虚拟地址之前, 代码应当无法正常运行

```shell
riscv64-linux-gnu-objdump -d

(gdb): target remote localhost:1234
```

但通过反汇编代码及gdb调试可以发现, 跳转指令的实现是相对寻址而非绝对寻址, 这使得即使尚未启动虚拟地址空间, 也不影响代码的正常跳转, 而在MMU初始化完毕之后, 内核代码就能够继续正常执行了

```
ffffffc080200012:	00000097          	auipc	ra,0x0
ffffffc080200016:	2bc080e7          	jalr	700(ra)
```
