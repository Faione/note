## 处理 nfs 错误

postgres pod 启动动时，会进行初始化操作，运行 `chmod -R 700 /var/lib/postgresql/data/pgdata || true`, ? 而在 nfs 中，文件的权限由提供者决定，而不能通过挂载 nfs 的形式修改，从而导致操作失败

因此启动 postgres 时，不应该挂载 nfs 目录，[参考](https://ithelp.ithome.com.tw/m/articles/10304306)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv-harbor-db
spec:
  storageClassName: local-harbor
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/harbor/db
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - node37
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: local-pvc-harbor-db
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi 
  storageClassName: local-harbor
```

启动命令, 如仍然存在权限不足的问题，则可以尝试将挂载的相关目录的权限修改为 `777`

```shell
helm -n harbor install --create-namespace \
--set expose.type=nodePort,\
expose.tls.auto.commonName=gluenet.registry.io,\
externalURL=https://gluenet.registry.io:30003,\
persistence.persistentVolumeClaim.database.existingClaim=local-pvc-harbor-db,\
persistence.persistentVolumeClaim.database.subPath=database \
harbor harbor
```
