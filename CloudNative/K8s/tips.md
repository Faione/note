## 导出kubeconfig

```shell
# --minify=true  只使用当前context，--flatten=true，生成可移动的config(不使用相对路径)
$ kubectl config view --minify=true --flatten=true 
```

## 切换集群

在 kubevirt 和 cilium 集群之间切换

```shell
$ kubectl config use-context kubevrit | cilium 
```

## jsonPath

[intro](https://kubernetes.io/docs/reference/kubectl/jsonpath/)

查看pod中的container

```
$ kubectl get pods <podname> -o jsonpath='{.spec.containers[*].name}'
```

## command && args

[commands && args](https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/)

- 如果不为容器提供 `command` 或 `args` 参数，则使用Docker镜像中定义的默认值
- 如果提供 `command` 但没有提供 `args` 参数，则仅使用提供的 `command`, Docker镜像中定义的默认EntryPoint和默认Cmd将被忽略
- 如果仅为容器提供 `args`，则Docker镜像中定义的默认Entrypoint将与您提供的 `args` 一起运行
- 如果提供 `command` 和 `args`，则将忽略Docker镜像中定义的默认Entrypoint和默认Cmd, 您的command与 args一起运行

## 

kubectl edit configMap frpc

kubectl get pod test -o yaml | kubectl apply -f -


kubectl config view --minify=true --flatten=true  > deploy/helm/manager/v0.3/k8sconfig

IMAGE_TAG=test APP=apiserver make remake redeploy-app

[k8s-api](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.25/)