# Vagrantfile

类似于 docker compose, 对虚拟机进行配置

[vagrant_libvirt_config](https://vagrant-libvirt.github.io/vagrant-libvirt/configuration.html)


```yaml
Vagrant.configure("2") do |config|

  config.vm.box = "podman-apline317"

  config.vm.box_check_update = false

  config.vm.provider :libvirt do |v|
    v.cpus = 1
    v.cpuset = 131
    v.memory = 1024
  end

  config.vm.network "public_network", ip: "10.208.129.191", :dev => "br0", :type => "bridge"
  
  config.vm.provision "shell", inline: <<-SHELL
    sudo podman pull --cert-dir /vagrant ict.acs.edu/app/redis:latest
    sudo podman run -d --network host ict.acs.edu/app/redis:latest
    sudo route add default gw 10.208.129.254
    eval `route -n | awk '{ if ($8 ==\"eth0\" && $2 != \"0.0.0.0\") print \"sudo route del default gw \" $2; }'`
  SHELL
end
```

## Basic

配置 `config.vm.box_check_update = false` 来关闭联网版本检测

## Shell

可以在 vagrant 中编写 shell 命令来定义虚拟机的启动行为，这些命令通常只会在虚拟机第一次启动时执行, 通过修改 `run` 字段可以定义执行的时机，通常有 `always`, `once`, `never`

```
config.vm.provision "shell",
    run: "always",
    inline: "route add default gw 192.168.0.1"
```

## Network

通常情况下，虚拟机连接到默认的虚拟网桥 `virbr`，从而与宿主机通信，同时宿主机经由此虚拟网桥来为虚拟机提供 dhcp 以及 dns 服务

这种情况下虚拟机仅能被宿主机访问，因此这种网络模式被称为 `private_network`, 此时如需要将虚拟机暴漏给外界，需要配置 `config.vm.network "forwarded_port", guest: 80, host: 8080` 以进行端口转发

如需将虚拟机完全暴漏到网络中，则需要通过建立连接到实际网络的虚拟网桥，通过这种方式使得虚拟机能够像物理机器一样连接到外部网络中，这种网络模式称为 `public_network`, 通过 `config.vm.network "public_network", ip: "10.208.129.191", :dev => "br0", :type => "bridge"` 配置以指定 public ip 以及实际要绑定到的网桥

使用这种方式创建的虚拟机中会有两张网卡，一张连接到 `private_network`， 另一张连接到 `public_network`, 而由于默认情况下的路由表由第一张网卡生成，此时启动的虚拟机并不能正确的在外部网络中进行网络访问, 需要在启动命令中，修改默认网关[^1]

[^1]: [vagrant_public_router](https://developer.hashicorp.com/vagrant/docs/networking/public_network)

