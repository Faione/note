[official](https://kubernetes.io/zh-cn/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
[k8s on centos](https://www.cnblogs.com/cerberus43/p/15881294.html)

```shell
version=1.23.15

sudo yum install kubelet-${version} kubectl-${version} kubeadm-${version}
```

准备镜像

```shell

version="v1.23.15"

orgin_registry="registry.k8s.io"
mirror_registry="registry.aliyuncs.com/google_containers"

for bs_image in kube-apiserver kube-controller-manager kube-scheduler kube-proxy;do \
docker pull ${mirror_registry}/${bs_image}:${version}
docker tag ${mirror_registry}/${bs_image}:${version} ${orgin_registry}/${bs_image}:${version}
docker rmi ${mirror_registry}/${bs_image}:${version};done

for ot_image in "pause:3.6" "etcd:3.5.6-0";do \
docker pull ${mirror_registry}/${ot_image}
docker tag ${mirror_registry}/${ot_image} ${orgin_registry}/${ot_image}
docker rmi ${mirror_registry}/${ot_image};done


docker pull ${mirror_registry}/"coredns:v1.8.6"
docker tag ${mirror_registry}/"coredns:v1.8.6" ${orgin_registry}/coredns/"coredns:v1.8.6"
docker rmi ${mirror_registry}/"coredns:v1.8.6"
```

```shell
version="v1.23.15"
orgin_registry="registry.k8s.io"
mirror_registry="registry.aliyuncs.com/google_containers"

for bs_image in kube-proxy;do \
docker pull ${mirror_registry}/${bs_image}:${version}
docker tag ${mirror_registry}/${bs_image}:${version} ${orgin_registry}/${bs_image}:${version}
docker rmi ${mirror_registry}/${bs_image}:${version};done

for ot_image in "pause:3.6" ;do \
docker pull ${mirror_registry}/${ot_image}
docker tag ${mirror_registry}/${ot_image} ${orgin_registry}/${ot_image}
docker rmi ${mirror_registry}/${ot_image};done

docker pull ${mirror_registry}/"coredns:v1.8.6"
docker tag ${mirror_registry}/"coredns:v1.8.6" ${orgin_registry}/coredns/"coredns:v1.8.6"
docker rmi ${mirror_registry}/"coredns:v1.8.6"
```

```shell
version="v1.23.15"

for image in `kubeadm config images list --kubernetes-version ${version}`; do \
echo ${image/"registry.k8s.io"/"registry.aliyuncs.com/google_containers"};done


```

sudo kubeadm init --kubernetes-version=v1.23.15 \
--pod-network-cidr=10.244.0.0/16 \
--service-cidr=10.96.0.0/12 \
--apiserver-advertise-address=172.16.31.36
