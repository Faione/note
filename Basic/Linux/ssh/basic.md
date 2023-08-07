 SSH基础
## 一、SSH验证原理
SSH利用公钥加密来保证安全  
再用户目录下，.ssh文件夹中保存了当前用户的公钥与私钥  
[ssh密钥认证原理](https://blog.csdn.net/bajiudongfeng/article/details/48225239)
### (1) 登录流程
- 密码登陆
   1. 用户通过SSH客户端向远程主机的SSH服务端发送请求: ssh user@ip
   2. SSH服务端接收到登录请求，将自己的公钥发送给客户端
   3. 客户端利用此公钥，将密码加密，并发送加密后的数据给服务端
   4. 服务端利用私钥解密登录密码，并通过密码的正确性来决定是否允许用户登录

- 公钥登陆
   1. 用户利用ssh客户端生成RSA公钥与私钥
   2. 用户将公钥存放到服务器
   3. 用户通过SSH客户端请求连接SSH服务端，服务端返回一个随机字符串给客户端，同时保留该字符串
   4. 客户端依据私钥加密该串字符并发送给服务端
   5. 服务端接收到加密后的字符串，使用公钥解密并验证，并决定是否允许用户登录  

- 首次登录提示
首次登录时，会弹出验证信息  
```shell
$
The authenticity of host 'host (12.18.429.21)' can't be established. 
RSA key fingerprint is 98:2e:d7:e0:de:9f:ac:67:28:c2:42:2d:37:16:58:4d. 
Are you sure you want to continue connecting (yes/no)?
```
这里即是上述密码登陆流程中的第二步，客户端接收到了来自服务端的公钥，但无法确认其主机的真实性，因而此处使用MD5计算，将原来 1024b RSA公钥缩减为 128b，用以提供用户验证，选择接受之后，就会保存此主机公钥到当前用户的.ssh/known_hosts中，并输入密码登录
> /etc/.ssh 目录中的公钥将被所有用户接受

## 二、SSH配置密钥登录
### (1) 生成私钥、公钥
```shell
ssh-keygen -t rsa -C "备注"
```

| 参数 | 说明                                                             |
| ---- | ---------------------------------------------------------------- |
| -t   | type, -t rsa 表示采用rsa加密方式                                 |
| -b   | 密钥长度, -b 1024 表示采用1024bit的密钥，最大为4096              |
| -f   | 生成的文件名, -f /home/fhl/keys, 表示生产密钥对keys在/home/fhl下 |
| -C   | 备注, -C "备注"                                                  |


### (2) 配置密钥登录
- 传输公钥到目标主机上
win10下使用存在问题
```shell
# 使用时，会执行一个脚本，此时需要git的shell有用
ssh-copy-id user@host
```

- 拷贝并配置公钥到目标主机
1. 在用户目录下的.ssh文件夹中，找到.pub类型的公钥文件，并传输到目标主机
2. 服务端ssh配置
修改 /etc/ssh/sshd_config 文件
```shell
RSAAuthentication yes # 有则配置，无则不管
PubkeyAuthentication yes # 必须配置
AuthorizedKeysFile .ssh/authorized_keys # 默认从 ~ 开始检索，因而需要在用户目录下配置

# 重启sshd服务使配置生效
systemctl restart sshd
```

3. 服务端配置客户端公钥
```shell
# 转到用户目录
cd ~

# 创建 .ssh 文件夹
mkdir .ssh

# 创建 authorized_keys 
touch .ssh/authorized_keys

# 权限赋予, 防止登录失败
# 赋予用户组git的用户git .ssh文件目录的使用权限
chown -R git:git .ssh 
chmod 700 .ssh
chmod 600 .ssh/authorized_keys

# 讲客户端公钥追加至authorized_keys
cat  user.pub >> .ssh/authorized_keys
```

### (3) 不允许主机中某用户使用ssh登录  

原理：ssh登录之后，所分配的git-shell启动便会退出（或是错误的shell，倒是无法使用终端交互），就无法进行命令行地交互了 
- [passwd详解](https://blog.csdn.net/liukaitydn/article/details/83046083)
``` shell
# 修改 /etc/passwd
#git:x:1001:1000::/home/git:/usr/bin/bash
git:x:1001:1000::/home/git:/usr/bin/git-shell

注册名(login_name):口令(passwd):用户标识号(UID):组标识号(GID):用户名(user_name):用户主目录(home_directory):命令解释程序(Shell)
```

关闭 ssh 密码登录

```shell
PasswordAuthentication no
```

### (4) Debug

查看 auth 记录

```shell
$ tail -f /var/log/auth.log
```

- Centos 

```shell
$ tail -f /var/log/secure

$ tail -f /var/log/message
```

- SElinux 拦截
- [SElinux 阻止sshd读取用户的key](https://blog.csdn.net/lanxe/article/details/50739768)

```shell
# 对于 .ssh 文件夹
$ restorecon -R -v .ssh
```
ssh登陆指定 port

```shell
$ ssh -oPort=10101 root@47.108.237.20
```

## Format

从 openssh 7.6 开始提供了更安全的私钥格式，需要进行格式转化，否则会提示 `invalid format`

```shell
ssh-keygen -f ~/.ssh/id_rsa -p
```

[ssh_key_format_invalid](https://serverfault.com/questions/854208/ssh-suddenly-returning-invalid-format)