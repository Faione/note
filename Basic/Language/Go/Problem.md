
- go 结构体组合指针访问内部变量问题
  - 原因，`var xx` 只初始化右侧对应的类型，如给出结构体，则初始化结构体，但给出结构体指针时，就只会初始化一个指针(无符号数)，并不会对结构体内部的数据进行初始化，因此会有空指针异常
  - 如想创建结构体指针并能使用，则可以使用`new`关键字

```go

type Inside struct {
	fo string
}
type Outside struct {
	bar string
	Inside
}

// Success
func TestStruct(t *testing.T) {
	var test Outside

	n := &test
	n.bar = "hello"
	n.fo = "nihao"

	fmt.Println(n)
}

func TestStruct(t *testing.T) {
	test := new(Outside)

	test.bar = "hello"
	test.fo = "nihao"

	fmt.Println(test)
}

// Falied
func TestStruct(t *testing.T) {
	var test *Outside

	test.bar = "hello"
	test.fo = "nihao"

	fmt.Println(test)
}
```