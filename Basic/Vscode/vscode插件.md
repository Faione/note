# vscode插件

## 一、remote-ssh

默认情况会转发至localhost, 按照如下配置则可以将数据转发至所有端口(0.0.0.0)

```json
"remote.localPortHost": "allInterfaces",
```
**安装插件**

扩展中搜索 Remote-SSH

**使用插件**

打开远程资源管理器, 添加或直接配置 config

config配置参考

```yml

Host <远程主机名称>
    HostName <远程主机IP>
    User <用户名>
    Port <ssh端口，默认22>
    IdentityFile <本机SSH私钥路径>

```

eg:

```yml
Host NJServer
  HostName 58.213.121.2
  User root
  Port 1037
```

## 二、Go开发套件

**安装插件**

扩展中搜索 Go

## 三、GitLens

**安装插件**

扩展中搜索 GitLens

## 三、GitGraph

**安装插件**

扩展中搜索 GitGraph

## 四、常用设置

Open Folders In New Window
 - on: 总是会打开新的窗口
 - off: 默认替换当前窗口
 - default




