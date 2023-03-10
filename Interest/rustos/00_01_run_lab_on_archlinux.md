实验最高支持 qemu 7.1.0， 由于 archlinux 滚动更新，需要依赖 `downgrade` 工具获取旧版本软件

```shell
# 安装 qemu 依赖
sudo downgrade qemu-common
sudo downgrade qemu-system-riscv-firmware

# 安装 qemu
sudo downgrade qemu-system-riscv
```

ch9 需要使用 gui，因此需要安装 gui 相关的程序

```shell
# qemu ui, 使用 gnome 则需要安装 qemu-ui-gtk
sudo downgrade qemu-ui-opengl
sudo downgrade qemu-ui-gtk

# qemu gpu
sudo downgrade qemu-hw-display-virtio-gpu
```