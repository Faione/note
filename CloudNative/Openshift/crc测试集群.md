# 搭建crc测试集群

[crc-official](https://crc.dev/crc/)
[crc-github](https://github.com/code-ready/crc)
[crc-csdn](https://blog.csdn.net/weixin_43902588/article/details/109571198)


pullsecret 地址
- https://console.redhat.com/openshift/install/pull-secret

?X11与crc存在冲突，当存在 `.Xauthority` 文件时, crc 的执行会异常缓慢
- 开启X11, 并在每次登陆时删除 `.Xauthority`

windows访问
- ssh隧道目标ip与端口
- 修改windows host文件 `C:\Windows\System32\drivers\etc\hosts`

增加主要服务的dns静态解析

```
127.0.0.1 console-openshift-console.apps-crc.testing
127.0.0.1 oauth-openshift.apps-crc.testing
```