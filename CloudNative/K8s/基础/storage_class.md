# Storage Class

[intro](https://kubernetes.io/docs/concepts/storage/storage-classes)

对于所能提供的存储服务的一种描述，能够自动的根据 pvc 创建 pv, 并伴随 pvc 的删除而删除对应的 pv

[nfs ganesha](https://github.com/kubernetes-sigs/nfs-ganesha-server-and-external-provisioner) 是一个简易的 provisioner, 用来创建所需的 pv 及存储空间