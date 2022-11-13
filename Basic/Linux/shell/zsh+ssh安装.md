## ZSH Shell工具
### (1) Linux安装ZSH
```shell
$ sudo apt-get install zsh 
```
### (2) 安装Oh-My-ZSH美化工具

```shell
# 脚本会自动设置当前用户的shell为zsh
$ sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```


```shell
# 使用 gitee 进行加速
$ git clone https://gitee.com/mirrors/oh-my-zsh oh-my-zsh

$ cd tools

$ ./install.sh
```

### (3) zsh 永久环境变量

```shell
# 找到 bash 路径
$ type -a zsh

# 设置为默认shell
$ chsh -s /bin/zsh

# 增加永久环境变量
$ vi ~/.zshrc
```

### (4) 其他用户配置ZSH

当前用户为 test
root用户已经配置好zsh

```shell
# 拷贝文件
$ sudo cp -r /root/.oh-my-zsh ~/

$ sudo cp /root/.zshrc ~/

# 赋予权限
$ sudo chown -R ~/.oh-my-zsh test

$ sudo chown -R ~/.zshrc test
```

其他
```shell
# 配置文件错误
export ZSH=$HOME/.oh-my-zsh
```

### (5) 修改主题

- [zsh配置](https://www.jianshu.com/p/497b4af1334d)

查看主题

```shell
$ ls ~/.oh-my-zsh/themes
```

修改主题

```shell
$ vi ~/.zshrc 

-> ZSH_THEME="ys" 
```

### (6) more than zsh


```shell
# 可使用 gitee 地址替代 github即可
$ git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

$ git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

```shell
plugins=(
      git 
      zsh-autosuggestions # 代码建议
      zsh-vi-mode # vi mod，可以在命令行中使用vi命令
      zsh-syntax-highlighting # 语法高亮
      colored-man-pages # man 高亮
)
```

autojump， 使用 `j dir_perfix` 跳转到之前访问过的目录中
zsh-autosuggestions, 使用方向键 `->` 补全推荐的代码



