

	StatusPending     = 1
	StatusReady       = 2
	StatusPause       = 3
	StatusError       = 4
	StatusTerminating = 5
	StatusTerminated  = 6


创建容器
   - 注册时: pending
   - 启动成功时: ready
   - stop时: pause
   - remove时: 
      - auto remove: terminating -> end
      - custom remove: terminating -> terminated 


key: "remove"
type: "string"
value: "auto"