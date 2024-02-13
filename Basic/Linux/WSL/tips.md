## WSL2 网络

WSL2 2023近期更新中，映入了 `mirrored` 网络模式，使得WSL与宿主机能够有近乎一致的网络环境(IP,代理)

```
[experimental]
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true
```

使用 `mirrored` 网络模式会导致先前的透明代理失效，特别在容器场景中， 容器中的 `localhost` 与 宿主的 localhost 不同，为避免这种问题，可以通过 `network host` 解除网络隔离实现, 同样地，在 build 过程中，也可以解除网络隔离来利用 localhost 上的代理服务