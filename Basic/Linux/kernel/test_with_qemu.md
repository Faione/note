## Guidience

get guidience from [kernel doc](https://www.kernel.org/doc)

## environment

llvm, clang, lld

```shell
sudo pacman -S llvm clang lld
```

## Fetch Kernel Source Code 

download from [kernel org](https://www.kernel.org/)

## Config

```shell
make LLVM=1 menuconfig
```

about rust

```
# enable rust support
General Setup
    -> Rust Support

# add rust samples
Kernel hacking
    -> Sample kernel code
        -> Rust samples

```

## Compiling

```shell
# `10` meaning 10 threads
make LLVM=1 -j 10
```

## Emulating

get filesystem image from [dqib](https://people.debian.org/~gio/dqib/)

```
KERNEL=""

qemu-system-x86_64 \
    -machine pc \
    -cpu Nehalem \
    -m 1G \
    -drive file=image.qcow2 \
    -device e1000,netdev=net \
    -netdev user,id=net,hostfwd=tcp::2222-:22 \
    -kernel $KERNEL \
    -initrd initrd \
    -nographic \
    -append "root=LABEL=rootfs console=ttyS0"
```


