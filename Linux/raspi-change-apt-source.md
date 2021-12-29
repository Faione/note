# 树莓派更新apt镜像源

- [更换ali源](http://www.shumeipaiba.com/wanpai/jiaocheng/16.html)
- [密钥认证问题](http://www.bubuko.com/infodetail-3674592.html)

## 一、配置apt镜像源

修改 /etc/apt/source.list

```yml
deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
```

修改 /etc/atp/source.list.d/rasp.list

```yml
deb http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/ stretch main ui
```

密钥认证问题

```shell
# <KeyServer>: keyserver.ubuntu.com, <公钥签名>: 9165938D90FDDD2E
$ apt-key adv --keyserver <KeyServer> --recv-keys <公钥签名>

$ gpg --export --armor <公钥签名> | sudo apt-key add -
```

