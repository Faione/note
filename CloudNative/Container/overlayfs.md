[容器底层原理](https://zhuanlan.zhihu.com/p/102171749)

## Overlayfs


OverlayFS通常表现为混合的，因为出现在其中的兑现通常并不属于此文件系统。在多数情况下很难区分访问的文件对象从unionfs还是从原生文件系统中进行[^2]

尽管目录文件会反馈来自 overlayfs的 `st_dev`， 非目录文件则会反馈来自提供该文件的底层文件系统的 `st_dev`。相同的，`st_ino` 仅在与 `st_dev` 组合时才是唯一的，并且非目录文件的这两个字段会在运行过程不断变化。不关心这两个字段的程序则不会受到影响

统一底层fs的文件会反馈底层fs的 `st_ino` 和 overlayfs 的 `st_dev`, 这使得很容易就能够区分 overlay fs 中的文件与底层fs中文件

### Upper And Lower
一个overlayfs通常由 upper fs 和 lower fs 组成，而如果个文件系统中都存在同名文件，则只有 upper fs 中的文件可见

### Directories

如果同名的是目录而不是文件，则会构造一个 merge directories，将两个目录文件中的索引对象组合起来
- workdir需要是同在upper fs中的空文件夹，用于存储操作overlayfs过程中产生的临时文件和中间状态(inode, dentry)
- 可以将 `$PWD/overlay` 理解为实际的overlayfs, 通过mount挂载到了 `$PWD/merged` 中
- 如果不给出 `upperdir` 与 `workdir`， 则overlayfs将是只读的

```shell
# `-t overlay` 指定了挂载的类型
# `-o`：指定了 `lowerdir`， `upperdir` 与 `workdir`
# `$PWD/overlay $PWD/merged`: 指定了源目录与目标目录
sudo mount -t overlay  -olowerdir=$PWD/lower,upperdir=$PWD/upper,workdir=$PWD/work $PWD/overlay $PWD/merged
```

**whiteouts and opaque directories**

overlayfs中使用 `whiteouts` 与 `opaque directories` 来支持在不影响 lower fs 的前提下的rm rmdir的使用

whiteout: 被创建为设备编号 0/0 的字符设备。当在一个upper合并目录中出现 whiteout 时, 所有与其名称相同的 lower level 中的对象将被忽视， whiteout 本身也会被隐藏起来

opaque directories: 通过设置 xaar 中的 "trusted.overlay.opaque" 属性为 "y", 如果 upper fs 中存在一个 opaque directories， 则所有与之同名的 lower level directory 将会被忽视


### Non-directories

非目录对象(文件、符号链接、设备专用文件等)根据用途在upper或lower中呈现。当对lowerfs中的文件进行写访问时, 该文件首先被复制到upper fs。注意，使用硬链接的文件同样需要copy_up, 而符号链接则不需要

而当只是写权限打开文件，但不进行修改时，copy-up本身可能就并非必要

copy_up 过程首先会确保目录在upper fs中存在，然后以相同的metadata创建目标对象。如果此对象是文件，则数据会从lower拷贝到upper中，最后所有的扩展属性都会被一并拷贝

一旦copy_up 完成， overlayfs就可以之间访问upper fs中新建的文件


### Permission model


### Multiple lower layers

通过 `:` 可指定多个lower fs, 多个 lower layer也存在覆盖层级，最左边是最上层

```shell
sudo mount -t overlay  -olowerdir=$PWD/lower:$PWD/other,upperdir=$PWD/upper,workdir=$PWD/work $PWD/overlay $PWD/merged
```

### Metadata only copy up

如果使能了 `metadata only copy up`。则当执行 chown/chmod 等修改metadata的操作时， ovelayfs 只会复制文件的 metadata。稍后打开文件进行写入操作时，将会复制完整文件

通过内核配置选项`CONFIG_OVERLAY_FS_METACOPY` 或者挂载选项 `metacopy=on/off` 实现

[^1]: [overlayFs](https://dev.to/napicella/how-are-docker-images-built-a-look-into-the-linux-overlay-file-systems-and-the-oci-specification-175n)

[^2]: [overlayFs_kernel_doc](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html?highlight=overlayfs)