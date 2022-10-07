## Service Monitor

[阿里云](https://help.aliyun.com/document_detail/260895.html)
[prometheus官方](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#servicemonitor)


配置 prometheus 监控的对象

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  labels:
    k8s-app: cprofile-exporter
  name: cprofile-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels: 
      gluenet.io/scrape: "true"
  endpoints:
  - interval: 30s 
    targetPort: 9090 
    scheme: http
  jobLabel: cprofile-exporter
```