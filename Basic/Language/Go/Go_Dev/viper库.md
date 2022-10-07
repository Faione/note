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


## 环境变量

使用 `AutomaticEnv` 时， viper会读取所有的环境变量，但并不将他们绑定到任何key上，而是在使用 `Get` 方法时，将传入的key匹配到某个环境变量上
- `SetEnvPrefix` 让viper仅读取指定前缀的环境变量，viper会将传入值转为大写，并增加 "_" 来构造前缀
- `SetEnvKeyReplacer` 会对传入 `GET` 中的key的特殊字符串进行替换，以匹配环境变量
- 大小写敏感

```go
vp := viper.New()
vp.SetEnvPrefix("watcher")
vp.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
vp.AutomaticEnv()
```

## viper 优先级

[](https://zhuanlan.zhihu.com/p/144323180)

1. 显式调用Set设置值
2. 命令行参数（flag）
3. 环境变量
4. 配置文件
5. key/value 存储
6. 默认值