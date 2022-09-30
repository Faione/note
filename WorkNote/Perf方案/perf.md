

perf stat -e r5301c7 -e r5302c7 -e r5304c7 -e r5308c7 -e r5310c7 -e r5320c7 -e r5340c7 -e r5380c7 -e r5300c4 -e r5381d0 -e r5382d0 -e r5300c0 -o total_stream.txt -I 1000   ./stream

docker run -it --rm --privileged -v ~/workplace/c/stream/out:/app/bin docker-perf:latest stat -e r5301c7 -e r5302c7 -e r5304c7 -e r5308c7 -e r5310c7 -e r5320c7 -e r5340c7 -e r5380c7 -e r5300c4 -e r5381d0 -e r5382d0 -e r5300c0 ./app/bin


- docker-perf镜像
  - 提供perf cli工具，以及二进制程序执行环境
  - 默认Entrypoint为`perf`
  - 运行另一个守护进程，监听perf结果，读取最新数据，并运行算力度量算法(python脚本)

1. 应用载入: 用户应用通过volume或打包在镜像中的方式，放置在`/app`目录下的`bin`中
2. 应用执行: 镜像的默认Entrypoint为`perf`, 容器启动命令指定event，默认启动应用程序`/app/bin`, 默认将结果写入`/data/raw`中
3. 数据收集: 容器中运行另一个守护进程，监听`/data/raw`文件的变化，读取最新数据
4. 数据处理: 守护进程将数据交给/调用算力度量脚本，获得处理过后的数据
5. 数据发送: 守护进程通过rpc client 将数据发送到总线的指定topic中 | 守护进程将数据发送到prometheus临时数据存储库中，prometheus再将数据发送到总控中

目标: 后台启动一个应用，前台能够访问某个接口获得应用执行整个周期的perf数据

## 数据存储


perf -> output file -> file-watcher -> pushGateWay -> prometheus

```
docker run -d -p 27182:9091 prom/pushgateway
```