[cni-migiration](https://www.jetstack.io/blog/cni-migration/)


```yaml
operator:
    unmanagedPodWatcher:
    restart: false # Migration: Don't restart unmigrated pods
cni:
    customConf: true # Migration: Don't install a CNI configuration file
    uninstall: false # Migration: Don't remove CNI configuration on shutdown
ipam:
    mode: "cluster-pool"
    operator:
    clusterPoolIPv4PodCIDRList: ["10.245.0.0/16"] # Migration: Ensure this is distinct and unused
policyEnforcementMode: "never" # Migration: Disable policy enforcement
bpf:
    hostLegacyRouting: true # Migration: Allow for routing between Cilium and the existing overlay
```
