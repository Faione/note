## CNI Chaining

CNI链接允许将Cilium与其他CNI插件结合使用。通过Cilium CNI链接，基本网络连接和IP地址管理由非Cilium CN插件管理，但Cilium将eBPF程序附加到非Ciliu插件创建的网络设备，以提供L3/L4网络可见性、策略执行和其他高级功能

[cilium-cni-chaining](https://docs.cilium.io/en/stable/installation/cni-chaining-generic-veth/)


创建 cni chaining 配置，然后在部署 cilium 时，使用 cni chaining
- cilium v1.13.0 存在未知bug, 导致 coredns 不断重启

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cni-configuration
  namespace: kube-system
data:
  cni-config: |-
    {
        "name": "generic-veth",
        "cniVersion": "0.3.1",
        "plugins": [
            {
                "type": "flannel",
                "delegate": {
                    "hairpinMode": true,
                    "isDefaultGateway": true
                }
            },
            {
                "type": "portmap",
                "capabilities": {
                    "portMappings": true
                }
            },
            {
                "type": "cilium-cni"
            }
        ]
    }
```