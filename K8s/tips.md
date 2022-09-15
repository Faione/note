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


  # hubble本身cilium隔离，当hubble先于cilium启动时，cilium无法获得其信息导致不能管理，因此需要严格两者的启动顺序，或在cilium启动之后，将未被管理的部分纳入其中

注意`--network-plugin=cni`
  minikube start --network-plugin=cni --cni=false