# Vagrant

Vagrant是对于hypervisor的高度封装，允许使用配置型的语言来声明一个虚拟机，并将其转化为所支持平台的对应命令，来构建和管理虚拟机，vagrant将不同hypervisor的镜像定义为box，并提供了类似于镜像存储的box仓库[vagrant_cloud_box](https://app.vagrantup.com/boxes/)， 允许用户上传或者从仓库中取得所需要的镜像
- virtual box
- vmware
- libvirt

vagrant 本质上是类似与 docker-compose 的配置管理工具，实际虚机管理功能由底层提供

## Provider

### Libvirt

[vagrant_libvirt_source](https://github.com/vagrant-libvirt/vagrant-libvirt)

libvirt 是一种 vagrant 的provider，相关的配置在 [`vagrant_libvirt`](https://vagrant-libvirt.github.io/vagrant-libvirt/) 中, 其本质上是与 libvirt API 交互，并通过底层的 Qemu，KVM 来完成虚拟化

hypervisor的对于虚机镜像的格式各有不同，vagrant仓库中常见的有 virtual box 与 vmware，对于 libvirt 镜像的支持较少，但是可以通过 [`vagrant_mutate`](https://github.com/sciurus/vagrant-mutate) 工具来对镜像格式进行转化

转化后的镜像名称可能与原来的不同，需要在 `~/.vagrant.d/boxes` 中进行修改， 同时转化后的镜像都是本地镜像，在VagrantFile的配置需要关闭在线版本检查

## Package

对当前虚拟机进行修改之后，可使用 `package` [vagrant_ops](https://www.junmajinlong.com/virtual/vagrant/vagrant_box/) 命令将虚拟机提交为一个新的 box

```shell
$ vagrant package --output <file>

$ vagrant box add <box_name> <name/path/url>
```