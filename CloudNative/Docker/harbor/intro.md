# harbor

- [harbor](#harbor)
  - [install by helm](#install-by-helm)
  - [docker with harbor](#docker-with-harbor)
  - [helm with harbor](#helm-with-harbor)

## install by helm

获取 harbor helm chart

```shell
helm repo add harbor https://helm.goharbor.io

helm fetch harbor/harbor --untar
```

安装 harbor
- `expose.type`: harbor 服务的暴露方式
- `expose.tls.auto.commonName`: CA验证的域名名称，需要与 `externalURL` 中的相同
- `externalURL`: 用来进行登陆重定向，默认拉取的url

```shell
helm -n harbor install --create-namespace \
  --set expose.type=nodePort \
  --set expose.tls.auto.commonName=gluenet.registry.io \
  --set externalURL=https://gluenet.registry.io:30003  \
  harbor harbor
```

## docker with harbor

在harbor处点击 `注册证书` 获取 ca 证书

为 docker 增加仓库 cert，[docker仓库配置参考](https://docs.docker.com/engine/security/certificates/)
- `gluenet.registry.io` 代表域名，`30003` 为仓库入口，如私有搭建，则需要配置host dns

```shell
# 在 /etc/docker/certs.d/ 中增加私有库配置
mkdir gluenet.registry.io:30003

# 拷贝 ca 证书
cp ca.crt gluenet.registry.io:30003/
```

**登入 harbor 仓库**

```
docker login gluenet.registry.io:30003
```

**上传镜像到 harbor 仓库**

```
docker tag <image_name>:<tag> gluenet.registry.io:30003/<image_name>:<tag>

docker push gluenet.registry.io:30003/<image_name>:<tag>
```

## helm with harbor

为主机添加私有库 ca 证书

```shell
# on centos
cd /etc/pki/ca-trust/source/anchors/

cp ca.crt .

# 更新ca
sudo update-ca-trust
```

**上传 helm chart**

```shell
helm package <chart_path>

helm push <chart_pkg>
```

```shell
ver=v2.7.0
repo=goharbor

for image in chartmuseum-photon redis-photon trivy-adapter-photon notary-server-photon notary-signer-photon harbor-registryctl registry-photon nginx-photon harbor-jobservice harbor-core harbor-portal harbor-db; do \
docker save ${repo}/${image}:${ver} | gzip >  ${image}.tar.gz ;done


for image in chartmuseum-photon redis-photon trivy-adapter-photon notary-server-photon notary-signer-photon harbor-registryctl registry-photon nginx-photon harbor-jobservice harbor-core harbor-portal harbor-db; do \
minikube -p harbor cp harbor:/home/docker/${image}.tar.gz  /home/fhl/harborimg/${image}.tar.gz  ;done


for image in chartmuseum-photon redis-photon trivy-adapter-photon notary-server-photon notary-signer-photon harbor-registryctl registry-photon nginx-photon harbor-jobservice harbor-core harbor-portal harbor-db; do \
docker load -i ${image}.tar.gz ;done
```