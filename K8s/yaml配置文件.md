# Yaml 配置文件

- [yaml变量引用](https://blog.csdn.net/weichi7549/article/details/112240408)
## 特殊符号

- `|` 保留文本每行尾部的换行符，而 `>` 则会将所有的换行符视为空格
  - 当 value 为多行文本时

```
include_newlines: |
            exactly as you see
            will appear these three
            lines of poetry

fold_newlines: >
            this is really a
            single line of text
            despite appearances
```

- `|+` 在保留文本每行尾部的换行符的同时，还保留结尾行的换行符
- `|-` 在保留文本每行尾部的换行符的同时，去除结尾行的换行符


```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agent-config
  namespace: gluenet-test1
data:
  agent_config.toml: |
    [host]
    [host.tags]

    [agent]
    area = "210018"
    role = "other"
    platform = "kubernetes"

    [driver]
    [driver.rpc]
    rpc_config = "nats://39.101.140.145:4222"
    [driver.helm]
    kube_path = "/kube/config"
    repo_name = "gluerepo"
    repo_url = "http://39.101.140.145:30028"
    [driver.k8s]
    kube_path = "/kube/config"

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: gluenet-agent-deployment
  namespace: gluenet-test1
spec:
  selector:
    matchLabels:
      pod: gluenet-agent-pod
  replica: 1
  template:
    metadata:
      name: gluenet-agent
      namespace: gluenet-test1
      labels:
        pod: gluenet-agent-pod
    spec:
      nodeName: worker1.okd.example.com
      containers:
        - name: gluenet-agent
          image: gluenet/agent:0.5
          imagePullPolicy: Always
          env:
            - name: HOST_NAME
              value: other_cluster
            - name: GLUENET_CONFIG_ROOT
              value: /kube/k8s
          command:
            - "/app/agent"
            - "--agent.config.path=/etc/agent/agent_config.toml"
            - "--without.components"
          volumeMounts:
            - mountPath: /etc/agent/
              name: agentconfig
            - mountPath: /kube/
              name: kubeconfig
      volumes:
        - name: agentconfig
          configMap:
            name: agent-config
            items:             
            - key: agent_config.toml             
              path: agent_config.toml
        - name: kubeconfig
          persistentVolumeClaim:
            claimName: config
```


``` yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: prometheus-config
  namespace: gluenet-test1
data:
  prometheus.yml: |
    global:
      scrape_interval:     5s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
      evaluation_interval: 5s # Evaluate rules every 15 seconds. The default is every 1 minute.
    rule_files:
    - "/prometheus/rules/*.yml"
    scrape_configs:
    remote_write:
    - url: "http://gluenet-transfer-svc:10099/v2/apis/agent/metric/write"
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: prometheus-rules
  namespace: gluenet-test1
data:
  rules.yml: |
    groups:
    - name: user1
      rules:
      - alert: cpu_usage_too_hight
        expr: |
          sum(metrics{label="tcp_open_total"}) by (container) > 100
        labels:
          labels: "test"
        annotations:
          summary: "服务 {{ $labels.app_guid }} 下线了"
          description: "{{ $labels.app_guid }} of job {{ $labels.container }} has been down for more than 1 minutes."
      - alert: cpu_usage_too_low
        expr: |
          sum(metrics{label="tcp_open_total"}) by (container) > 100
        labels:
          labels: "test"
        annotations:
          summary: "服务 {{ $labels.app_guid }} 下线了"
          description: "{{ $labels.app_guid }} of job {{ $labels.container }} has been down for more than 1 minutes."
---
apiVersion: v1
kind: Pod
metadata:
  name: glue-stream-prom
  namespace: gluenet-test1
  labels:
    app: glue-stream-prom
spec:
  nodeName: worker1.okd.example.com
  containers:
    - name: prometheus
      image: "prom/prometheus:latest"
      args:
        - --web.enable-remote-write-receiver
        - --web.enable-lifecycle
        - --config.file=/prometheus/config/prometheus.yml
        - --storage.tsdb.path=/prometheus/data/prom
      ports:
        - containerPort: 9090
          name: prometheus
      volumeMounts:
        - mountPath: /prometheus/config/prometheus.yml
          name: prometheus-config
          subPath: prometheus.yml
        - mountPath: /prometheus/rules
          name: prometheus-rules
          subPath: rules.yml
        - mountPath: /prometheus/data/
          name: kubeconfig
  volumes:
    - configMap:
        name: prometheus-config
      name: prometheus-config
    - configMap:
        name: prometheus-rules
      name: prometheus-rules
    - name: kubeconfig
      persistentVolumeClaim:
        claimName: config
---
kind: Service
apiVersion: v1
metadata:
  name: glue-stream-prom-service
  namespace: gluenet-test1
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 10000
      targetPort: 9090
  selector:
    app: glue-stream-prom
---
apiVersion: v1
kind: Pod
metadata:
  name: gluenet-transfer
  labels:
    app.kubernetes.io/component: gluenet-transfer
    app.kubernetes.io/name: gluenet-transfer
    app.kubernetes.io/part-of: kube-prometheus
    app: gluenet-transfer
  namespace: gluenet-test1
spec:
  containers:
    - name: glue-transfer
      image: gluenet/transfer:0.1
      imagePullPolicy: IfNotPresent
      ports:
        - containerPort: 10099
      env:
        - name: RPC_CONFIG
          value: "nats://39.101.140.145:4222"
        - name: PUSH_TOPIC
          value: "guid.manager:rpc.apis.data.metrics.push"
---
apiVersion: v1
kind: Service
metadata:
  name: gluenet-transfer-svc
  namespace: gluenet-test1
spec:
  type: ClusterIP
  ports:
  - name: gluenet-transfer
    protocol: TCP
    port: 10099
    targetPort: 10099
  selector:
    app: gluenet-transfer
---
kind: Service
apiVersion: v1
metadata:
  name: glue-stream-prom-frontend
  namespace: gluenet-test1
spec:
  type: NodePort
  ports:
    - name: http
      port: 55555
      targetPort: 9090
  selector:
    app: glue-stream-prom
```


```
    remoteWrite:
    - url: "http://glue-stream-prom-service.gluenet-test1:10000/api/v1/write"
```

``` yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: prometheus-config
  namespace: gluenet-test1
data:
  prometheus.yml: |
    global:
      scrape_interval:     5s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
      evaluation_interval: 5s # Evaluate rules every 15 seconds. The default is every 1 minute.
    rule_files:
    - "/prometheus/rules/*.yml"
    scrape_configs:
    remote_write:
    - url: "http://gluenet-transfer-svc:10099/v2/apis/agent/metric/write"
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: prometheus-rules
  namespace: gluenet-test1
data:
  rules.yml: |
    groups:
      - name: prometheus
        rules:
          - alert: PrometheusBadConfig
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has failed to
                reload its configuration.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusbadconfig
              summary: Failed Prometheus configuration reload.
            expr: |
              # Without max_over_time, failed scrapes could create false negatives, see
              # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details.
              max_over_time(prometheus_config_last_reload_successful{job="prometheus-k8s",namespace="monitoring"}[5m]) == 0
            for: 10m
            labels:
              severity: critical
          - alert: PrometheusNotificationQueueRunningFull
            annotations:
              description: Alert notification queue of Prometheus {{$labels.namespace}}/{{$labels.pod}}
                is running full.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusnotificationqueuerunningfull
              summary: Prometheus alert notification queue predicted to run full in less
                than 30m.
            expr: |
              # Without min_over_time, failed scrapes could create false negatives, see
              # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details.
              (
                predict_linear(prometheus_notifications_queue_length{job="prometheus-k8s",namespace="monitoring"}[5m], 60 * 30)
              >
                min_over_time(prometheus_notifications_queue_capacity{job="prometheus-k8s",namespace="monitoring"}[5m])
              )
            for: 15m
            labels:
              severity: warning
          - alert: PrometheusErrorSendingAlertsToSomeAlertmanagers
            annotations:
              description: '{{ printf "%.1f" $value }}% errors while sending alerts from
            Prometheus {{$labels.namespace}}/{{$labels.pod}} to Alertmanager {{$labels.alertmanager}}.'
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuserrorsendingalertstosomealertmanagers
              summary: Prometheus has encountered more than 1% errors sending alerts to
                a specific Alertmanager.
            expr: |
              (
                rate(prometheus_notifications_errors_total{job="prometheus-k8s",namespace="monitoring"}[5m])
              /
                rate(prometheus_notifications_sent_total{job="prometheus-k8s",namespace="monitoring"}[5m])
              )
              * 100
              > 1
            for: 15m
            labels:
              severity: warning
          - alert: PrometheusNotConnectedToAlertmanagers
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} is not connected
                to any Alertmanagers.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusnotconnectedtoalertmanagers
              summary: Prometheus is not connected to any Alertmanagers.
            expr: |
              # Without max_over_time, failed scrapes could create false negatives, see
              # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details.
              max_over_time(prometheus_notifications_alertmanagers_discovered{job="prometheus-k8s",namespace="monitoring"}[5m]) < 1
            for: 10m
            labels:
              severity: warning
          - alert: PrometheusTSDBReloadsFailing
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has detected
                {{$value | humanize}} reload failures over the last 3h.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustsdbreloadsfailing
              summary: Prometheus has issues reloading blocks from disk.
            expr: |
              increase(prometheus_tsdb_reloads_failures_total{job="prometheus-k8s",namespace="monitoring"}[3h]) > 0
            for: 4h
            labels:
              severity: warning
          - alert: PrometheusTSDBCompactionsFailing
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has detected
                {{$value | humanize}} compaction failures over the last 3h.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustsdbcompactionsfailing
              summary: Prometheus has issues compacting blocks.
            expr: |
              increase(prometheus_tsdb_compactions_failed_total{job="prometheus-k8s",namespace="monitoring"}[3h]) > 0
            for: 4h
            labels:
              severity: warning
          - alert: PrometheusNotIngestingSamples
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} is not ingesting
                samples.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusnotingestingsamples
              summary: Prometheus is not ingesting samples.
            expr: |
              (
                rate(prometheus_tsdb_head_samples_appended_total{job="prometheus-k8s",namespace="monitoring"}[5m]) <= 0
              and
                (
                  sum without(scrape_job) (prometheus_target_metadata_cache_entries{job="prometheus-k8s",namespace="monitoring"}) > 0
                or
                  sum without(rule_group) (prometheus_rule_group_rules{job="prometheus-k8s",namespace="monitoring"}) > 0
                )
              )
            for: 10m
            labels:
              severity: warning
          - alert: PrometheusDuplicateTimestamps
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} is dropping
                {{ printf "%.4g" $value  }} samples/s with different values but duplicated
                timestamp.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusduplicatetimestamps
              summary: Prometheus is dropping samples with duplicate timestamps.
            expr: |
              rate(prometheus_target_scrapes_sample_duplicate_timestamp_total{job="prometheus-k8s",namespace="monitoring"}[5m]) > 0
            for: 10m
            labels:
              severity: warning
          - alert: PrometheusOutOfOrderTimestamps
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} is dropping
                {{ printf "%.4g" $value  }} samples/s with timestamps arriving out of order.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusoutofordertimestamps
              summary: Prometheus drops samples with out-of-order timestamps.
            expr: |
              rate(prometheus_target_scrapes_sample_out_of_order_total{job="prometheus-k8s",namespace="monitoring"}[5m]) > 0
            for: 10m
            labels:
              severity: warning
          - alert: PrometheusRemoteStorageFailures
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} failed to send
                {{ printf "%.1f" $value }}% of the samples to {{ $labels.remote_name}}:{{
                $labels.url }}
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusremotestoragefailures
              summary: Prometheus fails to send samples to remote impl.
            expr: |
              (
                (rate(prometheus_remote_storage_failed_samples_total{job="prometheus-k8s",namespace="monitoring"}[5m]) or rate(prometheus_remote_storage_samples_failed_total{job="prometheus-k8s",namespace="monitoring"}[5m]))
              /
                (
                  (rate(prometheus_remote_storage_failed_samples_total{job="prometheus-k8s",namespace="monitoring"}[5m]) or rate(prometheus_remote_storage_samples_failed_total{job="prometheus-k8s",namespace="monitoring"}[5m]))
                +
                  (rate(prometheus_remote_storage_succeeded_samples_total{job="prometheus-k8s",namespace="monitoring"}[5m]) or rate(prometheus_remote_storage_samples_total{job="prometheus-k8s",namespace="monitoring"}[5m]))
                )
              )
              * 100
              > 1
            for: 15m
            labels:
              severity: critical
          - alert: PrometheusRemoteWriteBehind
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} remote write
                is {{ printf "%.1f" $value }}s behind for {{ $labels.remote_name}}:{{ $labels.url
                }}.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusremotewritebehind
              summary: Prometheus remote write is behind.
            expr: |
              # Without max_over_time, failed scrapes could create false negatives, see
              # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details.
              (
                max_over_time(prometheus_remote_storage_highest_timestamp_in_seconds{job="prometheus-k8s",namespace="monitoring"}[5m])
              - ignoring(remote_name, url) group_right
                max_over_time(prometheus_remote_storage_queue_highest_sent_timestamp_seconds{job="prometheus-k8s",namespace="monitoring"}[5m])
              )
              > 120
            for: 15m
            labels:
              severity: critical
          - alert: PrometheusRemoteWriteDesiredShards
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} remote write
                desired shards calculation wants to run {{ $value }} shards for queue {{
                $labels.remote_name}}:{{ $labels.url }}, which is more than the max of {{
                printf `prometheus_remote_storage_shards_max{instance="%s",job="prometheus-k8s",namespace="monitoring"}`
                $labels.instance | query | first | value }}.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusremotewritedesiredshards
              summary: Prometheus remote write desired shards calculation wants to run more
                than configured max shards.
            expr: |
              # Without max_over_time, failed scrapes could create false negatives, see
              # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details.
              (
                max_over_time(prometheus_remote_storage_shards_desired{job="prometheus-k8s",namespace="monitoring"}[5m])
              >
                max_over_time(prometheus_remote_storage_shards_max{job="prometheus-k8s",namespace="monitoring"}[5m])
              )
            for: 15m
            labels:
              severity: warning
          - alert: PrometheusRuleFailures
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has failed to
                evaluate {{ printf "%.0f" $value }} rules in the last 5m.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusrulefailures
              summary: Prometheus is failing rule evaluations.
            expr: |
              increase(prometheus_rule_evaluation_failures_total{job="prometheus-k8s",namespace="monitoring"}[5m]) > 0
            for: 15m
            labels:
              severity: critical
          - alert: PrometheusMissingRuleEvaluations
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has missed {{
                printf "%.0f" $value }} rule group evaluations in the last 5m.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusmissingruleevaluations
              summary: Prometheus is missing rule evaluations due to slow rule group evaluation.
            expr: |
              increase(prometheus_rule_group_iterations_missed_total{job="prometheus-k8s",namespace="monitoring"}[5m]) > 0
            for: 15m
            labels:
              severity: warning
          - alert: PrometheusTargetLimitHit
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has dropped
                {{ printf "%.0f" $value }} targets because the number of targets exceeded
                the configured target_limit.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustargetlimithit
              summary: Prometheus has dropped targets because some scrape configs have exceeded
                the targets limit.
            expr: |
              increase(prometheus_target_scrape_pool_exceeded_target_limit_total{job="prometheus-k8s",namespace="monitoring"}[5m]) > 0
            for: 15m
            labels:
              severity: warning
          - alert: PrometheusLabelLimitHit
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has dropped
                {{ printf "%.0f" $value }} targets because some samples exceeded the configured
                label_limit, label_name_length_limit or label_value_length_limit.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuslabellimithit
              summary: Prometheus has dropped targets because some scrape configs have exceeded
                the labels limit.
            expr: |
              increase(prometheus_target_scrape_pool_exceeded_label_limits_total{job="prometheus-k8s",namespace="monitoring"}[5m]) > 0
            for: 15m
            labels:
              severity: warning
          - alert: PrometheusScrapeBodySizeLimitHit
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has failed {{
                printf "%.0f" $value }} scrapes in the last 5m because some targets exceeded
                the configured body_size_limit.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusscrapebodysizelimithit
              summary: Prometheus has dropped some targets that exceeded body size limit.
            expr: |
              increase(prometheus_target_scrapes_exceeded_body_size_limit_total{job="prometheus-k8s",namespace="monitoring"}[5m]) > 0
            for: 15m
            labels:
              severity: warning
          - alert: PrometheusScrapeSampleLimitHit
            annotations:
              description: Prometheus {{$labels.namespace}}/{{$labels.pod}} has failed {{
                printf "%.0f" $value }} scrapes in the last 5m because some targets exceeded
                the configured sample_limit.
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusscrapesamplelimithit
              summary: Prometheus has failed scrapes that have exceeded the configured sample
                limit.
            expr: |
              increase(prometheus_target_scrapes_exceeded_sample_limit_total{job="prometheus-k8s",namespace="monitoring"}[5m]) > 0
            for: 15m
            labels:
              severity: warning
          - alert: PrometheusTargetSyncFailure
            annotations:
              description: '{{ printf "%.0f" $value }} targets in Prometheus {{$labels.namespace}}/{{$labels.pod}}
            have failed to sync because invalid configuration was supplied.'
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustargetsyncfailure
              summary: Prometheus has failed to sync targets.
            expr: |
              increase(prometheus_target_sync_failed_total{job="prometheus-k8s",namespace="monitoring"}[30m]) > 0
            for: 5m
            labels:
              severity: critical
          - alert: PrometheusErrorSendingAlertsToAnyAlertmanager
            annotations:
              description: '{{ printf "%.1f" $value }}% minimum errors while sending alerts
            from Prometheus {{$labels.namespace}}/{{$labels.pod}} to any Alertmanager.'
              runbook_url: https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuserrorsendingalertstoanyalertmanager
              summary: Prometheus encounters more than 3% errors sending alerts to any Alertmanager.
            expr: |
              min without (alertmanager) (
                rate(prometheus_notifications_errors_total{job="prometheus-k8s",namespace="monitoring",alertmanager!~``}[5m])
              /
                rate(prometheus_notifications_sent_total{job="prometheus-k8s",namespace="monitoring",alertmanager!~``}[5m])
              )
              * 100
              > 3
            for: 15m
            labels:
              severity: critical
      # 自定义rule
      # k8s平台下的指标 ，可监控机，容器的cpu memory disk network
      - name: userdefine
        rules:
      # machine cluster-总和 ，前端的判断标志：当host_name: "*" 为总和
        # 1. machine-cpu总和,单位：%
          - expr: |
              sum( clamp_max(clamp_min(1 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[1m]))),0),1) * on (instance) label_replace(machine_cpu_cores,"instance","$1","node","(.+)")) * 100 / sum(machine_cpu_cores)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              host_name: "*"
              label: "cluster_cpu_usage"
            record: "metrics"
        # 2. machine-memory总和,单位：%
          - expr: |
              100 - sum(node_memory_MemFree_bytes+node_memory_Cached_bytes+node_memory_Buffers_bytes)/sum(node_memory_MemTotal_bytes)*100
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              host_name: "*"
              label: "cluster_memory_usage"
            record: "metrics"
        # 3. machine-disk总和,单位：%
      # machine-总核心和总内存
          - expr: |
              sum by(host_name)(label_replace(machine_cpu_cores, "host_name", "$1", "node", "(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_cpu_cores"
            record: "metrics"
          - expr: |
              sum by(host_name)(label_replace(machine_cpu_physical_cores, "host_name", "$1", "node", "(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_cpu_physical_cores"
            record: "metrics"
          - expr: |
              sum by(host_name)(label_replace(machine_memory_bytes, "host_name", "$1", "node", "(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_memory_bytes"
            record: "metrics"
      # machine-单个
        # 一、cpu相关指标
          # 1.单个主机的cpu利用率 = 100 - ((所有空闲状态CPU使用时间总和 )/(所有状态CPU时间总和))*100  单位：%
          - expr: |
              clamp_min(sum(100 - avg by (host_name)(label_replace(irate(node_cpu_seconds_total{mode="idle"}[15s]),"host_name","$1","instance","(.+)")) * 100)without(instance),0)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_cpu_usage"
            record: "metrics"
          # 2.cpu处于用户时间的使用率
          - expr: |
              sum by(host_name)((label_replace(irate(node_cpu_seconds_total{mode="user"}[15s]),"host_name","$1","instance","(.+)")) * 100)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_cpu_user_usage"
            record: "metrics"
          # 3.cpu处于系统时间的使用率
          - expr: |
              sum by(host_name)((label_replace(irate(node_cpu_seconds_total{mode="system"}[15s]),"host_name","$1","instance","(.+)")) * 100)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_cpu_system_usage"
            record: "metrics"
        # 二、memory相关指标
          # 1.memory利用率 单位：%
          - expr: |
              100 - (sum by(host_name)(label_replace(((node_memory_MemFree_bytes+node_memory_Cached_bytes+node_memory_Buffers_bytes)/node_memory_MemTotal_bytes),"host_name","$1","instance","(.+)")) * 100)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_memory_usage"
            record: "metrics"
          # 2.memory使用量（已经用了多少）单位：byte
          - expr: |
              sum by(host_name)(label_replace(node_memory_MemTotal_bytes-node_memory_MemAvailable_bytes,"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_memory_used"
            record: "metrics"
          # 3.memory剩余量 单位：byte
          - expr: |
              sum by(host_name)(label_replace(node_memory_MemAvailable_bytes,"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_memory_avilable"
            record: "metrics"
        # 三、disk相关指标
          - expr: |
              100 - (sum by(host_name) (label_replace((node_filesystem_free_bytes{mountpoint="/"}/node_filesystem_size_bytes{mountpoint="/"} * 100),"host_name","$1","instance","(.+)")))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_disk_space_usage"
            record: "metrics"
          - expr: |
              sum by(host_name)(label_replace((irate(node_disk_io_time_seconds_total[1m])*100),"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_disk_activity_time"
            record: "metrics"
          - expr: |
              sum by (host_name) (label_replace(irate(node_disk_read_bytes_total[1m]),"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_disk_read_rate"
            record: "metrics"
          - expr: |
              sum by (host_name) (label_replace(irate(node_disk_written_bytes_total[1m]),"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_disk_written_rate"
            record: "metrics"
          - expr: |
              sum by (host_name) (label_replace(irate(node_disk_reads_completed_total[1m]),"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_disk_reads_iops"
            record: "metrics"
          - expr: |
              sum by (host_name) (label_replace(irate(node_disk_writes_completed_total[1m]),"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_disk_writes_iops"
            record: "metrics"
        # 四、network相关指标
          - expr: |
              sum by(agent_guid,host_name)(label_replace((irate(node_network_receive_bytes_total[1m])*8/1024),"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_network_receive_kbps"
            record: "metrics"
          - expr: |
              sum by(agent_guid,host_name)(label_replace((irate(node_network_transmit_bytes_total[1m])*8/1024),"host_name","$1","instance","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "node_network_transmit_kbps"
            record: "metrics"
      # apllication 总和，把每个application对应的容器加和（还未添加）
        # 一 .apllication 总和 cpu
          - expr: |
              sum by(application_guid) (label_replace((irate(container_cpu_system_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m])+irate(container_cpu_user_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m]))*100,"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              container: "*"
              label: "application_cpu_usage"
            record: "metrics"
          #保留 不作为接口使用
          - expr: |
              sum by(application_guid) (label_replace((container_cpu_usage_seconds_total{container!~"POD|linkerd-proxy",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              container: "*"
              label: "application_cpu_used_seconds"
            record: "metrics"
          - expr: |
              sum by(application_guid) (label_replace((container_memory_working_set_bytes{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              container: "*"
              label: "application_memory_used_bytes_total"
            record: "metrics"
      # container-单个
        # 一 、container单个-cpu相关指标
          - expr: |
              sum by(pod,container,application_guid)(label_replace((irate(container_cpu_system_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m])+irate(container_cpu_user_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m]))*100,"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_cpu_usage"
            record: "metrics"
          - expr: |
              sum by(pod,container,application_guid)(label_replace(irate(container_cpu_system_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m])*100,"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_cpu_system_usage"
            record: "metrics"
          - expr: |
              (sum by(pod,container,application_guid)(label_replace(irate(container_cpu_user_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m]),"application_guid","$1","namespace","(.+)")))*100
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_cpu_user_usage"
            record: "metrics"
          # 保留但是不用做指标
          - expr: |
              sum by(pod,container,application_guid)(label_replace((container_cpu_system_seconds_total+container_cpu_user_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_cpu_used_seconds"
            record: "metrics"
          - expr: |
              sum by(pod,container,application_guid)(label_replace((container_cpu_system_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_cpu_system_used_seconds"
            record: "metrics"
          - expr: |
              sum by(pod,container,application_guid)(label_replace((container_cpu_user_seconds_total{container!~"POD|linkerd-proxy|gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_cpu_user_used_seconds"
            record: "metrics"
        # 二 、container单个-memory相关指标
          # 1. 容器内存使用量 单位：byte （函数选择上有些问题）
          - expr: |
              sum by(pod,container,application_guid) (label_replace(container_memory_working_set_bytes{container!~"POD|linkerd-proxy||gluenet.*",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"},"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_memory_used"
            record: "metrics"
        # 三、container单个-disk相关指标
          # 1. 容器磁盘写速率 单位：b/s
          - expr: |
              sum by(pod,container,application_guid) (label_replace(irate(container_fs_writes_bytes_total{container!~"POD|linkerd-proxy",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m]),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_disk_write_rate"
            record: "metrics"
          # 2. 容器磁盘读速率
          - expr: |
              sum by(pod,container,application_guid) (label_replace(irate(container_fs_reads_bytes_total{container!~"POD|linkerd-proxy",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m]),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_disk_read_rate"
            record: "metrics"
          # 四、container-network相关指标
          - expr: |
              sum by(pod,container,application_guid) (label_replace(irate(container_network_receive_bytes_total{container!~"POD|linkerd-proxy",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m]),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_network_receive_kbps"
            record: "metrics"
          - expr: |
              sum by(pod,container,application_guid) (label_replace(irate(container_network_transmit_bytes_total{container!~"POD|linkerd-proxy",image!="",namespace!~"default|kube-system|monitoring|linkerd-viz|linkerd|minikube-frpc"}[1m]),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_network_transmit_kbps"
            record: "metrics"
      #状态
          - expr: |
              sum without(pod,uid,namespace,job,instance)(label_replace((0*kube_pod_container_status_waiting{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz|minikube-frpc",container!~"linkerd-proxy"}+1*kube_pod_container_status_ready{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"}+2*kube_pod_container_status_terminated{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"}),"application_guid","$1","namespace","(.+)"))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_status_information"
            record: "status"
          - expr: |
              avg by(application_guid)(sum without(pod,uid,namespace,job,instance)(label_replace((0*kube_pod_container_status_waiting{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz|minikube-frpc",container!~"linkerd-proxy"}+1*kube_pod_container_status_ready{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz|minikube-frpc",container!~"linkerd-proxy"}+2*kube_pod_container_status_terminated{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz|minikube-frpc",container!~"linkerd-proxy"}),"application_guid","$1","namespace","(.+)")))
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              container: "*"
              agent_guid: "AGENT_GUID"
              label: "application_status_information"
            record: "status"
      #其他
          - expr: |
              sum(label_replace(kubelet_node_name,"host_name","$1","node","(.+)")) by (host_name)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label:  "agent_hosts"
            record: "info"
          - expr: |
              sum(label_replace(label_replace((kube_pod_container_info{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"}) + on (pod,namespace) group_left(node)(0 * kube_pod_info{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz"}),"application_guid","$1","namespace","(.+)"),"host_name","$1","node","(.+)")) without(uid,job,instance,image_id,image_spec,namespace,node)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "instance_containers"
            record: "info"
          - expr: |
              sum(label_replace((kube_pod_container_info{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"} + on (pod,namespace) group_left(host_name)(0 * label_replace(kube_pod_info{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz"},"host_name","$1","node","(.+)"))),"application_guid","$1","namespace","(.+)")) without(uid,job,instance,image_id,image_spec,namespace)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "machine"
              agent_guid: "AGENT_GUID"
              label: "agent_containers"
            record: "info"
          - expr: |
              sum(label_replace(kube_pod_container_info{container!~"linkerd-proxy"},"application_guid","$1","namespace","(.+)"))by(container,application_guid,pod,image,container_id)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_info"
            record: "info"
          - expr: |
              sum(label_replace(kube_pod_container_status_ready{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"},"application_guid","$1","namespace","(.+)")) without(uid,job,instance,namespace)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_state_ready"
            record: "status"
          - expr: |
              sum(label_replace(kube_pod_container_status_waiting{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"},"application_guid","$1","namespace","(.+)")) without(uid,job,instance,namespace)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_state_not_ready"
            record: "status"
          - expr: |
              sum(label_replace(kube_pod_container_status_waiting{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"},"application_guid","$1","namespace","(.+)")) by(application_guid) == 0
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              container: "*"
              label: "application_state_ready"
            record: "status"
          - expr: |
              sum(label_replace(kube_pod_container_status_waiting{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"},"application_guid","$1","namespace","(.+)")) by(application_guid) > 0
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              container: "*"
              label: "application_state_not_ready"
            record: "status"
          - expr: |
              sum(label_replace(kube_pod_container_resource_limits{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"},"application_guid","$1","namespace","(.+)")) without (instance,job,uid,namespace,node)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_cpu_memory_limits"
            record: "resources"
          - expr: |
              sum(label_replace(kube_pod_container_resource_requests{namespace!~"default|monitoring|kube-system|linkerd|linkerd-viz",container!~"linkerd-proxy"},"application_guid","$1","namespace","(.+)")) without (instance,job,uid,namespace,node)
            labels:
              organize: "gluenets"
              platform: "kubernetes"
              object: "application"
              agent_guid: "AGENT_GUID"
              label: "container_cpu_memory_request"
            record: "resources"
---
apiVersion: v1
kind: Pod
metadata:
  name: glue-stream-prom
  namespace: gluenet-test1
  labels:
    app: glue-stream-prom
spec:
  nodeName: worker1.okd.example.com
  containers:
    - name: prometheus
      image: "registry.example.com:8443/prom/prometheus:latest"
      args:
        - --web.enable-remote-write-receiver
        - --web.enable-lifecycle
        - --config.file=/prometheus/config/prometheus.yml
        - --storage.tsdb.path=/prometheus/data/prom
      ports:
        - containerPort: 9090
          name: prometheus
      volumeMounts:
        - mountPath: /prometheus/config/prometheus.yml
          name: prometheus-config
          subPath: prometheus.yml
        - mountPath: /prometheus/rules/rules.yml
          name: prometheus-rules
          subPath: rules.yml
        - mountPath: /prometheus/data/
          name: kubeconfig
  volumes:
    - configMap:
        name: prometheus-config
      name: prometheus-config
    - configMap:
        name: prometheus-rules
      name: prometheus-rules
    - name: kubeconfig
      persistentVolumeClaim:
        claimName: config
---
kind: Service
apiVersion: v1
metadata:
  name: glue-stream-prom-service
  namespace: gluenet-test1
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 10000
      targetPort: 9090
  selector:
    app: glue-stream-prom
---
apiVersion: v1
kind: Pod
metadata:
  name: gluenet-transfer
  labels:
    app.kubernetes.io/component: gluenet-transfer
    app.kubernetes.io/name: gluenet-transfer
    app.kubernetes.io/part-of: kube-prometheus
    app: gluenet-transfer
  namespace: gluenet-test1
spec:
  containers:
    - name: glue-transfer
      image: gluenet/transfer:0.1
      imagePullPolicy: IfNotPresent
      ports:
        - containerPort: 10099
      env:
        - name: RPC_CONFIG
          value: "nats://39.101.140.145:4222"
        - name: PUSH_TOPIC
          value: "guid.manager:rpc.apis.data.metrics.push"
---
apiVersion: v1
kind: Service
metadata:
  name: gluenet-transfer-svc
  namespace: gluenet-test1
spec:
  type: ClusterIP
  ports:
  - name: gluenet-transfer
    protocol: TCP
    port: 10099
    targetPort: 10099
  selector:
    app: gluenet-transfer
---
kind: Service
apiVersion: v1
metadata:
  name: glue-stream-prom-frontend
  namespace: gluenet-test1
spec:
  type: NodePort
  ports:
    - name: http
      port: 55555
      targetPort: 9090
  selector:
    app: glue-stream-prom
```


```yaml
apiVersion: v1
data:
  config.yaml: |
    prometheusK8s:
      remoteWrite:
      - url: "http://glue-stream-prom-service.gluenet-test1:10000/api/v1/write"
        writeRelabelConfigs:
        - sourceLabels: ["prometheus_replica"]
          regex: "prometheus-k8s-0"
          action: "keep"
        - sourceLabels: ["namespace"]
          regex: "openshift.*|kube-.*|open-cluster.*|linkerd|monitoring|gluenet-test1"
          action: "drop"
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
```