
- [区分](https://www.cnblogs.com/guojun-junguo/p/10429568.html)

- 头文件提供函数的说明，库文件包含函数的实现
  - 库文件通过头文件向外导出接口， 用户通过头文件找到库文件中
  - 动态链接情况下，函数的实现在dll中，通过库文件进行动态链接，dll在函数运行时被调用到


## Const


[const](https://www.cnblogs.com/qxj511/p/4965793.html)
const 所修饰的变量不能够称为左值，即只读

const 与 指针
```C
// p 指向了一个 const int ，即 *p 只读
const int* p

// 指针 p 是被 const 修饰的，即 p 只读，然而 *p 能够被修改
int* const p

// 指针 p 以及指向的值都被 const 修饰, 即 *p 与 p 都是只读的
const int* const p
```

## 复合字面量

`(Type){}` 会创建一个 匿名 的Type类型，并使用 `{}` 中的值进行初始化 

```c
struct Foo *f = &(struct Foo){};

# equals to 
struct Foo temp = {};
struct Foo *f = &temp;
```

[compound_literals](https://gcc.gnu.org/onlinedocs/gcc/Compound-Literals.html)