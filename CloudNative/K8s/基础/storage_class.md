# Storage Class

[intro](https://kubernetes.io/docs/concepts/storage/storage-classes)

对于所能提供的存储服务的一种描述，需要指定一个provisioner, 其能够能够自动的根据 pvc 创建 pv, 并伴随 pvc 的删除而删除对应的 pv, 随后在声明 PVC 时指定一个 storageClassName, 就会将 PVC 的创建事件通知给对应的 provisioner, provisioner 随后创建并维护 pv, 可以说 provisioner 是一种受限的 operator

[nfs ganesha](https://github.com/kubernetes-sigs/nfs-ganesha-server-and-external-provisioner) 是一个简易的 provisioner, 用来创建所需的 pv 及存储空间

如下是一个简单的 nfs provisioner 及 storage class 的配置

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nfs-provisioner
---
kind: Service
apiVersion: v1
metadata:
  name: nfs-provisioner
  labels:
    app: nfs-provisioner
spec:
  ports:
    - name: nfs
      port: 2049
    - name: nfs-udp
      port: 2049
      protocol: UDP
    - name: nlockmgr
      port: 32803
    - name: nlockmgr-udp
      port: 32803
      protocol: UDP
    - name: mountd
      port: 20048
    - name: mountd-udp
      port: 20048
      protocol: UDP
    - name: rquotad
      port: 875
    - name: rquotad-udp
      port: 875
      protocol: UDP
    - name: rpcbind
      port: 111
    - name: rpcbind-udp
      port: 111
      protocol: UDP
    - name: statd
      port: 662
    - name: statd-udp
      port: 662
      protocol: UDP
  selector:
    app: nfs-provisioner
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: nfs-provisioner
spec:
  selector:
    matchLabels:
      app: nfs-provisioner
  replicas: 1
  strategy:
    type: Recreate 
  template:
    metadata:
      labels:
        app: nfs-provisioner
    spec:
      serviceAccount: nfs-provisioner
      containers:
        - name: nfs-provisioner
          image: k8s.gcr.io/sig-storage/nfs-provisioner:v3.0.0
          ports:
            - name: nfs
              containerPort: 2049
            - name: nfs-udp
              containerPort: 2049
              protocol: UDP
            - name: nlockmgr
              containerPort: 32803
            - name: nlockmgr-udp
              containerPort: 32803
              protocol: UDP
            - name: mountd
              containerPort: 20048
            - name: mountd-udp
              containerPort: 20048
              protocol: UDP
            - name: rquotad
              containerPort: 875
            - name: rquotad-udp
              containerPort: 875
              protocol: UDP
            - name: rpcbind
              containerPort: 111
            - name: rpcbind-udp
              containerPort: 111
              protocol: UDP
            - name: statd
              containerPort: 662
            - name: statd-udp
              containerPort: 662
              protocol: UDP
          securityContext:
            capabilities:
              add:
                - DAC_READ_SEARCH
                - SYS_RESOURCE
          args:
            - "-provisioner=gluenet.io/nfs"
          env:
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
            - name: SERVICE_NAME
              value: nfs-provisioner
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          imagePullPolicy: "IfNotPresent"
          volumeMounts:
            - name: export-volume
              mountPath: /export
      volumes:
        - name: export-volume
          hostPath:
            path: /data/nfsp
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nfs-provisioner-runner
rules:
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    verbs: ["get", "list", "watch", "create", "delete"]
  - apiGroups: [""]
    resources: ["persistentvolumeclaims"]
    verbs: ["get", "list", "watch", "update"]
  - apiGroups: ["storage.k8s.io"]
    resources: ["storageclasses"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["create", "update", "patch"]
  - apiGroups: [""]
    resources: ["services", "endpoints"]
    verbs: ["get"]
  - apiGroups: ["extensions"]
    resources: ["podsecuritypolicies"]
    resourceNames: ["nfs-provisioner"]
    verbs: ["use"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: run-nfs-provisioner
subjects:
  - kind: ServiceAccount
    name: nfs-provisioner
     # replace with namespace where provisioner is deployed
    namespace: gluenet-nfsp
roleRef:
  kind: ClusterRole
  name: nfs-provisioner-runner
  apiGroup: rbac.authorization.k8s.io
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-provisioner
rules:
  - apiGroups: [""]
    resources: ["endpoints"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-provisioner
subjects:
  - kind: ServiceAccount
    name: nfs-provisioner
    # replace with namespace where provisioner is deployed
    namespace: gluenet-nfsp
roleRef:
  kind: Role
  name: leader-locking-nfs-provisioner
  apiGroup: rbac.authorization.k8s.io
---
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: standard
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: gluenet.io/nfs
mountOptions:
  - vers=4.1
```