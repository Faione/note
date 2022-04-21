# Viper 

- [强大的配置文件管理库](https://pkg.go.dev/github.com/spf13/viper@v1.10.1)
- [toml配置规范](https://toml.io/cn/v1.0.0)

## 读入配置

- 从 io.reader 读取配置

```go
reader := strings.NewReader(VECTOR_DEFAULT_CONFIG)

viper.SetConfigType("toml")
err := viper.ReadConfig(reader)
```

## 修改配置



## 写回配置