# Prometheus自动发现

## 基于文件的自动发现

### Prometheus Server 配置文件

- [基于文件的服务发现](https://www.prometheus.wang/sd/service-discovery-with-file.html)
- [prometheus_file_sd_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#file_sd_config)

**targets.json**

- 配置监控目标
  - labels可以自定义添加内容

```json
[
  {
    "targets": [ "192.168.176.128:9100"],
    "labels": {
      "env": "localhost",
      "job": "node-exporter"
    }
  },
  {
    "targets": ["localhost:9090"],
    "labels": {
      "guid": "aab",
      "job": "prometheus"
    }
  }
]
```

**prometheus.yml**

- 配置 file_sd_configs 任务
  -  `files` 指定targets文件，默认从当前目录寻找
  -  `refresh_interval` 可配置刷新监控目标的周期

```yml
global:
  scrape_interval:     15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: file_ds
    file_sd_configs:
    - refresh_interval: 1m
      files:
        - targets.json
```

**dokcer-compose.yml**

- 绑定目录而非文件

```yml
version: "3"
services:
  prometheus:
    image: "prom/prometheus"
    ports:
      - "10090:9090"
    volumes:
      - ./prometheus/:/etc/prometheus/
```

### 基于 Http 的服务发现

- [Prometheus Http](https://prometheus.io/docs/prometheus/latest/http_sd/#writing-http-service-discovery)

**prometheus.yml**

- 配置 http_sd 任务
  -  `url` 提供targets的 url
  -  `refresh_interval` 可配置刷新监控目标的周期

```yml
global:
  scrape_interval:     15s
  evaluation_interval: 15s

scrape_configs:
    - job_name: http_sd
      http_sd_configs:
      - url: 192.168.176.128:10091/targets
        refresh_interval: 1m
```

- config server go 实现


```go
const (
	JOB_KEY  = `job`
	GUID_KEY = `guid`
	GUID     = `test-guid`
)

type Target struct {
	Targets []string          `json:"targets"`
	Labels  map[string]string `json:"labels"`
}

func genNodeExporterConfig() Target {
	targets := []string{"192.168.176.128:9100"}
	labels := make(map[string]string)

	labels[JOB_KEY] = "node_exporter"
	labels[GUID_KEY] = GUID

	return Target{
		Targets: targets,
		Labels:  labels,
	}
}

func handleTargets(w http.ResponseWriter, r *http.Request) {
	nodeExporterConfig := genNodeExporterConfig()

	targets := []Target{nodeExporterConfig}

	bytes, err := json.Marshal(targets)
	if err != nil {
		fmt.Println("marshal result err")
		w.Write([]byte(`server err`))
		return
	}

  // 需要对响应头部进行设置
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(200)
	w.Write(bytes)
	fmt.Println(string(bytes))
}

func main() {
	http.HandleFunc("/targets", handleTargets)

	log.Fatal(http.ListenAndServe("192.168.176.128:10091", nil))
}
```