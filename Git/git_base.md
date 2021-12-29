# Git

## 一、 git安装

包管理工具安装

```shell
$ yum install git
```

源码编译安装
   - [源码编译安装git](https://cloud.tencent.com/developer/article/1626792)



## 二、基础操作
### 1. 初始化git
- 初始化用户信息
> 用户名称（每次提交），用户邮箱

```shell
git config --global user.name "fhl"
git config --global user.email 1287481902@qq.com
```

- 查看git config信息

```shell
git config --list

git config user.name
```
### 2. git常用操作

### 3. git私有仓库搭建
[使用git + ssh完成本地到服务器的git同步](https://blog.csdn.net/u010597189/article/details/81284642)
#### （1） 在服务上创建仓库
```shell
# 某一目录下init git仓库
git init --bare // 使用bare标识此目录只存储 .git 中的信息，而不会创建 .git 文件夹

此仓库的Url为: username@ip:$PWD 
                    eg: git@47.108.237.20:/home/git/Disk/repository
```
#### (2) clone仓库
先clone仓库，则可以保存远程目录信息，方便推送
```shell
git clone git@47.108.237.20:/home/git/Disk/repository MyNote // MyNote 为本地目录

没有配置ssh密钥，则需要再输入密码
每需要密钥登录，都应当将自己的公钥写入ssh 的authority_keys中
```
#### (3) 仓库操作
```shell
# 拉取
git pull // git pull 等同于 git fetch && git merge, 即取得远程的分支，并将其合并到当前的分支中

# merge冲突的原因是: 两个已经提交的分支的相同文件相同位置的的不同操作进行了合并

# 推送
git push
```