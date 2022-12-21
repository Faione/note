## 全志D1

1KB = 2^{10} = 4 * 2^{2*4} = 0x400
1GB = 2^{30} = 4 * 2^{7*4} = 0x40000000

> /D1_User_Manual_V0.1/34

DRAM SPACE | 0x4000 0000---0xBFFF FFFF

因此程序必须写在 0x4000 0000 才可以被执行

## 串口

### 转接驱动

安装 `FT232` 驱动, [驱动链接](http://ftdichip.cn/Drivers/D2XX/Linux/libftd2xx-x86_64-1.4.27.tgz)


### 串口软件

使用 `--imap lfcrlf` 来让那让 rustSBI 输出正常, [错误原因](https://unix.stackexchange.com/questions/283924/how-can-minicom-permanently-translate-incoming-newline-n-to-crlf)

```
$ sudo picocom -b 115200 /dev/ttyUSB0 --imap lfcrlf
```

## 烧录 


### xfel 烧录

测试启动模式 `xfel --------> see -> kernel`, [rustSBI使用手册](https://github.com/rustsbi/rustsbi-d1)
- xfel 工具能够直连开发板并执行执行程序

编译  `see.bin`

```shell
# project rustsbi-d1
$ cargo make --see
```

需要注意, Licheel Dock 内存启始地址为 `0x40000000`, [参考博客](https://blog.hutao.tech/posts/boot-os-from-d1/)

```shell
# 初始化
$ xfel ddr d1

# 将程序写入开发板内存
$ xfel write 0x40000000 target/riscv64imac-unknown-none-elf/release/see.bin

# 执行程序
$ xfel exec 0x40000000
```







