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