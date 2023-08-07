- 支持监控目标热修改
- helm安装

[pod 与configMap交互](https://zhuanlan.zhihu.com/p/57570231)
[viper watch config](https://blog.csdn.net/Vancl_Wang/article/details/103234240)


```json
{
    "code": 200,
    "message": "succeed",
    "data": {
        "requests": [
            {
                "source_pod": "test-guid-1/tiefighter",
                "destination_pod": "test-guid-1/deathstar-6c94dcc57b-r86v7",
                "destination_port": "80",
                "verdict": "FORWARDED",
                "protocol": "HTTP/1.1",
                "method": "POST",
                "url": "/v1/request-landing"
            }
        ],
        "services": [
            {
                "name": "test-guid-1/deathstar-6c94dcc57b-r86v7",
                "labels": [
                    {
                        "foo": "bar"
                    }
                ],
                "ip": "10.0.1.69",
                "ports": [
                    {
                        "port": "80",
                        "protocol": "HTTP/1.1",
                        "urls": [
                            "/v1/request-landing",
                            "/v1/request-firing"
                        ]
                    },
                    {
                        "port": "443",
                        "protocol": "HTTP/1.1",
                        "urls": [
                            "/v1/request-takin-off"
                        ]
                    }
                ]
            },
            {
                "name": "test-guid-1/tiefighter",
                "labels": [
                    {
                        "foo": "bar"
                    }
                ],
                "ip": "10.0.1.3",
                "ports": []
            }
        ]
    }
}
```

```json
{
    "code": 200,
    "message": "succeed",
    "data": {
        "servicemap": {
            "test-guid-1/tiefighter": {
                "test-guid-1/deathstar-6c94dcc57b-r86v7": [
                    "sasdqwersagfqwe123"
                ]
            }
        },
        "requests": {
            "sasdqwersagfqwe123":       {
                "source_pod": "test-guid-1/tiefighter",
                "destination_pod": "test-guid-1/deathstar-6c94dcc57b-r86v7",
                "destination_port": "80",
                "verdict": "FORWARDED",
                "protocol": "HTTP/1.1",
                "method": "POST",
                "url": "/v1/request-landing"
            }
        },
        "services": {
            "test-guid-1/tiefighter": {
                "labels": [
                    {
                        "foo": "bar"
                    }
                ],
                "ip": "10.0.1.3",
                "ports": []
            },
             "test-guid-1/deathstar-6c94dcc57b-r86v7":           {
                "labels": [
                    {
                        "foo": "bar"
                    }
                ],
                "ip": "10.0.1.69",
                "ports": [
                    {
                        "port": "80",
                        "protocol": "HTTP/1.1",
                        "urls": [
                            "/v1/request-landing",
                            "/v1/request-firing"
                        ]
                    },
                    {
                        "port": "443",
                        "protocol": "HTTP/1.1",
                        "urls": [
                            "/v1/request-takin-off"
                        ]
                    }
                ]
            },
        }
    }
}
```