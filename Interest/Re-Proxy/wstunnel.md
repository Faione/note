## wstunnel

[wstunnel](https://github.com/erebe/wstunnel)

### Server

```yaml
version: "3"
services:
  ws_server:
    image: "ghcr.io/erebe/wstunnel:v8.5.4"
    network_mode: host
    restart: always
    environment:
      "SERVER_PROTOCOL": "wss"
      "SERVER_LISTEN": "[::]"
      "SERVER_PORT": "20030"
      "CONN_KEY": "f77b499114aab72d7b9fa492630c0edc"
    command:
        - "/bin/sh"
        - "-c"
        - "exec /home/app/wstunnel server $${SERVER_PROTOCOL}://$${SERVER_LISTEN}:$${SERVER_PORT} --restrict-http-upgrade-path-prefix $${CONN_KEY}"
```


### Client


```
SERVER_PROTOCOL=wss
SERVER_LISTEN=""
SERVER_PORT=
CONN_KEY=
```

```yaml
version: "3"

x-common: &common
  image: "ghcr.io/erebe/wstunnel:v8.5.4"
  network_mode: host
  restart: always
  env_file:
    - .env
  command:
    - "/bin/sh"
    - "-c"
    - "exec /home/app/wstunnel client -R tcp://$${REMOTE_SERVICE}:$${LOCAL_SERVICE} $${SERVER_PROTOCOL}://$${SERVER_LISTEN}:$${SERVER_PORT} --http-upgrade-path-prefix $${CONN_KEY}"

services:
  local_ssh:
    <<: *common
    environment:
      "LOCAL_SERVICE": "localhost:22"
      "REMOTE_SERVICE": "[::]:20031"
```