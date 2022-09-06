# 导出kubeconfig

```shell
# --minify=true  只使用当前context，--flatten=true，生成可移动的config(不使用相对路径)
$ kubectl config view --minify=true --flatten=true 
```