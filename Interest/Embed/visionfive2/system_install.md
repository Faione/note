## Upgrade Uboot

通过开机时的串口打印信息可以确认Uboot的编译时间(版本), 版本小于 v2.5.0 时只能通过 `tftpboot` 与 `sf update` 命令来更新，因此需要搭建tftp服务器， 推荐使用 docker 进行部署

```shell
docker run -d --rm -p 0.0.0.0:69:69/udp -v /var/tftpboot:/var/tftpboot  pghalliday/tftp
```

无法访问公共网络时，可以从[debian](https://www.debian.org/distrib/packages)下载软件包来进行相关软件的安装

## debian静态ip配置


## wlan连接

[wpa配置wlan网络](https://www.cnblogs.com/hokori/p/14168584.html)

## SSD Support

从nvme启动需要固件支持， 入发现 pci 无法找到的问题，可能是uboot启动参数问题

[nvme_boot_env](https://forum.rvspace.org/t/nvme-boot-not-working-on-visionfive-2-qspi-with-new-firmware/3293)