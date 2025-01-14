# Git 基础操作
- [Git 基础操作](#git-基础操作)
  - [一、分支管理](#一分支管理)
    - [(1) 简介](#1-简介)
    - [(2) 命令](#2-命令)
  - [二、版本管理](#二版本管理)
    - [(1) 说明](#1-说明)
    - [(2) 命令](#2-命令-1)
  - [三、远程管理](#三远程管理)
    - [(1) 简介](#1-简介-1)
    - [(2) 命令](#2-命令-2)
  - [四、常用开发](#四常用开发)
    - [(1) bug fix/refactor 分支](#1-bug-fixrefactor-分支)
    - [(2) 设置远程仓库](#2-设置远程仓库)
    - [(3) 合并commit](#3-合并commit)
    - [(4) working on mutiple branch](#4-working-on-mutiple-branch)
    - [submodule](#submodule)
    - [(4) git submodule](#4-git-submodule)
    - [(5) git tags](#5-git-tags)


## 一、分支管理
### (1) 简介
项目工程创建好后，存在一个默认的master分支，该分支用以存储当前完备的项目工程，而各子功能的开发都在branch之中进行，开发完成之后通过merge/rebase，合并到当前的master之中

分支非常轻量，仅指向某次提交记录，并不会额外的增加其他存储空间

### (2) 命令
1. 创建分支

```shell
$ git branch <分支名称>
```
2. 切换分支

```shell
$ git checkout <分支名称>
```

- 创建分支并切换

```shell
$ git checkout -b <分支名称>
```

3. 合并分支
- merge

>merge两个分支会在当前分支产生一个特殊的提交记录，其会有两个父节点  
>这意味着当前分支包含了两个分支全部的提交记录  
>但是，从提交记录来看，其仍然是"分叉"的，即是并行开发的

```shell
$ git merge <分支名称>
```

- rebase

>rebase两个分支会将当前分支的自己的部分(区别于公共的部分)直接链接到选择的分支之后  
>使得该条分支能包含两个分支全部的提交记录  
>并且，从提交记录来看，该条分支是线性的，即没有 "分叉"

## 二、版本管理
### (1) 说明
git head 默认指向当前分支的最新的提交，而要进行版本管理，首先就需要切换head

### (2) 命令
1. 查看commit log

```shell
$ git log
```

2. 切换head

>切换分支与切换head使用的命令相同，区别在于参数，前者使用的 branch, 后者使用的是 commit tag  
>同时，前者head默认指向分支的最后一次提交，后者则指向目标commit记录  
>显然，两种操作后者更普遍，也就是说，checkout实际上就是在切换head
>因而，切换head时，并不需要切换branch，同时，branch本身，就是指向分支的最新head

```shell
$ git checkout <commit tag>
```

1. 相对引用

>相对引用能够在不知道tag, 但清楚与最新提交之间的相对位置时，进行head的切换

- 回退一个

>该操作会让head指向 <分支名称> 分支最新提交的上一个commit
>多次执行其结果是相同的(理解上一句话)
>当然，对于具体分支tag而言，相对引用仍然是有效的

```shell
$ git checkout <分支名称>^

$ git checkout <commit tag>^
```
- 回退多个

```shell
$ git checkout <分支名称>^^

$ git checkout <分支名称>~2
```

4. 回退分支

>该操作将分支回退至指定的位置
>注意，branch

```shell
$ git branch -f <分支名称> <commit tag>
```

5. 撤销变更
- reset[^1]

>撤销本地变更
>将当前分支回退至 commit tag处，并使得改tag之后的commit无效
>对远程分支无效(没有push?)

```shell
$ git reset <commit tag>

# 回退至上一次commit, 并保留变更的文件
$ git reset --soft HEAD^
```

- revert

> 无效 commit tag 之后的所有commit，并执行相反的操作(复原)
> 将上述相反的操作作为一次新的commit，让当前分支指向该commit
> 即将

```shell
$ git revert <commit tag>
```

## 三、远程管理
### (1) 简介

远程仓库是本地仓库的备份

### (2) 命令

1. 克隆远程仓库

```shell
# 文件夹名未给出时，默认为远程分支的文件名
$ git clone <url> -b <分支名称> <文件夹名> 
```

2. 切换远程分支

远程分支也可以通过 checkout 命令进行切换，但是切换之后，就进入了分离Head状态, 即当前的commit不会对远程分支产生影响
>分离Head状态: Head指针指向某次commit，而非某分支(默认是该分支的最新提交)

```shell
$ git checkout origin/master
```

3. 更新本地远程分支
- Fetch
Fetch进行两项工作
   - 从远程仓库下载本地仓库缺失的提交记录
   - 更新远程分支指针(origin/master 及远程仓库上的其他分支)  

Fetch仅对.git文件进行了更新(下载、指针更新)，即将本地仓库中所有的远程分支记录进行了同步，但不会影响本地仓库，故本地分支/文件不会发生变化
   - Fetch之后，再进行分支合并，就可以将远程分支中的变化，整合到本地分支上

```shell
$ git fetch

# 同步这些变化, 可以使用以下方法
$ git cherry-pick orgin/master
$ git rebase orgin/master
$ git merge orgin/master
```

- Pull
pull操作提供了更简介的本地-远程分支合并操作
   - 执行fetch更新本地仓库的远程分支
   - 执行merge，合并关联的远程分支(同名分支)

```shell
$ git pull origin <远程分支名>
```

4. 删除远程分支

```shell
$ git push <remote> -d <remote_branch>
```

## 四、常用开发

- 查看当前所有分支

```
$ git branch -a
```

### (1) bug fix/refactor 分支

- 构造工作分支[^2][^3]

```
$ git checkout -b refactor
```

- 进行相关工作

```shell
$ git add .
$ git commit -m"finish refactor"
```

- Rebase 分支

```shell
# 在工作分支上
# 同步主分支最新代码 (有需要则进行，否则不必)
$ git pull --rebase
$ git rebase master

# 在目标分支上
# git rebase refactor
$ git merge --no-ff refactor

# 删除工作分支
$ git branch -d refactor
```

### (2) 设置远程仓库

- 全局设置

```shell
git config --global user.name "Fhl"
git config --global user.email "1287481902@qq.com"
```

- 创建git仓库

```shell
mkdir test
cd test
git init 
touch README.md
git add README.md
git commit -m "first commit"
git remote add origin https://gitee.com/gitee_rubbish/test.git
git push -u origin "master"
```

- 已有仓库

```shell
cd existing_git_repo
git remote add origin https://gitee.com/gitee_rubbish/test.git
git push -u origin "master"

# 如仓库进行了初始化而非空仓库时
git pull --rebase origin master
git push -u origin "master"

git remote rm origin
```

### (3) 合并commit

- [合并commit](https://blog.csdn.net/Spade_/article/details/108698036)

```shell
# 查看分支
$ git log

# 定位要合并的分支
$ git rebase -i <要合并commit中最后一个commit的父节点>

# 设置合并策略
# commit从早到晚依次排列
# pick 第一个，之后的使用fixup(丢弃提交信息)或squash(合并提交信息)
 
$ git push --force 
```

修改commit信息

```
$ git commit --amend -m "new message"
```

删除远程分支

```shell
$ git push origin --delete <branch_name>
```

### (4) working on mutiple branch

切换分支通常使用`git checkout <branch>`，但切换前后的文件都限于当前目录，这意味着同一时间只能存在一个分支，而要想维护不同版本的代码，就必须来回切换

`git worktree`[^4]能够将分支检出到不同文件夹，这使得切换文件夹就能够切花代码版本，也意味着能够同时维护多个分支的代码或对比不同分支代码的行为等

```shell
git worktree add <target_path> <branch>
```
- 默认情况下检出当前`HEAD`分支
- 指定branch时，如果其已经关联到了一个worktree(需注意默认有一个worktree), 则add会被拒绝执行，可通过`-f`来强制执行，不指定branch时，会使用path(截)作为分支名称
- 与`checkout`类似，可使用`-b`来创建分支并关联worktree, 当分支已经存在时，可使用`-B`强制执行

相关命令[^5]

> lock: If a worktree is on a portable device or network share which is not always mounted, lock it to prevent its administrative files from being pruned automatically. This also prevents it from being moved or deleted

```shell
# 添加worktree
git worktree add [-f] [--checkout -b <new-branch>] <path> <commit-ish>
# 列出所有worktree
git worktree list [--porcelain]
# worktree上锁
git worktree lock [--reason <string> <worktree>]
# worktree解锁
git worktree unlock <worktree>
# 移动worktree到其他目录
git worktree move <worktree> <new-path>
# 清除那些检出目录已经被删除的worktree
git worktree prune -n --expire <expire>
# 删除worktree, 同时删除检出目录
git worktree remove -f <worktree>
```

### submodule

```shell
git clone --recursive <gitpath>
```

[^1]: [撤销_reset](https://blog.csdn.net/mhlghy/article/details/84786497)
[^2]: [git_merge_解析](https://www.jianshu.com/p/58a166f24c81)
[^3]: [git_分支模型](https://www.jianshu.com/p/b357df6794e3)
[^4]: [git_worktree](https://jasonkayzk.github.io/2020/05/03/Git-Worktree%E7%9A%84%E4%BD%BF%E7%94%A8/)
[^5]: [git_worktree_official](https://git-scm.com/docs/git-worktree)

### (4) git submodule

```shell
# 添加 submodule
git submodule add <url> <path>

# 删除 submodule
git rm --cached <path>
```

[^6]: [git_submodule](https://iphysresearch.github.io/blog/post/programing/git/git_submodule/)
[^7]: [git_submodule_official](https://git-scm.com/docs/git-submodule)

### (5) git tags

标签是比分支更为固定和不可更改的指针，它们指向的是代码库中的某个特殊提交，并通过注释信息描述该提交的含义。

需要注意的是，与分支不同，标签不能被移动或更改。如果要修改一个旧的标签，必须删除它并创建一个新的标签

创建tag

```shell
$ git tag <tagname>

# use `-m` with `-a`
$ git tag -a <tagname> -m <msg>
```

查看所有的tag

```shell
$ git tag
```

切换到某个tag

```shell
$ git checkout <tagname>
```

在特定tag上创建分支

```shell
$ git checkout -b <branchname> <tagname>
```

删除tag

```shell
$ git tag -d <tagname>
```

推送tag到远程仓库

```shell
$ git push origin <tagname>
```


[^8]: [git_tag](https://git-scm.com/docs/git-tag)