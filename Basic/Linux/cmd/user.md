# Linux用户管理

- [Linux用户管理](https://www.runoob.com/linux/linux-user-manage.html)

## 一、用户管理

### (1) 增加用户

useradd 选项 用户名

```shell
# -m 参数能够在没有用户目录的情况下创建用户目录
$ useradd -c "a handsome man" -d /home/fhl -s /bin/bash -m fhl 
```

### (2) 删除用户

userdel 选项 用户名

```shell
# -r 选项会将用户及用户家目录一同删除
$ userdel fhl
```

### (3) 修改用户

usermod 选项 用户名

```shell
# -g 为覆盖，-G 为增加
usermod -g normal fhl
```

### (4) 用户口令

新创建的用户没有口令, 无法被其他用户使用(root仍然可以切换), 因此必须为其指定口令

### (5) 切换用户

- [linux用户切换](https://www.cnblogs.com/wzk-0000/p/11083008.html)

- sudo:
   - 暂时切换到 root执行命令
     - "sudo -s": 不加载用户变量(root用户变量), 不跳转目录
     - "sudo -i": 加载用户变量，并跳转至家目录
- su <name>
   - 直接切换到 name 用户  



## 二、组管理

### (1) 增加组

groupadd 选项 用户组

```shell
$ groupadd normal
```
### (2) 删除组

groupdel 用户组

```shell
$ groupdel normal
```

### (3) 修改组

groupmod 用户组

### (4) 切换组

```shell
# 查看当前用户所属用户组
$ groups

# 切换组
$ newgrp root
```

## 二、权限管理

### (1) root权限

先 w!, 再 q! 强制修改

```shell
# $ adduser username sudo 

# $ vi /etc/sudoers
$ visudo

add -> fhl   ALL=(ALL:ALL) ALL
```

- CentOS

```
usermod -aG wheel username
```

- Ubuntu

```
usermod -aG sudo username
```

### (2) 文件权限

所有权变更

- [chown 命令](https://www.runoob.com/linux/linux-comm-chown.html)

chown -R fhl:nomal <file>

权限变更

- [chmod 命令](https://www.runoob.com/linux/linux-comm-chmod.html)

权限分为三级别: 文件所有者, 所有者所在用户组, 其他用户组
权限值: r(4), w(2), x(1)
   - 对应二进制(000), 那个为1则有那个权限, 结果表示为数字
   - 第一个是文件类型
参数说明
  - u(所有者), g(所有者用户组), o(其他)

linux 文件类型

| 文件属性 |                                 文件类型                                 |
| :------: | :----------------------------------------------------------------------: |
|    -     |                             常规文件，即file                             |
|    d     |                                 目录文件                                 |
|    b     |     block device 即块设备文件，如硬盘;支持以block为单位进行随机访问      |
|    c     | character device 即字符设备文件，如键盘支持以character为单位进行线性访问 |
|    l     |               symbolic link 即符号链接文件，又称软链接文件               |
|    p     |                           pipe 即命名管道文件                            |
|    s     |              socket 即套接字文件，用于实现两个进程进行通信               |