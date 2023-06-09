# Go Callvis


## Installation

Go Callvis is a Go library for visualizing Callvis data[^1]

> origin 尚未更新对于 go 1.20.0 的支持，可参考ISSUE[^2]

[^1] [origin](https://github.com/ofabry/go-callvis)
[^2] [issues_149](https://github.com/ofabry/go-callvis/issues/149)

## Tutorial

`go-callvis` 并不会真正的运行程序，而是对源码中的函数调用进行静态分析，并通过web ui交互窗口的形式进行浏览，通常用于分析代码结构，分析性能应当考虑`go pprof`

```shell
go-callvis <pakages_path>
```

一般用法
```shell
# 只查看目标 package 中的函数调用, std库以及内部的函数不会显示出来
go-callvis -nointer -nostd -focus <pakage_import_name>
```

可选命令

```
Usage of go-callvis:
  -debug
    	Enable verbose log.
  -file string
    	output filename - omit to use server mode
  -cacheDir string
    	Enable caching to avoid unnecessary re-rendering.
  -focus string
    	Focus specific package using name or import path. (default "main")
  -format string
    	output file format [svg | png | jpg | ...] (default "svg")
  -graphviz
    	Use Graphviz's dot program to render images.
  -group string
    	Grouping functions by packages and/or types [pkg, type] (separated by comma) (default "pkg")
  -http string
    	HTTP service address. (default ":7878")
  -ignore string
    	Ignore package paths containing given prefixes (separated by comma)
  -include string
    	Include package paths with given prefixes (separated by comma)
  -limit string
    	Limit package paths to given prefixes (separated by comma)
  -minlen uint
    	Minimum edge length (for wider output). (default 2)
  -nodesep float
    	Minimum space between two adjacent nodes in the same rank (for taller output). (default 0.35)
  -nointer
    	Omit calls to unexported functions.
  -nostd
    	Omit calls to/from packages in standard library.
  -rankdir
        Direction of graph layout [LR | RL | TB | BT] (default "LR")
  -skipbrowser
    	Skip opening browser.
  -tags build tags
    	a list of build tags to consider satisfied during the build. For more information about build tags, see the description of build constraints in the documentation for the go/build package
  -tests
    	Include test code.
  -version
    	Show version and exit.
```