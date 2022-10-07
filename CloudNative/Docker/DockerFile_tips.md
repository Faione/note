## DockerFile

[](https://docs.docker.com/engine/reference/builder/)

docker build 的参数如 `.` 表明从当前目录进行构建

### 多阶段镜像构建

[多阶段镜像构建](https://docs.docker.com/build/building/multi-stage/)

build的过程会分阶段进行, 通过 `as` 对不同阶段进行命名, 然后使用 `--from=build` 便可以从 `build` 阶段的容器中, 获得文件
- 过程中会产生虚悬镜像(REPOSITORY 与 TAG均为None的镜像), 使用 `docker image prune` 进行删除

```Dockerfile
FROM golang:latest as build
 
ENV GO111MODULE=on
ENV GOPROXY=https://goproxy.cn,direct

ADD . src/

RUN cd src && make build

FROM docker.io/alpine as app

COPY --from=build /go/src/bin/watcher /app/watcher
ENTRYPOINT ["/app/watcher"]
```

### Docker build

[overview](https://docs.docker.com/build/)
[docker build](https://docs.docker.com/engine/reference/commandline/build/)


[](https://iximiuz.com/en/posts/you-need-containers-to-build-an-image/)