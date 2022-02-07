## kernel测试问题

- 问题描述
  - test make 时报错

```shell
$ make ARCH=native mainargs=k run 

**/home/fhl/workplace/exp/pa/ics2021/abstract-machine/am/src/native/platform.h:23:11: error: variably modified ‘sigstack’ at file scope
   23 |   uint8_t sigstack[SIGSTKSZ];**
```

- 问题分析
  - Ubuntu 21.10 中标准库 signal.h 稍有变化
    - 增加了头文件 "# include <bits/sigstksz.h>"
    - 其中取消了头文件 "# include <bits/sigstack.h>" 中使用的 "define SIGSTKSZ 8192" 的静态定义，修改为 "define SIGSTKSZ sysconf (_SC_SIGSTKSZ)"
    - 这导致直接使用 "uint8_t sigstack[SIGSTKSZ]" 时会产生 "variably modified ‘sigstack’ at file scope" 错误, 而在vscode中报错"常量表达式中不允许函数调用"

- 解决方法
  1. 将 SIGSTKSZ 修改为 8192, 编译正常，运行正常
     - 程序泛用性降低，切无法预知未来的错误
  2.   