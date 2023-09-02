## tmux使用

.tmux.conf
  - 此配置保证创建的window与分割的窗格的路径都与其父相同   
  - [CentOS路径失效问题](https://unix.stackexchange.com/questions/233929/tmux-2-0-pane-current-path-not-working-on-centos)
    - CentOS 中使用 $PWD 替换 ##{pane_current_path}

```conf
bind-key c new-window -c "##{pane_current_path}"
bind-key % split-window -h -c "##{pane_current_path}"
bind-key '"' split-window -c "##{pane_current_path}"
```

```shell
## 使tmux配置生效
$ tmux source-file .tmux.conf
```

- [tmux教程](https://www.ruanyifeng.com/blog/2019/10/tmux.html)
  - 创建会话 -> 创建窗口 -> 分割窗格
  - shell可以创建多个会话, 一个会话中可以有多个窗口，一个窗口中可以分割出多个窗格  

```shell
## 创建会话
## 直接使用 tmux 也能够创建一个会话
$ tmux new -s <session-name>

## 显示所有会话
$ tmux ls 

## 连接一个会话
$ tmux attach -t <num or name>

## 关闭一个会话
$ tmux kill-session -t <name>
```
以下需要在 tmux 会话中使用

- 会话管理

```
Ctrl+b d：分离当前会话。
Ctrl+b s：列出所有会话。
Ctrl+b $：重命名当前会话。
```

- 窗格管理

```
Ctrl+b %：划分左右两个窗格。
Ctrl+b "：划分上下两个窗格。
Ctrl+b <arrow key>：光标切换到其他窗格。<arrow key>是指向要切换到的窗格的方向键，比如切换到下方窗格，就按方向键↓。
Ctrl+b ;：光标切换到上一个窗格。
Ctrl+b o：光标切换到下一个窗格。
Ctrl+b {：当前窗格与上一个窗格交换位置。
Ctrl+b }：当前窗格与下一个窗格交换位置。
Ctrl+b Ctrl+o：所有窗格向前移动一个位置，第一个窗格变成最后一个窗格。
Ctrl+b Alt+o：所有窗格向后移动一个位置，最后一个窗格变成第一个窗格。
Ctrl+b x：关闭当前窗格。
Ctrl+b !：将当前窗格拆分为一个独立窗口。
Ctrl+b z：当前窗格全屏显示，再使用一次会变回原来大小。
Ctrl+b Ctrl+<arrow key>：按箭头方向调整窗格大小。
Ctrl+b q：显示窗格编号。

Ctrl+b [: 进入查看模式，可以使用 pgup | pgdown进行翻页, 按下 q 退出此模式
```

- 窗口管理

```
Ctrl+b c：创建一个新窗口，状态栏会显示多个窗口的信息。
Ctrl+b p：切换到上一个窗口（按照状态栏上的顺序）。
Ctrl+b n：切换到下一个窗口。
Ctrl+b <number>：切换到指定编号的窗口，其中的<number>是状态栏上的窗口编号。
Ctrl+b w：从列表中选择窗口。
Ctrl+b ,：窗口重命名。
```