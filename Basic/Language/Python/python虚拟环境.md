# Python虚拟环境

- [linux python 虚拟环境](https://www.cnblogs.com/Infi-chu/p/10342029.html)

Python虚拟化环境提供一个隔离的开发环境，其中有独立的python解释器与包管理工具pip

```cmd
# 在指定 filename中创建一个虚拟环境
# -m 使得模块 venv 以脚本的方式运行
python -m venv <filename>
```
虚拟环境表现为一套脚本与工具，其并不严格要求程序开发在其中进行，但是需要在其中运行的程序必须与其中的解释器与包管理工具关联