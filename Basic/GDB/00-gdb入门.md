# GDB入门

- [gdb常用命令](https://blog.csdn.net/qq_28351609/article/details/114855630)

-  GDB 全称"GNU symbolic debugger", 是Linux下常用的程序调试器

## 准备

- 对于一般编译得到的二进制文件，GDB无法直接进行调试，因为这样得到的二进制文件中，缺少GDB调试所需要的信息
  - 使用gcc编译代码时，增加"-g"参数，使得编译得到的二进制文件能够使用GDB进行调试，而实际更推荐的参数是"-Og"
    - "-Og"有时不会有调试信息

## 简单使用

- 对于包含调试信息的二进制文件, 可以使用GDB进行调试
  - 使用选项 --silent（或者 -q、--quiet）, 让GDB打开时不会显示免责条款
```shell
$ gdb test.out
```

- 查看源代码
  - 默认情况下，l只显示10行源码
```shell
$(gdb) l 
```

- 打断点
  - 参数对应于源码中的行号

```shell
$(gdb) b 2
```

- 运行程序
  - 程序会在断点zanting

```shell
$(gdb) r 
```

- 单步执行程序
  - 触发断点后，可以单步执行程序

```shell
$(gdb) n 
```

- 继续执行程序
  - 程序会继续运行

```shell
$(gdb) c
```
![GDB简单调试命令](2022-03-27-09-45-31.png)


