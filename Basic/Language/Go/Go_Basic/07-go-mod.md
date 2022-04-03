# go mod

## 说明

go 的依赖管理工具

## go调用本地库

```shell
# 构建mod模块
go mod init <projectName>
```

此时，就能够通过 projectName 索引内部的package了

```go
import {
    <anyName> "projectName/internal/<package>"
}
```

然后，就能够在代码中使用 \<anyName\> 来对 \<package\> 中的所有对外方法进行调用了
