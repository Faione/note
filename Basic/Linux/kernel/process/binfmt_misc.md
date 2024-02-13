# Kernel Support for miscellaneous Binary Formats

[Kernel Support for miscellaneous Binary Formats](https://www.kernel.org/doc/html/latest/admin-guide/binfmt-misc.html)

内核允许用户为特定类型的程序设置相应的解释器，使得在条件符合时，在shell中调用的程序将会转交给解释器进行执行

内核中完成这一功能的模块是 `binfmt_misc`
- `binfmt_misc` 提供了一套可读写的文件系统与用户进行交互
- 向`register`写入特定的信息来完成解释器的注册
- 

```
echo ":name:type:offset:magic:mask:interpreter:flags" > /proc/sys/fs/binfmt_misc/register
```