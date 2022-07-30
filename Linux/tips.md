
- watch工具
  - 周期性执行命令

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