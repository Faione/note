# Unsafe

unsafe 库提供了在 Go 中操作指针的方法，这些方法需要开发者来保证其安全性

访问私有变量

```go
// pkg foo

type Foo struct {
    // 私有变量
    private string
}

func NewFoo() *Foo{}

// pkg bar

{
    foo := NewFoo()

    // 编译器不允许访问 foo.private, 因此以下代码无法通过编译
    // fmt.Println(foo.private)

    // 构造 foo 的 unsafe 指针
    pFoo := unsafe.Pointer(foo)

    type tmp struct {
        public string
    }

    // 将 pFoo 转化为 tmp 指针
    rawFoo := (*tmp) (pFoo)

    // tmp.public 即是 foo.private
    fmt.Println(tmp.public)
}

```