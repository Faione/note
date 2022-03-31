# Helm

- [helm官方文档](https://helm.sh/zh/docs/)
- [helm go client](https://manuelmazzuola.dev/2021/03/28/deploy-helm-chart-go#the-helm-go-sdk)
- [helm go client mittwald](https://pkg.go.dev/github.com/mittwald/go-helm-client#NewClientFromKubeConf)

## What is Helm

- helm是k8s的包管理工具
  - helm管理的包即是 chart，本质上是一个模板文件的组合，用来对要部署的k8s资源进行描述，以及一个用于评估的值文件

> Helm installs charts into Kubernetes, creating a new release for each installation. And to find new charts, you can search Helm chart repositories

## 基本概念

- Chart 代表着 Helm 包
  - 包含在 Kubernetes 集群内部运行应用程序，工具或服务所需的所有资源定义
  - 可以看作是 Homebrew formula，Apt dpkg，或 Yum RPM 在Kubernetes 中的等价物

- Repository（仓库） 是用来存放和共享 charts 的地方
  - 像 Perl 的 CPAN 档案库网络或是 Fedora 的 软件包仓库，只不过它是供 Kubernetes 包所使用的

- Release 是运行在 Kubernetes 集群中的 chart 的实例
  - 一个 chart 通常可以在同一个集群中安装多次。每一次安装都会创建一个新的 release
  - 以 MySQL chart为例，如果你想在你的集群中运行两个数据库，你可以安装该chart两次， 每一个数据库都会拥有它自己的 release 和 release name

- Helm 安装 charts 到 Kubernetes 集群中，每次安装都会创建一个新的 release
  - 可以在 Helm 的 chart repositories 中寻找新的 chart

## Helm功能列表

|command|describe|
|-|-|
|completion | generate autocompletions script for the specified shell|
|create     | create a new chart with the given name|
|dependency | manage a chart's dependencies|
|env        | helm client environment information|
|get        | download extended information of a named release|
|help       | Help about any command|
|history    | fetch release history|
|install    | install a chart|
|lint       | examine a chart for possible issues|
|list       | list releases|
|package    | package a chart directory into a chart archive|
|plugin     | install, list, or uninstall Helm plugins|
|pull       | download a chart from a repository and (optionally) unpack it in local directory|
|repo       | add, list, remove, update, and index chart repositories|
|rollback   | roll back a release to a previous revision|
|search     | search for a keyword in charts|
|show       | show information of a chart|
|status     | display the status of the named release|
|template   | locally render templates|
|test       | run tests for a release|
|uninstall  | uninstall a release|
|upgrade    | upgrade a release|
|verify     | verify that a chart at the given path has been signed and is valid|
|version    | print the client version information|

## Helm构建轻量级应用

### （1） 创建模板

```shell
# 在当前目录下，创建名为 test 的chart模板
$ helm create test
```

- helm create 会创建一个文件夹，其中包含一系列模板文件, 存放在templates中

```shell
# 目录结构
test
.
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml

```

### (2) 自定义模板

```shell
# 默认模板可以删除
$ "rm -rf templates/*" 
```
- 生成基础的deployment.yaml与service.yaml
  - 使用 kubectl命令生成，配置"dry-run=client"使得命令不会真正执行

```shell
# 生成deployment.yaml
$ kubectl create deployment test-1-core-simservice --image=39.101.140.145:5000/cpu-ctrl-core-1  --dry-run=client -o yaml > deployment.yaml

# 生成service.yaml
$ kubectl expose deployment test-1-core-simservice --port=80 --target-port=10111 --dry-run=client -o yaml >service.yaml
```

### (3) helm Chart部署

- 此处CHART即 create 所创建的文件夹
  - 运行时的Chart即Release
  - Helm 使用 NAME 来索引 Release，真正部署的deployement等名称与配置文件相关

```shell
# helm install [NAME] [CHART] [flags]
$ helm install test-cpu-service testHelm
```
### (4) helm Release卸载

- uninstall、del、delete功能类似

``` shell
# helm uninstall RELEASE_NAME [...] [flags]
$ helm del test-cpu-service
```

