## k8s自动发现

[k8s config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)

prometheus中的k8s插件，会自动与k8s进行同步，获得node、pod、service、entrypoint等信息，并进行label，这些label能够作用于服务发现
- 需要给prometheus配置cluster权限
- 支持自定义的annotation


```yaml
scrape_configs:
    - job_name: 'gluenets-services'
    metrics_path: /metrics
    params:
        module: [http_2xx]
    kubernetes_sd_configs:
        - role: service
    relabel_configs:
        - source_labels: [__meta_kubernetes_service_annotation_gluenet_io_scrape]
        action: keep
        regex: true
        - source_labels: [__address__, __meta_kubernetes_service_annotation_gluenet_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: ${1}:${2}
        target_label: __address__
        - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
        - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
        - source_labels: [__meta_kubernetes_service_name]
        target_label: service
```