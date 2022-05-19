
- go 默认项目在 $GOPATH/src 中
  - 如果项目不在 $GOPATH/src 中，则无法直接引用 三方库
- 项目目录中使用 `go mod init <name>` 
  - 构造 `go.mod` 与 `go.sum` 文件，之后再使用 `go get` 则能够成功导入三方库