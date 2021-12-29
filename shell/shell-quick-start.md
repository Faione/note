
# Shell Quick Start

## keyboard shortcuts

[keyboard shortcuts](https://www.howtogeek.com/howto/ubuntu/keyboard-shortcuts-for-bash-command-shell-for-ubuntu-debian-suse-redhat-linux-etc/)

## Pipe & Redirect

- pipe

操作系统提供的IPC机制，能够将前一个进程的输出作为后一个进程的输入

```shell
$ ls | grep "key"
```

- redirect
   - \> 重定向
   - \>\> 写追加
```shell
# 将 ls 的结果重定向到 ls_out 文件
$ ls > ls_out

# 将 文件中的内容作为 grep 的输入
$ grep "key" < ls_out 
```

## Command检索

- [command not fonund](https://command-not-found.com/)

- [tldr](https://tldr.sh/)

## 检索工具-ag

可以在从当前目录下开始检索目标key的位置(文件，行号)
   - 可以替代 grep 的功能

```shell
# 安装
$ apt-get install silversearcher-ag
# 使用
$ ag main()

```

## 数据处理工具-awk

```shell
# 对于tmp中的每一行，触发一次 '{}' 中定义的操作
cat tmp | awk '{print $2}'
```