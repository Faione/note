# Profiling

在 go test 中使用 `-test.cpuprofile cpu.out` flag 可以生成一个名为 `cpu.out` 的profiling文件，配合默认生成的 `<pkg>.test` 文件可以在 `pprof` [^1] 工具中对代码性能进行详细的分析

```shell
$ go tool pprof -http=”:” <pkg>.test cpu.out
```

[^1]: [go_pprof_doc](https://github.com/google/pprof/blob/main/doc/README.md)