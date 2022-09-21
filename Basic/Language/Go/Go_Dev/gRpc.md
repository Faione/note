# Protobuf通信协议

- [gRpc](https://grpc.io/docs/languages/go/quickstart/)
- [officail tutorial](https://developers.google.com/protocol-buffers/docs/gotutorial)

## 一、简介

- 编写 `.proto` 文件来对将要存储的数据结构进行描述
- protocol buffer 编译器通过`.proto`文件构造类
  - 该类以有效的二进制格式实现协议缓冲区数据的自动编码和解析
  - 生成的类为各个字段提供 getter 和 setter并负责将proto buffer 作为读取和写入的单元

## 二、protobuf 基本语法

- 编写 `.proto` 文件
  - `syntax = "proto3"`: 声明 protobuf 版本
  - `package test`: 用来区别不同的 protobuf 文件
  - `option go_package="/model"`: 最后一个作为go文件包名，与`go_out`拼接为路径

```go
syntax = "proto3"; 

package test; 

option go_package="/model"; 

message User {
    string name = 1;
}
```

- 编译 `.proto` 文件
  - `I`: 搜索 `.proto` 文件的目录
  - `--go_out`: 输出语言及目录
  - `model/test.proto`: 要编译的文件

```shell
$ protoc -I=model --go_out=. model/test.proto
```

## gRpc

gRpc用来快速构建微服务，允许用户在`.proto`文件中定义的请求/响应的数据结构，及使用到这些数据的方法接口，并通过`protoc`编译器，生成`*.pb.go`与`*_grpc.pb.go`代码文件，其中:
- `*.pb.go`包含服务的接口，用户可以基于接口来定义业务逻辑
- `*_grpc.pb.go`包含客户端，用户可以直接通过构造对应的客户端，来请求服务

### 工具准备(go)

[quick start](https://grpc.io/docs/languages/go/quickstart/)


[insall protoc](https://grpc.io/docs/protoc-installation/)

protoc编译器

```shell
$ PB_REL="https://github.com/protocolbuffers/protobuf/releases"
$ curl -LO $PB_REL/download/v3.15.8/protoc-3.15.8-linux-x86_64.zip

$ unzip protoc-3.15.8-linux-x86_64.zip -d $HOME/.local
$ export PATH="$PATH:$HOME/.local/bin"
```

protoc-go插件

```shell
$ go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
$ go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
```


### Hello World

编译`.proto`文件
- `--go_out=.`: 指定生成的`.pb.go`文件目录为当前目录
  - `--go_opt=paths=source_relative`: 如果`.proto`文件在当前目录中可以检索到，则会在其同目录下生成`.pb.go`文件
- `--go-grpc_out=.`: 指定生成的`*_grpc.pb.go`文件目录为当前目录
  - `--go-grpc_opt=paths=source_relative`: 如果`.proto`文件在当前目录中可以检索到，则会在其同目录下生成`*_grpc.pb.go`文件

```
$ protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    helloworld/helloworld.proto
```

### gRpc开发

1. Define a service in a .proto file.
2. Generate server and client code using the protocol buffer compiler.
3. Use the Go gRPC API to write a simple client and server for your service.