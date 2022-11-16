## server

deloy by docker-compose

- 设置 DRONE_USER_CREATE 环境变量以控制用户权限，如为gitee用户 `gitee_rubbish` 赋予 admin权限，解决无法挂载目录的问题

```yaml
version: "3"
services:
  drone:
    image: drone/drone:2
    container_name: drone
    volumes:
      - ./data:/data
    environment:
      - DRONE_GITEE_CLIENT_ID=de7cc4e88b554a04709c1dd526397e876d588c18cdeb0fe09a3ecbd65e92a830
      - DRONE_GITEE_CLIENT_SECRET=a6bc15901e3259ed0aa72f956aec05d25f813f609d636fde83b076a8ebb09244
      - DRONE_RPC_SECRET=36d7fe78a51c82e1ce275cede62a5ff0
      - DRONE_SERVER_HOST=124.222.198.37:10115
      - DRONE_SERVER_PROTO=http
      - DRONE_USER_CREATE=username:gitee_rubbish,admin:true
    ports:
      - 10116:80
    restart: always
```

## runner

```yaml
version: "3"
services:
  drone-runner:
    image: drone/drone-runner-docker:1
    container_name: runner
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DRONE_RPC_PROTO=http
      - DRONE_RPC_HOST=124.222.198.37:10115
      - DRONE_RPC_SECRET=36d7fe78a51c82e1ce275cede62a5ff0
      - DRONE_RUNNER_CAPACITY=2
      - DRONE_RUNNER_NAME=my-first-runner
    ports:
      - 3000:3000
    restart: always
```

## Custom CI

runner会轮询server来获得需要进行的CI(取决于web hook), drone通过项目根目录下的 `.drone.yml` 文件来定义CI过程

以docker CI为例，默认会通过git容器pull最新的代码，并将其挂载到一个共享目录中，之后的所有step中用到的容器，都通过挂载此目录，并修改workdir的方式，在整个流程中共享代码文件

以下配置的目标是 clone 代码 -> docker-compose 构建镜像并运行

```yaml
kind: pipeline
type: docker
name: default

steps:
- name: compose
  image: linuxserver/docker-compose:2.12.2-v2
  volumes:
  - name: docker
    path: /var/run/docker.sock
  commands:
  - docker-compose-entrypoint.sh down --rmi all
  - docker-compose-entrypoint.sh up --build -d

volumes:
- name: docker
  host:
    path: /var/run/docker.sock
```

