# MaaS需求

- [MaaS需求](#maas需求)
  - [系统镜像查询](#系统镜像查询)
    - [需求描述](#需求描述)
    - [请求接口](#请求接口)
    - [数据格式](#数据格式)
  - [网段查询](#网段查询)
    - [需求描述](#需求描述-1)
    - [请求接口](#请求接口-1)
    - [数据格式](#数据格式-1)
  - [宿主机查询](#宿主机查询)
    - [需求描述](#需求描述-2)
    - [请求接口](#请求接口-2)
    - [数据格式](#数据格式-2)
  - [KVM虚拟机创建](#kvm虚拟机创建)
    - [需求描述](#需求描述-3)
    - [请求接口](#请求接口-3)
    - [数据格式](#数据格式-3)
  - [裸机查询](#裸机查询)
    - [需求描述](#需求描述-4)
    - [请求接口](#请求接口-4)
    - [数据格式](#数据格式-4)
  - [附录](#附录)
    - [虚拟机参数](#虚拟机参数)
      - [可选参数](#可选参数)
      - [标签列表](#标签列表)
    - [裸机参数](#裸机参数)
      - [可选参数](#可选参数-1)
      - [标签列表](#标签列表-1)
    - [相关链接](#相关链接)


## 系统镜像查询

### 需求描述

普通用户在前端创建虚拟机时，能够系统中当前可用的系统镜像中选择合适的镜像，以便进行虚拟机/裸机的系统的设置

1. MaaS端查询系统镜像列表返回数据格式，区分不同源(MaaS官方，第三方)

### 请求接口

`GetSubObject("boot-resources")`

```go
// pkg: github.com/maas/gomaasclient/client

c ,_ := cli.GetApiClient("http://10.16.0.218:5240/MAAS", "Y3BDFAL4SjXX6f6BrY:WfrSbfL8BsQ55gqEr9:ZdEgqc5nKWjVarxdETxucc4Ks4kx5mZ7", "2.0")
err := c2.GetSubObject("boot-resources").Get("",url.Values{}, func(bytes []byte) error {
	fmt.Printf("返回json字符串 %s",bytes)
	return nil
})
```

### 数据格式

返回数据， 主要字段为 name、architecture

```json

[
    {
        "id": 7,
        "type": "Synced",
        "name": "grub-efi-signed/uefi",
        "architecture": "amd64/generic",
        "resource_uri": "/MAAS/api/2.0/boot-resources/7/"
    },
    {
        "id": 8,
        "type": "Synced",
        "name": "grub-efi/uefi",
        "architecture": "arm64/generic",
        "resource_uri": "/MAAS/api/2.0/boot-resources/8/"
    },
    {
        "id": 9,
        "type": "Synced",
        "name": "grub-ieee1275/open-firmware",
        "architecture": "ppc64el/generic",
        "resource_uri": "/MAAS/api/2.0/boot-resources/9/"
    },
    {
        "id": 10,
        "type": "Synced",
        "name": "pxelinux/pxe",
        "architecture": "i386/generic",
        "resource_uri": "/MAAS/api/2.0/boot-resources/10/"
    },
    {
        "id": 1,
        "type": "Synced",
        "name": "ubuntu/focal",
        "architecture": "amd64/ga-20.04",
        "resource_uri": "/MAAS/api/2.0/boot-resources/1/",
        "subarches": "generic,hwe-p,hwe-q,hwe-r,hwe-s,hwe-t,hwe-u,hwe-v,hwe-w,ga-16.04,ga-16.10,ga-17.04,ga-17.10,ga-18.04,ga-18.10,ga-19.04,ga-19.10,ga-20.04"
    },
    {
        "id": 2,
        "type": "Synced",
        "name": "ubuntu/focal",
        "architecture": "amd64/ga-20.04-lowlatency",
        "resource_uri": "/MAAS/api/2.0/boot-resources/2/",
        "subarches": "generic,hwe-p,hwe-q,hwe-r,hwe-s,hwe-t,hwe-u,hwe-v,hwe-w,ga-16.04,ga-16.10,ga-17.04,ga-17.10,ga-18.04,ga-18.10,ga-19.04,ga-19.10,ga-20.04"
    },
    {
        "id": 3,
        "type": "Synced",
        "name": "ubuntu/focal",
        "architecture": "amd64/hwe-20.04",
        "resource_uri": "/MAAS/api/2.0/boot-resources/3/",
        "subarches": "generic,hwe-p,hwe-q,hwe-r,hwe-s,hwe-t,hwe-u,hwe-v,hwe-w,ga-16.04,ga-16.10,ga-17.04,ga-17.10,ga-18.04,ga-18.10,ga-19.04,ga-19.10,ga-20.04"
    },
    {
        "id": 4,
        "type": "Synced",
        "name": "ubuntu/focal",
        "architecture": "amd64/hwe-20.04-edge",
        "resource_uri": "/MAAS/api/2.0/boot-resources/4/",
        "subarches": "generic,hwe-p,hwe-q,hwe-r,hwe-s,hwe-t,hwe-u,hwe-v,hwe-w,ga-16.04,ga-16.10,ga-17.04,ga-17.10,ga-18.04,hwe-18.10,hwe-19.04,hwe-19.10,hwe-20.04"
    },
    {
        "id": 5,
        "type": "Synced",
        "name": "ubuntu/focal",
        "architecture": "amd64/hwe-20.04-lowlatency",
        "resource_uri": "/MAAS/api/2.0/boot-resources/5/",
        "subarches": "generic,hwe-p,hwe-q,hwe-r,hwe-s,hwe-t,hwe-u,hwe-v,hwe-w,ga-16.04,ga-16.10,ga-17.04,ga-17.10,ga-18.04,ga-18.10,ga-19.04,ga-19.10,ga-20.04"
    },
    {
        "id": 6,
        "type": "Synced",
        "name": "ubuntu/focal",
        "architecture": "amd64/hwe-20.04-lowlatency-edge",
        "resource_uri": "/MAAS/api/2.0/boot-resources/6/",
        "subarches": "generic,hwe-p,hwe-q,hwe-r,hwe-s,hwe-t,hwe-u,hwe-v,hwe-w,ga-16.04,ga-16.10,ga-17.04,ga-17.10,ga-18.04,hwe-18.10,hwe-19.04,hwe-19.10,hwe-20.04"
    }
]
```


## 网段查询

### 需求描述

普通用户在前端创建虚拟机时，能够从系统中当前可选网段中选择合适的网段，以便进行虚拟机/裸机的网段设置

1. MaaS端查询网段列表返回数据格式

### 请求接口

`GetSubObject("subnets")`

```go
c ,_ := cli.GetApiClient("http://10.16.0.218:5240/MAAS", "Y3BDFAL4SjXX6f6BrY:WfrSbfL8BsQ55gqEr9:ZdEgqc5nKWjVarxdETxucc4Ks4kx5mZ7", "2.0")
err := c2.GetSubObject("subnets").Get("",url.Values{}, func(bytes []byte) error {
	fmt.Printf("返回json字符串 %s",bytes)
	return nil
})
```

### 数据格式

```json
[
    {
        "name": "10.16.0.0/24",
        "description": "",
        "vlan": {
            "vid": 0,
            "mtu": 1500,
            "dhcp_on": true,
            "external_dhcp": null,
            "relay_vlan": null,
            "id": 5001,
            "secondary_rack": null,
            "fabric": "fabric-0",
            "space": "undefined",
            "fabric_id": 0,
            "name": "untagged",
            "primary_rack": "bfdhyc",
            "resource_uri": "/MAAS/api/2.0/vlans/5001/"
        },
        "cidr": "10.16.0.0/24",
        "rdns_mode": 2,
        "gateway_ip": "10.16.0.254",
        "dns_servers": [],
        "allow_dns": true,
        "allow_proxy": true,
        "active_discovery": false,
        "managed": true,
        "disabled_boot_architectures": [],
        "id": 1,
        "space": "undefined",
        "resource_uri": "/MAAS/api/2.0/subnets/1/"
    },
    {
        "name": "172.16.0.0/16",
        "description": "",
        "vlan": {
            "vid": 0,
            "mtu": 1500,
            "dhcp_on": true,
            "external_dhcp": null,
            "relay_vlan": null,
            "id": 5001,
            "secondary_rack": null,
            "fabric": "fabric-0",
            "space": "undefined",
            "fabric_id": 0,
            "name": "untagged",
            "primary_rack": "bfdhyc",
            "resource_uri": "/MAAS/api/2.0/vlans/5001/"
        },
        "cidr": "172.16.0.0/16",
        "rdns_mode": 2,
        "gateway_ip": null,
        "dns_servers": [],
        "allow_dns": true,
        "allow_proxy": true,
        "active_discovery": false,
        "managed": true,
        "disabled_boot_architectures": [],
        "id": 2,
        "space": "undefined",
        "resource_uri": "/MAAS/api/2.0/subnets/2/"
    },
    {
        "name": "192.168.122.0/24",
        "description": "",
        "vlan": {
            "vid": 0,
            "mtu": 1500,
            "dhcp_on": false,
            "external_dhcp": null,
            "relay_vlan": null,
            "id": 5002,
            "secondary_rack": null,
            "fabric": "fabric-1",
            "space": "undefined",
            "fabric_id": 1,
            "name": "untagged",
            "primary_rack": null,
            "resource_uri": "/MAAS/api/2.0/vlans/5002/"
        },
        "cidr": "192.168.122.0/24",
        "rdns_mode": 2,
        "gateway_ip": null,
        "dns_servers": [],
        "allow_dns": true,
        "allow_proxy": true,
        "active_discovery": false,
        "managed": true,
        "disabled_boot_architectures": [],
        "id": 4,
        "space": "undefined",
        "resource_uri": "/MAAS/api/2.0/subnets/4/"
    },
    {
        "name": "192.168.2.0/24",
        "description": "",
        "vlan": {
            "vid": 0,
            "mtu": 1500,
            "dhcp_on": true,
            "external_dhcp": null,
            "relay_vlan": null,
            "id": 5001,
            "secondary_rack": null,
            "fabric": "fabric-0",
            "space": "undefined",
            "fabric_id": 0,
            "name": "untagged",
            "primary_rack": "bfdhyc",
            "resource_uri": "/MAAS/api/2.0/vlans/5001/"
        },
        "cidr": "192.168.2.0/24",
        "rdns_mode": 2,
        "gateway_ip": "192.168.2.254",
        "dns_servers": [],
        "allow_dns": true,
        "allow_proxy": true,
        "active_discovery": false,
        "managed": true,
        "disabled_boot_architectures": [],
        "id": 3,
        "space": "undefined",
        "resource_uri": "/MAAS/api/2.0/subnets/3/"
    },
    {
        "name": "10.12.26.0/24",
        "description": "",
        "vlan": {
            "vid": 0,
            "mtu": 1500,
            "dhcp_on": false,
            "external_dhcp": null,
            "relay_vlan": null,
            "id": 5003,
            "secondary_rack": null,
            "fabric": "fabric-2",
            "space": "undefined",
            "fabric_id": 2,
            "name": "untagged",
            "primary_rack": null,
            "resource_uri": "/MAAS/api/2.0/vlans/5003/"
        },
        "cidr": "10.12.26.0/24",
        "rdns_mode": 2,
        "gateway_ip": null,
        "dns_servers": [],
        "allow_dns": true,
        "allow_proxy": true,
        "active_discovery": false,
        "managed": true,
        "disabled_boot_architectures": [],
        "id": 5,
        "space": "undefined",
        "resource_uri": "/MAAS/api/2.0/subnets/5/"
    },
    {
        "name": "fd42:91fa:b2a2:5f99::/64",
        "description": "",
        "vlan": {
            "vid": 0,
            "mtu": 1500,
            "dhcp_on": false,
            "external_dhcp": null,
            "relay_vlan": null,
            "id": 5003,
            "secondary_rack": null,
            "fabric": "fabric-2",
            "space": "undefined",
            "fabric_id": 2,
            "name": "untagged",
            "primary_rack": null,
            "resource_uri": "/MAAS/api/2.0/vlans/5003/"
        },
        "cidr": "fd42:91fa:b2a2:5f99::/64",
        "rdns_mode": 2,
        "gateway_ip": null,
        "dns_servers": [],
        "allow_dns": true,
        "allow_proxy": true,
        "active_discovery": false,
        "managed": true,
        "disabled_boot_architectures": [],
        "id": 6,
        "space": "undefined",
        "resource_uri": "/MAAS/api/2.0/subnets/6/"
    }
]
```

## 宿主机查询

### 需求描述

普通用户在前端创建虚拟机时，能够通过地域、标签、网段等筛选符合需求的物理机，以便进行虚拟机的资源配置

1. MaaS端查询裸机列表请求参数，以及返回数据格式

### 请求接口

`GetSubObject("vm-hosts")`
- maas 只提供 list all vm host


```go
c ,_ := cli.GetApiClient("http://10.16.0.218:5240/MAAS", "Y3BDFAL4SjXX6f6BrY:WfrSbfL8BsQ55gqEr9:ZdEgqc5nKWjVarxdETxucc4Ks4kx5mZ7", "2.0")
err := c2.GetSubObject("vm-hosts").Get("",url.Values{}, func(bytes []byte) error {
	fmt.Printf("返回json字符串 %s",bytes)
	return nil
})
```

### 数据格式

返回数据

```json
[
    {
        "cpu_over_commit_ratio": 1.0,
        "id": 8,
        "name": "ubuntu-219",
        "version": "5.5",
        "memory_over_commit_ratio": 1.0,
        "capabilities": [
            "composable",
            "dynamic_local_storage",
            "over_commit",
            "storage_pools"
        ],
        "zone": {
            "name": "default",
            "description": "",
            "id": 1,
            "resource_uri": "/MAAS/api/2.0/zones/default/"
        },
        "storage_pools": [
            {
                "id": "default",
                "name": "default",
                "type": "dir",
                "path": "/var/snap/lxd/common/lxd/storage-pools/default",
                "total": 1967845019648,
                "used": 1400000000000,
                "available": 567845019648,
                "default": true
            }
        ],
        "architectures": [
            "amd64/generic"
        ],
        "default_macvlan_mode": null,
        "used": {
            "cores": 36,
            "memory": 57364,
            "local_storage": 1400000000000
        },
        "pool": {
            "name": "default",
            "description": "Default pool",
            "id": 0,
            "resource_uri": "/MAAS/api/2.0/resourcepool/0/"
        },
        "type": "lxd",
        "total": {
            "cores": 40,
            "memory": 65536,
            "local_storage": 1967845019648
        },
        "available": {
            "cores": 4,
            "memory": 8172,
            "local_storage": 567845019648
        },
        "tags": [
            "pod-console-logging"
        ],
        "host": {
            "system_id": "etn3be",
            "__incomplete__": true
        },
        "resource_uri": "/MAAS/api/2.0/vm-hosts/8/"
    }
]
```

## KVM虚拟机创建

### 需求描述

普通用户在填写完表单并提交，能够得到系统正在创建的反馈并在完成后获得虚拟机的相关信息，以便进行下一步操作

1. MaaS端查询虚拟机请求参数，以及返回数据格式

### 请求接口

`GetSubObject("vm-hosts")`

- [虚拟机可选参数](#虚拟机参数)

```go
c ,_ := cli.GetApiClient("http://10.16.0.218:5240/MAAS", "Y3BDFAL4SjXX6f6BrY:WfrSbfL8BsQ55gqEr9:ZdEgqc5nKWjVarxdETxucc4Ks4kx5mZ7", "2.0")

// 参数设置
val := url.Values{}
val.Set("hostname","vm1") // 命名不要冲突
val.Set("interfaces","eth0:subnet_cidr=192.168.2.0/24") // 网段选择
val.Set("storage","test:10(default)") // 磁盘悬着

// 这里的"8"是 vmhost 的id，需要在哪台vmhost上创建，就选哪台
err := c.GetSubObject("vm-hosts").GetSubObject("8").Post("compose",val, func(bytes []byte) error {
	fmt.Printf("get %s",bytes)
	return nil
})
```

### 数据格式

返回数据

```json
{
    "system_id": "ag3h8y",
    "resource_uri": "/MAAS/api/2.0/machines/ag3h8y/"
}
```

## 裸机查询

### 需求描述

普通用户在前端添加裸机时，能够从系统中当前可发现的裸机中选择合适的配置，以便于挑选合适配置的裸机

1. MaaS端查询裸机列表请求参数，以及返回数据格式

### 请求接口

`GetSubObject("machines")`

```go
c ,_ := cli.GetApiClient("http://10.16.0.218:5240/MAAS", "Y3BDFAL4SjXX6f6BrY:WfrSbfL8BsQ55gqEr9:ZdEgqc5nKWjVarxdETxucc4Ks4kx5mZ7", "2.0")
val := url.Values{}
val.Set("hostname","vm1")
...设置参数...
err := c2.GetSubObject("machines").Get("",val, func(bytes []byte) error {
	fmt.Printf("返回json字符串 %s",bytes)
	return nil
})
```

### 数据格式

返回数据结构

```json
[
    {
        "interface_test_status_name": "Unknown",
        "commissioning_status": 2,
        "hardware_info": {
            "system_vendor": "QEMU",
            "system_product": "Standard PC (Q35 + ICH9, 2009)",
            "system_family": "Unknown",
            "system_version": "pc-q35-7.0",
            "system_sku": "Unknown",
            "system_serial": "Unknown",
            "cpu_model": "Intel(R) Xeon(R) CPU E5-2630 v4",
            "mainboard_vendor": "Canonical Ltd.",
            "mainboard_product": "LXD",
            "mainboard_serial": "Unknown",
            "mainboard_version": "pc-q35-7.0",
            "mainboard_firmware_vendor": "EFI Development Kit II / OVMF",
            "mainboard_firmware_date": "02/06/2015",
            "mainboard_firmware_version": "0.0.0",
            "chassis_vendor": "QEMU",
            "chassis_type": "Other",
            "chassis_serial": "Unknown",
            "chassis_version": "pc-q35-7.0"
        },
        "memory_test_status_name": "Unknown",
        "min_hwe_kernel": "",
        "status_name": "Allocated",
        "node_type": 0,
        "netboot": true,
        "osystem": "",
        "storage": 200000.004096,
        "status": 10,
        "next_sync": null,
        "fqdn": "vm1.test-k8s",
        "special_filesystems": [],
        "last_sync": null,
        "interface_test_status": -1,
        "cpu_test_status_name": "Unknown",
        "domain": {
            "authoritative": true,
            "ttl": null,
            "id": 2,
            "resource_record_count": 0,
            "is_default": false,
            "name": "test-k8s",
            "resource_uri": "/MAAS/api/2.0/domains/2/"
        },
        "default_gateways": {
            "ipv4": {
                "gateway_ip": "10.16.0.254",
                "link_id": null
            },
            "ipv6": {
                "gateway_ip": null,
                "link_id": null
            }
        },
        "distro_series": "",
        "swap_size": null,
        "cpu_count": 4,
        "current_testing_result_id": 30,
        "pod": {
            "id": 8,
            "name": "ubuntu-219",
            "resource_uri": "/MAAS/api/2.0/pods/8/"
        },
        "hardware_uuid": "994e8dfa-d45f-44cc-8999-92dfbcdd07a2",
        "virtualmachine_id": 4,
        "sync_interval": null,
        "pool": {
            "name": "default",
            "description": "Default pool",
            "id": 0,
            "resource_uri": "/MAAS/api/2.0/resourcepool/0/"
        },
        "other_test_status": -1,
        "power_state": "off",
        "address_ttl": null,
        "architecture": "amd64/generic",
        "network_test_status_name": "Unknown",
        "storage_test_status": 2,
        "boot_interface": {
            "params": "",
            "effective_mtu": 1500,
            "vendor": null,
            "interface_speed": 0,
            "parents": [],
            "numa_node": 0,
            "name": "eth0",
            "vlan": {
                "vid": 0,
                "mtu": 1500,
                "dhcp_on": true,
                "external_dhcp": null,
                "relay_vlan": null,
                "id": 5001,
                "secondary_rack": null,
                "fabric": "fabric-0",
                "space": "undefined",
                "fabric_id": 0,
                "name": "untagged",
                "primary_rack": "bfdhyc",
                "resource_uri": "/MAAS/api/2.0/vlans/5001/"
            },
            "children": [],
            "link_speed": 0,
            "link_connected": true,
            "mac_address": "00:16:3e:f9:ba:58",
            "product": null,
            "system_id": "sbfrtx",
            "enabled": true,
            "links": [
                {
                    "id": 47,
                    "mode": "auto",
                    "subnet": {
                        "name": "10.16.0.0/24",
                        "description": "",
                        "vlan": {
                            "vid": 0,
                            "mtu": 1500,
                            "dhcp_on": true,
                            "external_dhcp": null,
                            "relay_vlan": null,
                            "id": 5001,
                            "secondary_rack": null,
                            "fabric": "fabric-0",
                            "space": "undefined",
                            "fabric_id": 0,
                            "name": "untagged",
                            "primary_rack": "bfdhyc",
                            "resource_uri": "/MAAS/api/2.0/vlans/5001/"
                        },
                        "cidr": "10.16.0.0/24",
                        "rdns_mode": 2,
                        "gateway_ip": "10.16.0.254",
                        "dns_servers": [],
                        "allow_dns": true,
                        "allow_proxy": true,
                        "active_discovery": false,
                        "managed": true,
                        "disabled_boot_architectures": [],
                        "id": 1,
                        "space": "undefined",
                        "resource_uri": "/MAAS/api/2.0/subnets/1/"
                    }
                }
            ],
            "discovered": [
                {
                    "subnet": {
                        "name": "192.168.2.0/24",
                        "description": "",
                        "vlan": {
                            "vid": 0,
                            "mtu": 1500,
                            "dhcp_on": true,
                            "external_dhcp": null,
                            "relay_vlan": null,
                            "id": 5001,
                            "secondary_rack": null,
                            "fabric": "fabric-0",
                            "space": "undefined",
                            "fabric_id": 0,
                            "name": "untagged",
                            "primary_rack": "bfdhyc",
                            "resource_uri": "/MAAS/api/2.0/vlans/5001/"
                        },
                        "cidr": "192.168.2.0/24",
                        "rdns_mode": 2,
                        "gateway_ip": "192.168.2.254",
                        "dns_servers": [],
                        "allow_dns": true,
                        "allow_proxy": true,
                        "active_discovery": false,
                        "managed": true,
                        "disabled_boot_architectures": [],
                        "id": 3,
                        "space": "undefined",
                        "resource_uri": "/MAAS/api/2.0/subnets/3/"
                    },
                    "ip_address": "192.168.2.208"
                }
            ],
            "firmware_version": null,
            "tags": [],
            "id": 58,
            "sriov_max_vf": 0,
            "type": "physical",
            "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/interfaces/58/"
        },
        "owner_data": {},
        "testing_status": 2,
        "volume_groups": [],
        "other_test_status_name": "Unknown",
        "hostname": "vm1",
        "physicalblockdevice_set": [
            {
                "firmware_version": "2.5+",
                "numa_node": 0,
                "available_size": 0,
                "used_for": "GPT partitioned with 2 partitions",
                "name": "sda",
                "block_size": 512,
                "path": "/dev/disk/by-dname/sda",
                "filesystem": null,
                "uuid": null,
                "serial": "lxd_root",
                "size": 200000004096,
                "storage_pool": "default",
                "system_id": "sbfrtx",
                "partition_table_type": "GPT",
                "model": "QEMU HARDDISK",
                "tags": [
                    "rotary",
                    "1rpm"
                ],
                "id": 8,
                "partitions": [
                    {
                        "uuid": "477e2c43-7399-4d51-bc7f-c6f7f5239e15",
                        "size": 536870912,
                        "bootable": true,
                        "tags": [],
                        "device_id": 8,
                        "id": 4,
                        "system_id": "sbfrtx",
                        "used_for": "fat32 formatted filesystem mounted at /boot/efi",
                        "type": "partition",
                        "path": "/dev/disk/by-dname/sda-part1",
                        "filesystem": {
                            "fstype": "fat32",
                            "label": "efi",
                            "uuid": "4e55c61b-9526-4610-a796-84d1c09a0909",
                            "mount_point": "/boot/efi",
                            "mount_options": null
                        },
                        "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/partition/4"
                    },
                    {
                        "uuid": "1a96372d-5e1c-49eb-b986-e6ffdc8a506b",
                        "size": 199455932416,
                        "bootable": false,
                        "tags": [],
                        "device_id": 8,
                        "id": 5,
                        "system_id": "sbfrtx",
                        "used_for": "ext4 formatted filesystem mounted at /",
                        "type": "partition",
                        "path": "/dev/disk/by-dname/sda-part2",
                        "filesystem": {
                            "fstype": "ext4",
                            "label": "root",
                            "uuid": "465f5953-4610-4f58-81f3-19eeabf1b832",
                            "mount_point": "/",
                            "mount_options": null
                        },
                        "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/partition/5"
                    }
                ],
                "id_path": "/dev/disk/by-id/scsi-SQEMU_QEMU_HARDDISK_lxd_root",
                "used_size": 199998046208,
                "type": "physical",
                "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/"
            }
        ],
        "numanode_set": [
            {
                "index": 0,
                "memory": 8320,
                "cores": [
                    0,
                    1,
                    2,
                    3
                ],
                "hugepages_set": []
            }
        ],
        "boot_disk": {
            "firmware_version": "2.5+",
            "numa_node": 0,
            "available_size": 0,
            "used_for": "GPT partitioned with 2 partitions",
            "name": "sda",
            "block_size": 512,
            "path": "/dev/disk/by-dname/sda",
            "filesystem": null,
            "uuid": null,
            "serial": "lxd_root",
            "size": 200000004096,
            "storage_pool": "default",
            "system_id": "sbfrtx",
            "partition_table_type": "GPT",
            "model": "QEMU HARDDISK",
            "tags": [
                "rotary",
                "1rpm"
            ],
            "id": 8,
            "partitions": [
                {
                    "uuid": "477e2c43-7399-4d51-bc7f-c6f7f5239e15",
                    "size": 536870912,
                    "bootable": true,
                    "tags": [],
                    "device_id": 8,
                    "id": 4,
                    "system_id": "sbfrtx",
                    "used_for": "fat32 formatted filesystem mounted at /boot/efi",
                    "type": "partition",
                    "path": "/dev/disk/by-dname/sda-part1",
                    "filesystem": {
                        "fstype": "fat32",
                        "label": "efi",
                        "uuid": "4e55c61b-9526-4610-a796-84d1c09a0909",
                        "mount_point": "/boot/efi",
                        "mount_options": null
                    },
                    "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/partition/4"
                },
                {
                    "uuid": "1a96372d-5e1c-49eb-b986-e6ffdc8a506b",
                    "size": 199455932416,
                    "bootable": false,
                    "tags": [],
                    "device_id": 8,
                    "id": 5,
                    "system_id": "sbfrtx",
                    "used_for": "ext4 formatted filesystem mounted at /",
                    "type": "partition",
                    "path": "/dev/disk/by-dname/sda-part2",
                    "filesystem": {
                        "fstype": "ext4",
                        "label": "root",
                        "uuid": "465f5953-4610-4f58-81f3-19eeabf1b832",
                        "mount_point": "/",
                        "mount_options": null
                    },
                    "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/partition/5"
                }
            ],
            "id_path": "/dev/disk/by-id/scsi-SQEMU_QEMU_HARDDISK_lxd_root",
            "used_size": 199998046208,
            "type": "physical",
            "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/"
        },
        "cache_sets": [],
        "locked": false,
        "cpu_test_status": -1,
        "storage_test_status_name": "Passed",
        "system_id": "sbfrtx",
        "current_installation_result_id": null,
        "memory_test_status": -1,
        "workload_annotations": {},
        "virtualblockdevice_set": [],
        "current_commissioning_result_id": 29,
        "hwe_kernel": null,
        "tag_names": [
            "virtual",
            "pod-console-logging"
        ],
        "interface_set": [
            {
                "params": "",
                "effective_mtu": 1500,
                "vendor": null,
                "interface_speed": 0,
                "parents": [],
                "numa_node": 0,
                "name": "eth0",
                "vlan": {
                    "vid": 0,
                    "mtu": 1500,
                    "dhcp_on": true,
                    "external_dhcp": null,
                    "relay_vlan": null,
                    "id": 5001,
                    "secondary_rack": null,
                    "fabric": "fabric-0",
                    "space": "undefined",
                    "fabric_id": 0,
                    "name": "untagged",
                    "primary_rack": "bfdhyc",
                    "resource_uri": "/MAAS/api/2.0/vlans/5001/"
                },
                "children": [],
                "link_speed": 0,
                "link_connected": true,
                "mac_address": "00:16:3e:f9:ba:58",
                "product": null,
                "system_id": "sbfrtx",
                "enabled": true,
                "links": [
                    {
                        "id": 47,
                        "mode": "auto",
                        "subnet": {
                            "name": "10.16.0.0/24",
                            "description": "",
                            "vlan": {
                                "vid": 0,
                                "mtu": 1500,
                                "dhcp_on": true,
                                "external_dhcp": null,
                                "relay_vlan": null,
                                "id": 5001,
                                "secondary_rack": null,
                                "fabric": "fabric-0",
                                "space": "undefined",
                                "fabric_id": 0,
                                "name": "untagged",
                                "primary_rack": "bfdhyc",
                                "resource_uri": "/MAAS/api/2.0/vlans/5001/"
                            },
                            "cidr": "10.16.0.0/24",
                            "rdns_mode": 2,
                            "gateway_ip": "10.16.0.254",
                            "dns_servers": [],
                            "allow_dns": true,
                            "allow_proxy": true,
                            "active_discovery": false,
                            "managed": true,
                            "disabled_boot_architectures": [],
                            "id": 1,
                            "space": "undefined",
                            "resource_uri": "/MAAS/api/2.0/subnets/1/"
                        }
                    }
                ],
                "discovered": [
                    {
                        "subnet": {
                            "name": "192.168.2.0/24",
                            "description": "",
                            "vlan": {
                                "vid": 0,
                                "mtu": 1500,
                                "dhcp_on": true,
                                "external_dhcp": null,
                                "relay_vlan": null,
                                "id": 5001,
                                "secondary_rack": null,
                                "fabric": "fabric-0",
                                "space": "undefined",
                                "fabric_id": 0,
                                "name": "untagged",
                                "primary_rack": "bfdhyc",
                                "resource_uri": "/MAAS/api/2.0/vlans/5001/"
                            },
                            "cidr": "192.168.2.0/24",
                            "rdns_mode": 2,
                            "gateway_ip": "192.168.2.254",
                            "dns_servers": [],
                            "allow_dns": true,
                            "allow_proxy": true,
                            "active_discovery": false,
                            "managed": true,
                            "disabled_boot_architectures": [],
                            "id": 3,
                            "space": "undefined",
                            "resource_uri": "/MAAS/api/2.0/subnets/3/"
                        },
                        "ip_address": "192.168.2.208"
                    }
                ],
                "firmware_version": null,
                "tags": [],
                "id": 58,
                "sriov_max_vf": 0,
                "type": "physical",
                "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/interfaces/58/"
            }
        ],
        "bios_boot_method": "uefi",
        "testing_status_name": "Passed",
        "network_test_status": -1,
        "zone": {
            "name": "default",
            "description": "",
            "id": 1,
            "resource_uri": "/MAAS/api/2.0/zones/default/"
        },
        "owner": "admin",
        "bcaches": [],
        "raids": [],
        "status_action": "",
        "cpu_speed": 2200,
        "ip_addresses": [
            "192.168.2.208"
        ],
        "description": "",
        "memory": 8320,
        "blockdevice_set": [
            {
                "firmware_version": "2.5+",
                "numa_node": 0,
                "available_size": 0,
                "used_for": "GPT partitioned with 2 partitions",
                "name": "sda",
                "block_size": 512,
                "path": "/dev/disk/by-dname/sda",
                "filesystem": null,
                "uuid": null,
                "serial": "lxd_root",
                "size": 200000004096,
                "storage_pool": "default",
                "system_id": "sbfrtx",
                "partition_table_type": "GPT",
                "model": "QEMU HARDDISK",
                "tags": [
                    "rotary",
                    "1rpm"
                ],
                "id": 8,
                "partitions": [
                    {
                        "uuid": "477e2c43-7399-4d51-bc7f-c6f7f5239e15",
                        "size": 536870912,
                        "bootable": true,
                        "tags": [],
                        "device_id": 8,
                        "id": 4,
                        "system_id": "sbfrtx",
                        "used_for": "fat32 formatted filesystem mounted at /boot/efi",
                        "type": "partition",
                        "path": "/dev/disk/by-dname/sda-part1",
                        "filesystem": {
                            "fstype": "fat32",
                            "label": "efi",
                            "uuid": "4e55c61b-9526-4610-a796-84d1c09a0909",
                            "mount_point": "/boot/efi",
                            "mount_options": null
                        },
                        "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/partition/4"
                    },
                    {
                        "uuid": "1a96372d-5e1c-49eb-b986-e6ffdc8a506b",
                        "size": 199455932416,
                        "bootable": false,
                        "tags": [],
                        "device_id": 8,
                        "id": 5,
                        "system_id": "sbfrtx",
                        "used_for": "ext4 formatted filesystem mounted at /",
                        "type": "partition",
                        "path": "/dev/disk/by-dname/sda-part2",
                        "filesystem": {
                            "fstype": "ext4",
                            "label": "root",
                            "uuid": "465f5953-4610-4f58-81f3-19eeabf1b832",
                            "mount_point": "/",
                            "mount_options": null
                        },
                        "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/partition/5"
                    }
                ],
                "id_path": "/dev/disk/by-id/scsi-SQEMU_QEMU_HARDDISK_lxd_root",
                "used_size": 199998046208,
                "type": "physical",
                "resource_uri": "/MAAS/api/2.0/nodes/sbfrtx/blockdevices/8/"
            }
        ],
        "status_message": "Ready",
        "disable_ipv4": false,
        "power_type": "lxd",
        "node_type_name": "Machine",
        "commissioning_status_name": "Passed",
        "resource_uri": "/MAAS/api/2.0/machines/sbfrtx/"
    },
]
```


## 附录

### 虚拟机参数

#### 可选参数

|       参数       |  类型   |   可选   |                                                                                                   描述                                                                                                    |
| :--------------: | :-----: | :------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|      cores       |   Int   | Optional |                                                                                      The minimum number of CPU cores                                                                                      |
|      memory      |   Int   | Optional |                                                                The minimum amount of memory, specified in MiB (e.g. 2 MiB == 2*1024*1024)                                                                 |
| hugepages_backed | Boolean | Optional |                                                                           Whether to request hugepages backing for the machine                                                                            |
|   pinned_cores   |   Int   | Optional |                                                       List of host CPU cores to pin the VM to. If this is passed, the "cores" parameter is ignored                                                        |
|    cpu_speed     |   Int   | Optional |                                                                                  The minimum CPU speed, specified in MHz                                                                                  |
|   architecture   | String  | Optional |                                                    The architecture of the new machine (e.g. amd64). This must be an architecture the VM host supports                                                    |
|     storage      | String  | Optional | A list of storage constraint identifiers in the form label:size(tag,tag,...), label:size(tag,tag,...). For more information please see the CLI VM host management page of the official MAAS documentation |
|    interfaces    | String  | Optional |      A labeled constraint map associating constraint labels with desired interface properties. MAAS will assign interfaces that match the given interface properties  [标签说参考及说明](#标签列表)       |
|      domain      |   Int   | Optional |                                                                      The ID of the domain in which to put the newly composed machine                                                                      |
|       zone       |   Int   | Optional |                                                                       The ID of the zone in which to put the newly composed machine                                                                       |
|       pool       |   Int   | Optional |                                                                       The ID of the pool in which to put the newly composed machine                                                                       |
|     hostname     | String  | Optional |                                                                                The hostname of the newly composed machine                                                                                 |

#### 标签列表

**Format**: `label:key=value,key=value,...`

**Keys**

    id: Matches an interface with the specific id
    fabric: Matches an interface attached to the specified fabric.
    fabric_class: Matches an interface attached to a fabric with the specified class.
    ip: Matches an interface whose VLAN is on the subnet implied by the given IP address, and allocates the specified IP address for the machine on that interface (if it is available).
    mode: Matches an interface with the specified mode. (Currently, the only supported mode is "unconfigured".)
    name: Matches an interface with the specified name. (For example, "eth0".)
    hostname: Matches an interface attached to the node with the specified hostname.
    subnet: Matches an interface attached to the specified subnet.
    space: Matches an interface attached to the specified space.
    subnet_cidr: Matches an interface attached to the specified subnet CIDR. (For example, "192.168.0.0/24".)
    type: Matches an interface of the specified type. (Valid types: "physical", "vlan", "bond", "bridge", or "unknown".)
    vlan: Matches an interface on the specified VLAN.
    vid: Matches an interface on a VLAN with the specified VID.
    tag: Matches an interface tagged with the specified tag.

### 裸机参数

#### 可选参数

如果不提供则则查询全部，详情查看[maas api 参考文档](https://maas.io/docs/api)

|     参数     |  类型  |   可选   |                                                                  描述                                                                   |
| :----------: | :----: | :------: | :-------------------------------------------------------------------------------------------------------------------------------------: |
|   hostname   | String | Optional | Only nodes relating to the node with the matching hostname will be returned. This can be specified multiple times to see multiple nodes |
|  cpu_count   |  Int   | Optional |                                  Only nodes with the specified minimum number of CPUs will be included                                  |
|     mem      | String | Optional |                              Only nodes with the specified minimum amount of RAM (in MiB) will be included                              |
| mac_address  | String | Optional |                            Only nodes relating to the node owning the specified MAC address will be returned                            | This can be specified multiple times to see multiple nodes |
|      id      | String | Optional |                               Only nodes relating to the nodes with matching system ids will be returned                                |
|    domain    | String | Optional |                                     Only nodes relating to the nodes in the domain will be returned                                     |
|     zone     | String | Optional |                                      Only nodes relating to the nodes in the zone will be returned                                      |
|     pool     | String | Optional |                                            Only nodes belonging to the pool will be returned                                            |
|  agent_name  | String | Optional |                               Only nodes relating to the nodes with matching agent names will be returned                               |
|   fabrics    | String | Optional |                                    Only nodes with interfaces in specified fabrics will be returned                                     |
| not_fabrics  | String | Optional |                                  Only nodes with interfaces not in specified fabrics will be returned                                   |
|    vlans     | String | Optional |                                     Only nodes with interfaces in specified VLANs will be returned                                      |
|  not_vlans   | String | Optional |                                   Only nodes with interfaces not in specified VLANs will be returned                                    |
|   subnets    | String | Optional |                                    Only nodes with interfaces in specified subnets will be returned                                     |
| not_subnets  | String | Optional |                                  Only nodes with interfaces not in specified subnets will be returned                                   |
|  link_speed  | String | Optional |                    Only nodes with interfaces with link speeds greater than or equal to link_speed will be returned                     |
|    status    | String | Optional |                                            Only nodes with specified status will be returned                                            |
|     pod      | String | Optional |                                       Only nodes that belong to a specified pod will be returned                                        |
|   not_pod    | String | Optional |                                    Only nodes that don't belong to a specified pod will be returned                                     |
|   pod_type   | String | Optional |                                 Only nodes that belong to a pod of the specified type will be returned                                  |
| not_pod_type | String | Optional |                                Only nodes that don't belong a pod of the specified type will be returned                                |
|   devices    | String | Optional |      Only return nodes which have one or more devices containing the following constraints in the [标签说参考及说明](#标签列表-1)       |

#### 标签列表

**Format**: `label:key=value,key=value,...`

**Keys**:

    vendor_id: The device vendor id
    product_id: The device product id
    vendor_name: The device vendor name, not case sensative
    product_name: The device product name, not case sensative
    commissioning_driver: The device uses this driver during commissioning

### 相关链接

- [maas api 参考文档](https://maas.io/docs/api)
- [maas go client](https://github.com/maas/gomaasclient)

```go
import (
    gomaasclient "github.com/maas/gomaasclient/client"
)
```