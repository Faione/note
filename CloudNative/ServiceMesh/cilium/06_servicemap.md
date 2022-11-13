## MapDemo

Base Service

api

```yaml
# api_config_map.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: apis
data:
  db.json: |-
    {
    "posts": [
        { "id": 1, "body": "foo" },
        { "id": 2, "body": "bar" }
    ]
    }

```
service

```yaml
---
# base_service_deploy.yaml
---
apiVersion: v1
kind: Service
metadata:
  name: demo-service-{service_num}
  labels:
    app.kubernetes.io/name: demo-service-{service_num}
spec:
  type: ClusterIP
  ports:
  - port: 80
  selector:
    app: demo-service-{service_num}
---
apiVersion: v1
kind: Pod
metadata:
  name: demo-service-{service_num}
  labels:
    app: demo-service-{service_num}
  annotations:
    io.cilium.proxy-visibility: "<Ingress/80/TCP/HTTP>"
spec:
  containers:
  - name: demo-service-{service_num}
    image: clue/json-server:latest
    volumeMounts:
      - mountPath: /data/
        name: apiconfig
  volumes:
    - name: apiconfig
      configMap:
        name: apis
        items:
        - key: db.json
          path: db.json

```

scripts

```python
import click
import subprocess
import os

DEFAULT_YAML = "test.yaml"
DEFAULT_DEPTH = 3
DEFAULT_NS = "test-guid-service-map"

API_CONFIG_MAP_YAML = "api_config_map.yaml"
BASE_SERVICE_YAML = "base_service_deploy.yaml"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--depth', default=DEFAULT_DEPTH, help="Depth of the service tree")
@click.option('--file', default=DEFAULT_YAML, help="Yaml file of the target service tree")
def create(depth, file):
    nodes = 2 ** depth - 1
    # prepare configMap
    cmd = ["cat", API_CONFIG_MAP_YAML, ">", DEFAULT_YAML]
    subprocess.getstatusoutput(" ".join(cmd))
    for i in range(1, 1 + nodes):
        cmd = ["sed", "-e", '"s/{service_num}/'+ str(i) + '/g"', BASE_SERVICE_YAML, ">>", DEFAULT_YAML]
        subprocess.getstatusoutput(" ".join(cmd))

@cli.command()
@click.option('--file', default=DEFAULT_YAML, help="Yaml file of the target service tree")
def delete(file):
    cmd = ["rm ", file]
    subprocess.getstatusoutput(" ".join(cmd))

@cli.command()
@click.option('--file', default=DEFAULT_YAML, help="Yaml file of the target service tree")
@click.option('--namespace', default=DEFAULT_NS, help="Namespace of the target service tree")
def deploy(namespace, file):
    cmd = ["kubectl", "create", "ns", namespace]
    subprocess.getstatusoutput(" ".join(cmd))
    cmd = ["kubectl", "apply" , "-n", namespace, "-f", file]
    subprocess.getstatusoutput(" ".join(cmd))

@cli.command()
@click.option('--file', default=DEFAULT_YAML, help="Yaml file of the target service tree")
@click.option('--namespace', default=DEFAULT_NS, help="Namespace of the target service tree")
def undeploy(namespace, file):
    cmd = ["kubectl", "delete", "-n", namespace, "-f", file]
    subprocess.getstatusoutput(" ".join(cmd))

@cli.command()
@click.option('--depth', default=DEFAULT_DEPTH, help="Depth of the service tree")
@click.option('--namespace', default=DEFAULT_NS, help="Namespace of the target service tree")
def test(namespace, depth):
    non_leaf_nodes = 2 ** (depth-1) - 1
    for i in range(1, 1 + non_leaf_nodes):
        child = [2 * i, 2 * i +1]
        for c in child:
            curl_cmd = ["curl", "-s", "--connect-timeout", "3", "demo-service-" + str(c) + "." + namespace + ".svc.cluster.local/posts"]
            cmd = ["kubectl", "-n", namespace, "exec", "-it", "demo-service-" + str(i), "--"] + curl_cmd
            subprocess.getstatusoutput(" ".join(cmd))

if __name__ == "__main__":
    cli()
```

