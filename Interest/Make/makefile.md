# MakeFile

[教程](https://www.ruanyifeng.com/blog/2015/02/make.html)

makefile 规则
   - target
   - prerequisites
   - command


[makefile变量赋值](https://www.cnblogs.com/wanqieddy/archive/2011/09/21/2184257.html)

```
= 是最基本的赋值
:= 是覆盖之前的值
?= 是如果没有被赋值过就赋予等号后面的值
+= 是添加等号后面的值
```

[make $](https://blog.csdn.net/dlf1769/article/details/78997967)

```
$@  表示目标文件
$^  表示所有的依赖文件
$<  表示第一个依赖文件
$?  表示比目标还要新的依赖文件列表
```