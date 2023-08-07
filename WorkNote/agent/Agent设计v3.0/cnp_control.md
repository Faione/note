## 需求

pod 网络访问控制
1. 仅允许被同namespace下访问
2. 允许被其他namespace访问
3. 允许被 proxy 应用访问以进行代理

## 网络策略

定义一组网络策略，并通过 group label 选择一组目标进行实施，多个策略可以附加在同一个组上，彼此取并

默认组策略

|  level  |   Ingress    | Egress |                描述                 |    cnp     |
| :-----: | :----------: | :----: | :---------------------------------: | :--------: |
| normal  |    无限制    | 无限制 |              普通服务               |    None    |
| protect | 同一命名空间 | 无限制 |       仅能在同namespace中访问       | ProtectCnp |
|  proxy  |  proxy应用   | 无限制 | 允许被 `proxy` 应用访问，以进行代理 |  ProxyCnp  |


### 默认策略

label protect

```yaml
# protect_cnp
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: gluenet-cnp-protect
specs:
  - endpointSelector:
      matchLabels:
        gluenet.netgroup.protect: in
    ingress:
    - fromEndpoints:
        - {}
```

label proxy

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: gluenet-cnp-proxy
specs:
  - endpointSelector:
      matchLabels:
        gluenet.netgroup.proxy: in
    ingress:
    - fromEndpoints:
        - matchLabels:
            k8s:io.kubernetes.pod.namespace: {envoy_namespace}
```


