## run

``` shell
go run [build flags] [-exec xprog] package [arguments...]
```

go run 会在其他目录(tmp)编译 package, 并设置GO_ROOT为当前目录(方便如读取当前目录文件), 然后执行编译好的二进制文件bin

如设置了 `-exec xprog`, 则go run会执行 `xprog bin args` 而不是 `bin args`， 如设置 `-exec sudo`， 则会使用root权限执行bin


## generator

`go genenrate` 在 go v1.4 中引入，其工作方式是扫描go源码中注明为`general commands` 的特殊注释

`go generate` 并非 `go build` 的组成部分，其中也没有依赖分析，同时必须在go build 之前运行

[^1] [generating_code](https://go.dev/blog/generate)