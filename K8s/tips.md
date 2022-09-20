# 导出kubeconfig

```shell
# --minify=true  只使用当前context，--flatten=true，生成可移动的config(不使用相对路径)
$ kubectl config view --minify=true --flatten=true 
```

# 切换集群

在 kubevirt 和 cilium 集群之间切换

```shell
$ kubectl config use-context kubevrit | cilium 
```

# jsonPath

[intro](https://kubernetes.io/docs/reference/kubectl/jsonpath/)

查看pod中的container



```
$ kubectl get pods <podname> -o jsonpath='{.spec.containers[*].name}'
```