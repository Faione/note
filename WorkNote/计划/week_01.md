## 计划池

|          |       |
| :------: | :---: |
| complete |  14   |
|  delay   |  16   |
|  cancel  |   0   |
|  total   |  30   |

ebpf
- [delay] {文档} c ebpf 调研
- [delay] {文档} 调研 cilium connections maps 实现
- [delay] {代码} ebpf 抓取当前网络连接数(TCP/UDP)
- [delay] {文档} 对比ebpf与netstats的差异

rcore
- [delay] {代码} 完成基于virtio的block dev，通过相关测例
- [delay] {代码} 确定第一阶段日程，提交相关代码
- [delay] {文档} 整理 rust 相关内容(引用与解引用)
- [delay] {文档} 补充1-2节内容(基于riscv book)

exporter调研
- [x] {文档} go 代码分析工具
- [x] {文档} 调研prometheus handler 调用路径
- [x] {文档} 调研prometheus go client关键抽象
- [x] {文档} 调研prometheus vector withlabel查询方式
- [x] {文档} exporter 基本框架图绘制
- [x] {文档} 整理exporter分享
- [x] {文档} 准备exporter分享

k8s
- [delay] {代码} operator 相关api
- [delay] {文档} operator 教程

信息高铁
- [x] {代码} 优化netstat功能，细粒度采集每个connection
- [x] {代码} 优化ssh auth log功能，增加 accept 与 disconnect 指标
  - 端口存在复用，如果某一个端口同时被passwd和publickey使用，那么对于后登陆的方式，计数为0
- [x] {代码} 优化ssh auth log, 通过日志编号而不是ip端口更精确地统计
- [x] {代码} 完成 ipmi 模块功能，首要是 sel 日志的采集
  - 可以编写vector插件实现
- [x] {代码} 完成dmesg, auth log等日志采集
- [delay] {文档} harbor p2p 分发功能调研

找工作
- [x] {文档} vscode刷题环境
- [delay] {代码} 刷题 35 

其他
- [x] {文档} web ppt写法
- [delay] {代码} os功能挑战赛
- [delay] {文档} runC架构，rust youki等调研
- [delay] {代码} 替换gitbook项目为github pages
- [delay] {文档} OScamp系统功能赛道

## 日程安排

<table>
<tr>
<th></th>
<th>周一</th>
<th>周二</th>
<th>周三</th>
<th>周四</th>
<th>周五</th>
<th>周六</th>
<th>周天</th>
</tr>

<!-- ---------------- 计划 ---------------- -->
<tr align="left">
<th>计划</th>

<!-- 周一 -->
<th>
1. c ebpf 调研 <br>
2. ebpf 抓取当前网络连接数(TCP/UDP) <br>
3. 调研 cilium connections maps 实现 <br>
4. 优化ssh auth log功能，增加 accept 与 disconnect 指标 <br>
5. 对比ebpf与netstats的差异 <br>
6. vscode刷题环境 <br>
</th>

<!-- 周二 -->
<th>
1. 调研prometheus handler 调用路径 <br>
2. exporter 基本框架图绘制 <br>
3. 优化netstat功能，细粒度采集每个connection <br>
4. go 代码分析工具 <br>
5. 优化ssh auth log <br>
</th>

<!-- 周三 -->
<th>
1. 调研prometheus go client关键抽象 <br>
2. exporter 基本框架图绘制 <br>
3. web ppt写法 <br>
4. 完成dmesg, auth log等日志采集 <br>
5. 完成 ipmi 模块功能，首要是 sel 日志的采集 <br>
</th>

<!-- 周四 -->
<th>
调研prometheus vector withlabel查询方式 <br>
整理exporter分享 <br>
准备exporter分享 <br>
</th>

<!-- 周五 -->
<th>
整理exporter分享 <br>
准备exporter分享 <br>
</th>

<!-- 周六 -->
<th>
</th>

<!-- 周天 -->
<th>
</th>
</tr>

<!-- ---------------- 实现 ---------------- -->
<tr align="left">
<th>实现</th>

<!-- 周一 -->
<th>
1. 调研bpftool与libbpf, 编译样例c bpf程序<br>
2. 调研cilium-ebpf，编译样例程序，了解 go build package 与 go generator <br>
3. cilium 并没有使用此框架编写bpf程序，仅涉及数据交互部分的相关内容 <br>
4. 优化ssh auth log功能，增加online指标 <br>
5. netstat依赖的是对于 `/proc/<pid>/tcp` 等文件的读取与解析 <br>
6. 只需要修改endpoint为leetcode cn即可 <br>
</th>

<!-- 周二 -->
<th>
1. 调研handler关键路径，调研Registry中，Gather和Register主要逻辑以及metricId的生成方式<br>
2. 未进行 <br>
3. 优化netstat功能，细粒度采集每个connection <br>
4. 完成 go-callvis 调研，对于含有较多回调的代码，并没有参考价值<br>
5. 每次ssh连接会有一个`编号`, 检索这个编号可以查看一次完整的ssh auth过程(accept, opened, disconnect, closed) <br>
</th>

<!-- 周三 -->
<th>
1. 完成registry register, gather源码分析 <br>
2. exporter 基本框架图绘制 <br>
3. web ppt写法 <br>
4. dmesg, auth log等日志采集使用 vector file 即可 <br>
5. 完成 ipmi 模块功能，首要是 sel 日志的采集，使用 vector exec 即可 <br>
</th>

<!-- 周四 -->
<th>
调研prometheus vector withlabel查询方式 <br>
整理exporter分享 <br>
</th>

<!-- 周五 -->
<th>
准备exporter分享, 完成 marp action<br>
</th>

<!-- 周六 -->
<th>
</th>

<!-- 周天 -->
<th>
</th>

</tr>

<!-- ---------------- 刷题 ---------------- -->
<tr align="left">
<th>刷题</th>

<!-- 周一 -->
<th>
+1<br>
1. 空间换时间，使用map即可
</th>

<!-- 周二 -->
<th>
</th>

<!-- 周三 -->
<th>
+2<br>
有序metric, 右上角满足左小右大，故可从此处开始搜索<br>
字符串替换，遍历确定新字符串大小，然后再遍历进行拷贝，替换<br>
</th>

<!-- 周四 -->
<th>
</th>

<!-- 周五 -->
<th>
</th>

<!-- 周六 -->
<th>
</th>

<!-- 周天 -->
<th>
</th>

</tr>

</table>

本周Coding: 
- +77