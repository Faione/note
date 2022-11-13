## 搭建 Vscode Server Go语言环境
### 一、Linux安装Go环境
#### (1)使用包管理工具安装
```shell
sudo apt-get install golang

# 查看是否安装成功
go version
go version go1.13.8 linux/amd64
```
- 问题
apt-get 默认安装的go版本较老，不支持新特性

#### (2)二进制包安装
在 [Go中文社区Golang资源](https://studygolang.com/dl), 或Go官网找到对应平台的Go二进制文件

```shell
# 下载二进制文件
GOBIN=go1.19.linux-amd64.tar.gz
wget https://studygolang.com/dl/golang/$GOBIN .
# 解压二进制文件
# 解压至 /usr/local
sudo tar -C /usr/local -xzf $GOBIN

# 增加环境变量
export PATH=$PATH:/usr/local/go/bin

# 测试
$ go version
go version go1.17.1 linux/amd64
```

### 二、Go编译器的使用
#### (1) 示例程序
```go
// file name: hello.go
package main

import "fmt"

func main(){
    fmt.Println("Hello World")
}
```
#### (2) 编译
```shell
go build hello.go
# 产生二进制文件 hello
```
#### (3) 执行
``` shell
./hello 
>> hello world

# 编译执行
go run hello.go
>> hello world
# 编译执行不会产生 hello 文件
```

### 三、Vscode Go 环境
#### (1) 安装vscode插件
找到并安装即可
#### (2) 安装Go支持库
- 国内代理镜像配置
``` shell
$ go env -w GOPROXY=https://goproxy.cn,direct
```

- 插件版本错误
匹配Go版本即可

- 运行调试提示 "go.mod not found..."
go环境配置错误
```shell
# 补充配置
$ go env -w GO111MODULE=auto
```


- 下载所有 go 插件, 美化代码
   - [参考](https://blog.csdn.net/qq_41891425/article/details/110675093)


