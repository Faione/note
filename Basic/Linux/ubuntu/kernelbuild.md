```
apt install -y kernel-package pkg-config libncurses-dev libncurses-dev flex bison libssl-dev libelf-dev ca-certificates dwarves zstd rsync
```

```shell
# source: $PWD/linux
# ouput: $PWD/linux-*.deb
docker run -it --rm -v $PWD:/src ict.acs.edu/infra/kernelbuilder:v0.0.1 /bin/bash
```

set `CONFIG_SYSTEM_TRUSTED_KEYS` `CONFIG_SYSTEM_REVOCATION_KEYS` to empty if `No rule to make target 'xxx', need by 'cert/x509_certificate_list'` occured

```shell
make-kpkg --initrd --append-to-version -20230613 --revision 001 kernel_image kernel_headers -j`nproc`
```

Dockerfile中处理交互式时区

```
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
```