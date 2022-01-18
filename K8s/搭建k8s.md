# k8s 搭建

- [kubectl](https://kubernetes.io/zh/docs/tasks/tools/install-kubectl-linux/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)

## 问题汇总

1. 谷歌源无法访问
   - 替换aliyun源

```
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
```


