# Gdb内存分析

## 变量地址打印

```
(gdb) print &user
```

## 查看内存

```
(gdb) x /4xb &user.age
```

- 大小端判断
  - 大端: 数字高位存放在低地址
  - 小端: 数字低位存放在低地址


![小端存储](./img/2022-04-23-09-59-10.png)

- [gdb查看内存](http://c.biancheng.net/view/7470.html)
- [gdb内存分析](https://www.cnblogs.com/azhao/p/12074656.html)

## 反汇编

- `x/10i $pc`
  - 从当前PC值的位置开始，在内存中反汇编10条指令

- `p/x $t0`
  - 以16进制打印寄存器 t0 的值
- `p/d $x1`
  - 以10进制打印寄存器 t0 的值