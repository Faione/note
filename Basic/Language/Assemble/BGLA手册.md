# Brennan's Guide to Inline Assembly ： by Brennan "Bas" Underwood

- [bgla](http://www.delorie.com/djgpp/doc/brennan/brennan_att_inline_djgpp.html)

## 一、语法

- x86架构处理器所使用的汇编指令一般有两种格式: Intel汇编、AT&T汇编

### （1）寄存器命名

- AT&T中，对于寄存器的命名，会在加上前缀“%”

```s
AT&T: %eax
Intel: eax
```

### (2) 数据源/目标顺序

- AT%T中, 数据源总是在左边, 而数据目标总是在右边
- Intel中, 数据源在右边, 而数据目标在左边

```s
AT$T: movl %eax, %ebx
Intel: mov ebx, eax
```
### (3) 常量/立即数格式

- AT%T中, 常量/立即数之前必须加上前缀 "$"

**常量 -> eax寄存器**

```s
AT$T: movl $_booga, %eax
Intel: mov eax, _booga
```
**立即数 -> eax寄存器

```s
AT$T: movl $0xd00d, %eax
Intel: mov ebx, doodh
```

### (4) 操作数大小声明

- AT$T, 在指令后增加后缀 "l/w/b" 来表明操作数的字长

**mov指令**

|指令|说明|字长|
|:-:|:-:|:-:|
|movl|mov long: 字长传送|32位|
|movw|mov word: 字传送|16位|
|movb|mov byte: 字节传送|8位|

**字长对应**

|C声明|Intel数据类型|汇编代码后缀|大小(字节)|
|:-:|:-:|:-:|:-:|
|char|字节|b|1|
|short|字|w|2|
|int|双字|l|4|
|long|四字|q|8|
|char*|四字|q|8|
|float|单精度|s|4|
|double|双精度|l|8|

```s
AT$T: movw %ax, %bx
Intel: mov bx, ax
```

### (5) 内存引用

**32位寻址范式**

- [80386处理器参考](https://blog.csdn.net/weixin_43569916/article/details/105472194)

- basepointer：可以理解位基址寄存器
- indexpointer：理解为变址寄存器
- indexscale：变址因子
- immed32：偏移量

```s
AT&T:  immed32(basepointer,indexpointer,indexscale)
Intel: [basepointer + indexpointer*indexscale + immed32]
```

**特定变量寻址**

- "_" 是从汇编程序获取静态（全局）C 变量的方式
  - 这仅适用于全局变量,否则需要使用扩展 asm 将变量预加载到寄存器中

```s
AT&T:  _booga
Intel: [_booga]
```

**寄存器直接寻址**

- 寄存器中给出地址

```s
AT&T:  (%eax)
Intel: [eax]
```

**根据偏移与寄存器寻址**

- 通过偏移量与寄存器中的值相加得到地址

```s
AT&T: _variable(%eax)
Intel: [eax + _variable]
```

**数组中寻址**

```s
AT&T:  _array(,%eax,4)
Intel: [eax*4 + array]
```

**立即数寻址**

```s
C code: *(p+1) // where p is a char *
AT&T:  1(%eax)  // where eax has the value of p
Intel: [eax + 1]
```





