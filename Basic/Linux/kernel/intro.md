# Linux Kernel

## Source Code

linux kernel stable版本通常为 x.y.z
- x: 大版本号
- y: 小版本号
- x: 修订号
  
其中 `x.y` 为当时的主线版本，可以从[torvalds_linux](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/refs/)按tag下载得到。通常版本发布之后，会有一系列的补丁，可以按需要加上这些补丁
- EOL 表示此分支的最后一个版本
- rc 为非正式版本, 主要用于测试，且每周都会发布一个，rcx 的patch 基于上一个 tag

```shell
# 下载指定版本的 source code
git clone https://kernel.googlesource.com/pub/scm/linux/kernel/git/torvalds/linux.git -b v6.6 --depth 1
```

## Using Patch

patch 通常为一系列的补丁集合，可以从某个tag版本升级到最新的stable版本，具体操作参考[Applying Patches To The Linux Kernel](https://docs.kernel.org/process/applying-patches.html)

```shell
# 在 linux 源码目录下
xzcat ~/Downloads/patch-6.6.4.xz | patch -p1
```