## Stringer
>类似与java中的toString()方法，绝大多数类都实现了此接口（内置接口）  
>实现 String() string 方法即可  
>Print时自动调用
```go
type Stringer interface {
    String() string
}
```
## Error
>同样是内建接口，可以通过实现 Error() string 方法  
>某种错误（如算数错误）可通过实现该接口，设定出发该错误时应当返回的字符串说明信息  
>Print时自动调用（实现接口，可转型为error）
```go
type error interface {
    Error() string
}
```
## Reader
>内建接口，接收byte数组作为缓冲，向其中填入值，并返回填入的大小及err
```go
func (T) Read(b []byte) (n int, err error)
```
