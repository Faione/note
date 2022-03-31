

- [dynamic-client](https://github.com/kubernetes/client-go/blob/master/examples/dynamic-create-update-delete-deployment/main.go)
- [yaml 文件操作](https://gist.github.com/pytimer/0ad436972a073bb37b8b6b8b474520fc)


## 启停操作

``` shell
# 从 yaml 启动
$ kubectl apply -f

# 从 yaml 删除
$ kubectl delete -f 
```

## 监控操作

**logs监控**

```shell
# 监控指定deployment中的容器
# kubectl logs deployement/[name] -c [containername] 
$ kubectl logs deployment/test-1-core-simservice
```

**metric监控**


## k8s 监控设计

- deployment.yaml 中能够解析 deployment name 与 container name, 进而能够索引单个容器
  - TODO: namespace?

**log监控**

- 通过索引获得容器的logs
  - kubect logs

**metric监控**

- 借助外部工具，prometheus 抓取metric数据，利用索引进行过滤

