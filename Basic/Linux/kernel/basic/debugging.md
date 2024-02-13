# Kernel Debugging

[using_gdb_to_debug_kernel](https://www.starlab.io/blog/using-gdb-to-debug-the-linux-kernel)

## Basic

在内核中开启 Debug 选项并生成 gdb 脚本，再通过 gdb 远程调试的方法来对运行在 Qemu 虚拟机中的 Kernel Debug, 参考[kernel_debugging](https://docs.kernel.org/dev-tools/gdb-kernel-debugging.html)
- 6.x kernel生成的 debug 脚本存在一些问题, 参考[6.x_gdb_scripts_patch](https://lore.kernel.org/lkml/20230607221337.2781730-1-florian.fainelli@broadcom.com/T/#m89733097d8c7bdde834e9977292e09aaf3fd79c8)

使用内核gdb脚本时，注意将脚本加入到安全路径中，`add-auto-load-safe-path /path/to/linux-build`

```shell
$ gdb vmlinux  -ex "target remote localhost:1234"
```

查看对应函数的符号

```shell
lx-symbols 
```

## Hardware Breakpoint

内核代码中的一些部分(如初始化过程)，需要依靠硬件辅助的断点才能够进行debug

```gdb
hbreak start_kernel
```