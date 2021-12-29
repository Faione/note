## Go Web Service
### 一、简单搭建
库: net/http  

#### (1) 构造一个API
```go
func main(){
    http.HandleFunc("/", sayHello) // api "/", 对应的service为 sayHello
    
    err := http.ListenAndServe(":9990", nil) // 开启服务并监听端口9990
    if err != nil {
       log.Fatal("Listen And Serve:", err)
    
}
```
#### (2) 构造一个Service
```go
func sayHello(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()  // 解析参数，默认是不会解析的
	fmt.Println(r.Form)  // 这些信息是输出到服务器端的打印信息
	fmt.Println("path", r.URL.Path)
	fmt.Println("scheme", r.URL.Scheme)
	fmt.Println(r.Form["url_long"]) // 读取用户传入request params中的 "url_long" 项

	for k, v := range r.Form { // 遍历所有的request params
		fmt.Println("key:", k)
		fmt.Println("val:", strings.Join(v, ""))
	}
	fmt.Fprintf(w, "Hello !") // 利用reponse回写响应给用户   
}
```
#### (3) 测试
```shell
$ curl "http://localhost:9990"
> Hello !

backend: 
> path /
> scheme 
> []

$ curl "http://localhost:9990/url_long=1&url_long=2"
> Hello !

backend: 
> path /
> scheme 
> [1, 2]
> key: url_long
> val: 12
```

### 二、Go网络请求原理
#### (1) 基础概念（后端）
1. Request: 用户(或其他程序)所定义、传来的请求信息，包括请求的类型(Post、Get)、Cookie、url等信息
2. Response: 服务器所产生，对应请求的反馈值
3. Connection: 每一次请求所产生的链接
4. Handler: 处理请求与生成返回信息的处理逻辑（一个或一组函数）

#### (2) http包处理流程
后端处理http请求的流程： 
   1. 创建Listen Socket, 监听指定端口， 等待客户端请求到来
   2. Listen Socket接收到客户端的请求，得到Client Socket，并通过Client Socket与客户通信
   3. 处理客户端的请求
      - 从Client Socket读取HTTP请求的协议头，如果是Post方法，则还要读取客户端提交的数据
      - 交给相应的Handler处理请求
      - Handler处理完毕后，通过Client Socket写回给客户端

对于任何语言，运行Web服务必须解决三个问题:
   1. 监听端口（能接收到数据）
   2. 接收客户端请求（能将数据解析为一个Request）
   3. 分配Handler（能通过Request信息找到对应的Handler）

#### (3) net库的实现原理
```go
// 启动服务的代码
rr := http.ListenAndServe(":9990", nil) // 开启服务并监听端口9990

// 调用的具体方法
func ListenAndServe(addr string, handler Handler) error {
	server := &Server{Addr: addr, Handler: handler} // 创建了一个Server对象
	return server.ListenAndServe() // 调用了该对象的ListenAndServe方法
}

// Server的ListenAndServe方法
func (srv *Server) ListenAndServe() error {
	if srv.shuttingDown() {
		return ErrServerClosed
	}
	addr := srv.Addr
	if addr == "" {
		addr = ":http" 
	}
	ln, err := net.Listen("tcp", addr) // 使用底层tcp搭建了一个服务
	if err != nil {
		return err
	}
	return srv.Serve(ln)
}

// Serve方法
func (c *conn) serve(ctx context.Context) {
    ...
	ctx, cancelCtx := context.WithCancel(ctx)
	c.cancelCtx = cancelCtx
	defer cancelCtx()

	c.r = &connReader{conn: c}
	c.bufr = newBufioReader(c.r)
	c.bufw = newBufioWriterSize(checkConnErrorWriter{c}, 4<<10)

	for {
		w, err := c.readRequest(ctx) // 解析请求内容
        ...

		// HTTP cannot have multiple simultaneous active requests.[*]
		// Until the server replies to this request, it can't read another,
		// so we might as well run the handler in this goroutine.
		// [*] Not strictly true: HTTP pipelining. We could let them all process
		// in parallel even if their responses need to be serialized.
		// But we're not going to implement HTTP pipelining because it
		// was never deployed in the wild and the answer is HTTP/2.
		serverHandler{c.server}.ServeHTTP(w, w.req)  // 获取响应的handler进行请求的处理
		w.cancelCtx()
        ...

	}
}

// ServerHTTP-请求的处理
func (sh serverHandler) ServeHTTP(rw ResponseWriter, req *Request) {
	handler := sh.srv.Handler
	if handler == nil {
		handler = DefaultServeMux  // 匹配路由规则，http.HandleFunc("/", sayhelloName) 注册了路由规则，此处则是匹配"/"，找到函数 sayhelloName
	}
	if req.RequestURI == "*" && req.Method == "OPTIONS" {
		handler = globalOptionsHandler{}
	}
	handler.ServeHTTP(rw, req) // 内部就是调用上述函数sayhelloName的过程, 并在最后, 利用参数req, 即Client Socket, 将结果回写
}

```
#### (4) 完整请求流程
![完整请求流程](/Go/Go_Project/image/3.3.illustrator.png)

