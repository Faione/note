
# watch工具

周期性执行命令

```shell
# -n 单位为秒
$ watch -n 1 ps
```

```shell
#! /bin/bash

RED='\e[1;31m' # 红
GREEN='\e[1;32m' # 绿
RES='\e[0m' # 清除颜色

commands=(kubectl)
flag=1
isCommandReady() {
    if hash $1 2>/dev/null;then
        echo -e "${1} ${GREEN}Yes${RES}"
    else
        echo -e "${1} ${RED}No${RES}"
        let flag=0
    fi
}

for cmd in  ${commands[@]}
do
isCommandReady $cmd
done

if [ $flag == 0 ]
then
exit 1
fi
```

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

