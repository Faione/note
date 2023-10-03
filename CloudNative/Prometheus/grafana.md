# Grafana

Grafana 是一个数据展示/分析平台

选择 Prometheus 作为数据源， Grafana通过 `exp` 表达式周期性地从 Prometheus 获取数据，并转化为 DataFrame 在前端进行展示

## Provision

使用 Provision [^1]可通过配置文件来让 Grafana 自动导入 DataSource 配置与 Dashboard 配置, 需要注意在 grafana 的配置文件中会有默认的 Provision检索路径

[^1]: [provisioning](https://grafana.com/docs/grafana/v9.4/administration/provisioning/)

### DataSource

配置 Prometheus DataSource 时，需要注意相关字段与配置文件的差异，参考 Provision 中的定义进行编写

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    # change `prometheus` to real endpoint
    url: http://prometheus:9090
    uid: master_prometheus
    isDefault: true
    jsonData:
      timeInterval: 4s
      timeout: 4s
      httpMethod: POST
      prometheusType: Prometheus
```

[promeetheus_json_data](https://grafana.com/docs/grafana/v9.4/administration/provisioning/#json-data)
[prometheus_ds](https://grafana.com/docs/grafana/v9.4/datasources/prometheus/#provision-the-data-source)

### DashBoards

DashBoards 也可预先进行配置，注意除定义 Dashboard 本身的 json 文件外，还需要在Provision中定义获取 Dashboard 的方式

```yaml
apiVersion: 1

providers:
  # <string> an unique provider name. Required
  - name: 'ict_acs'
    # <int> Org id. Default to 1
    orgId: 1
    # <string> name of the dashboard folder.
    folder: ''
    # <string> folder UID. will be automatically generated if not specified
    folderUid: ''
    # <string> provider type. Default to 'file'
    type: file
    # <bool> disable dashboard deletion
    disableDeletion: false
    # <int> how often Grafana will scan for changed dashboards
    updateIntervalSeconds: 10
    # <bool> allow updating provisioned dashboards from the UI
    allowUiUpdates: false
    options:
      # <string, required> path to dashboard files on disk. Required when using the 'file' type
      path: /etc/dashboards
      # <bool> use folder names from filesystem to create folders in Grafana
      foldersFromFilesStructure: true
```