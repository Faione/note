## Qemu Bridge 设置

[missing_bridge_conf](https://qemu-discuss.nongnu.narkive.com/rNgxmrbk/missing-bridge-conf)

```shell
echo 'allow br0' | sudo tee -a /etc/qemu/bridge.conf
```