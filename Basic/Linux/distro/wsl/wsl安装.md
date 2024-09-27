# WSL 安装

## 一、简介

wsl(windows subsystem linux), 即运行在window中的linux系统

## 二、安装

-[官方文档](https://docs.microsoft.com/zh-cn/windows/wsl/install)

以管理员身份运行cmd

```
wsl --install
```

等待安装
- 实际上，只需要等待WSL2内核安装完成即可
- GUI，发行版Linux可以自行在windows store中安装

安装完成之后重启, 初始化linux即可运行

## 三、使用

- vscode 关联: remote wsl插件
- mobaxterm 关联: 自动关联

## 四、问题

### (1) oh-my-zsh字体缺失问题

下载字体
- [DejaVuSansMono](https://github.com/powerline/fonts/tree/master/DejaVuSansMono)

安装完成之后, 右键 wsl terminal 边框, 设置字体

## 五、迁移备份

```
# 关闭虚拟机
wsl --shutdown

# 导出 `Ubuntu-22.04` 实例到 E:\ubuntu2204.tar
wsl --export Ubuntu-22.04 E:\ubuntu2204.tar

# 删除实例
wsl --unregister Ubuntu-22.04

# 导入实例, 设置名称为 `Ubuntu-22.04, 文件系统路径 `F:\VirtualMachines\WSL\Ubuntu2204`, 版本 `2`
wsl --import Ubuntu-22.04 F:\VirtualMachines\WSL\Ubuntu2204 E:\ubuntu2204.tar --version 2
```

如修改了WSL的名称，则WSL会因丢失基础信息，而默认使用root登录，需要参考如下方法修改默认用户
- Inside the instance, as root, create or edit /etc/wsl.conf and add these lines:

```
[user]
default=username
```

[wsl导入导出](https://zhuanlan.zhihu.com/p/406917270)