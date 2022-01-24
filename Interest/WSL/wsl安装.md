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

## 三、问题

### (1) oh-my-zsh字体缺失问题

下载字体
- [DejaVuSansMono](https://github.com/powerline/fonts/tree/master/DejaVuSansMono)

安装完成之后, 右键 wsl terminal 边框, 设置字体