# dig

依赖注入: 通过注册的构建函数，依靠反射获取所需参数，分析依赖情况，自动完成依赖构建，并保存构造的对象
- 通过泛型函数，取出构造的对象

```go
var container = dig.New()

func Provide(constructor interface{}, opts ...dig.ProvideOption) {
	if err := container.Provide(constructor, opts...); err != nil {
		logrus.Fatal("provide dependency err : ", err)
	}
}

func Invoke(function interface{}, opts ...dig.InvokeOption) {
	// todo: 错误判断
	if err := container.Invoke(function, opts...); err != nil {
		logrus.Fatal("invoke dependency err : ", err)
	}
}

func Produce[T any]() T {
	var d T
	Invoke(func(driver T) {
		d = driver
	})
	return d
}

```