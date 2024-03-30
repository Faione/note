# Alpine

Alpine 是一个轻量级 Linux 发行版
- 链接 busybox 以提供基础软件功能
- 使用 musl 进一步减少占用

musl 与 glibc 是两套不同的 C 动态链接库, 提供了如 malloc 等关键功能的实现，而由于两者的实现上存在的差异，因此存在兼容性问题，alpine linux提供了几种[解决的思路](https://wiki.alpinelinux.org/wiki/Running_glibc_programs)
- `gcompat`: 提供了一个兼容层，但仅支持 musl 与 glibc 的功能交集
- `chroot` / `container`: 两者思路类似，均通过其他distro的mount ns从而实现glibc的加载