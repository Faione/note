# Custom WSL2 Kernel

custom kernel on Host

```
[wsl2]

kernel=C:\\temp\\myCustomKernel
```

build kernel

```shell
$ make KCONFIG_CONFIG=Microsoft/config-wsl
```

[host_config](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#wslconfig)
[wsl_kernel_source](https://github.com/microsoft/WSL2-Linux-Kernel/)