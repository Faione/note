# Uboot

修改 uboot 环境变量, 使得 uboot 启动时, 会自动地从 sd 卡中读取内核镜像到目标内存, 并跳转执行

```
setenv load_arce_os fatload mmc 1:0 43000000 helloworld_visionfive2-riscv.bin
setenv arce_bootcmd go 0x43000000
setenv bootcmd "run load_arce_os;run arce_bootcmd"

bootcmd=run load_vf2_env;run importbootenv;run load_distro_uenv;run boot2;run distro_bootcmd
```


## SV39 MMU 设置

物理内存范围 `0x4000_0000..0x2_3fff_ffff`, 考虑内核需要对物理地址进行直接操作, 因此这部分地址采用直接映射

编译时指定内核从 `0xffff_ffc0_4300_0000` 开始, 为使保证内核内部地址访问的正确性, `0xffff_ffc0_4000_0000..0xffff_ffc2_3fff_ffff` 需要映射到 `0x4000_0000..0x2_3fff_ffff`


0x4000_0000..0x2_3fff_ffff

0x0_4000_0000..0x0_8000_0000
0x0_8000_0000..0x0_c000_0000
0x0_c000_0000..0x1_0000_0000
0x1_0000_0000..0x1_4000_0000
0x1_4000_0000..0x1_8000_0000
0x1_8000_0000..0x1_c000_0000
0x1_c000_0000..0x2_0000_0000
0x2_0000_0000..0x2_4000_0000


0xffff_ffc0_4000_0000..0xffff_ffc2_4000_0000

0xffff_ffc0_4000_0000..0xffff_ffc0_8000_0000
0xffff_ffc0_8000_0000..0xffff_ffc0_c000_0000
0xffff_ffc0_c000_0000..0xffff_ffc1_0000_0000
0xffff_ffc1_0000_0000..0xffff_ffc1_4000_0000
0xffff_ffc1_4000_0000..0xffff_ffc1_8000_0000
0xffff_ffc1_8000_0000..0xffff_ffc1_c000_0000
0xffff_ffc1_c000_0000..0xffff_ffc2_0000_0000
0xffff_ffc2_0000_0000..0xffff_ffc2_4000_0000


0x4000_0000:   000000001  2 * 0  16 *0 12 * 0
PGD: 0_0000_0001 (0x1)

0_8000_0000:   000000010  2 * 0  16 *0 12 * 0
PGD: 0_0000_0010 (0x2)

...

0x2_4000_0000: 000001001  2 * 0  16 *0 12 * 0
PGD: 0_0000_1001 (0x9)


----

0xffff_ffc0_4000_0000:   100000001  2 * 0  16 *0 12 * 0
PGD: 1_0000_0001 (0x101)

0_8000_0000:   000000010  2 * 0  16 *0 12 * 0
PGD: 1_0000_0010 (0x102)

...

0x2_4000_0000: 000001001  2 * 0  16 *0 12 * 0
PGD: 1_0000_1001 (0x109)




