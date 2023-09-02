# Ethernet

`ethtool -i eno0`


```
driver: st_gmac
version: 6.2.0-19-generic
firmware-version: 
expansion-rom-version: 
bus-info: 16030000.ethernet
supports-statistics: yes
supports-test: no
supports-eeprom-access: no
supports-register-dump: yes
supports-priv-flags: no
```

## Static IP on Debian

```
auto end0
iface end0 inet static
address 10.30.5.121
netmask 255.255.224.0
gateway 10.30.0.254
```

## SoftAp by ESWIN 6600U

### Basic

查看 usb 网卡, 为 `ESWIN 6600U`

```
$ lsusb
> Bus 001 Device 007: ID 3452:6600 ESWIN 6600U
```

安装相关软件工具
- `iptables`: 设置路由规则，如包转发，Nat等
- `hostapd`: softAp工具，允许无线网卡以AP的模式运行，并进行相关参数的配置
- `dnsmasq`: 类似dhcpd的 dns & dhcp 工具，相对更轻量，适用于小型网络

```
$ apt install iptables hostapd dnsmasq
```

### Set Up

通过 ap 模式启动无线网卡，并设置 dhcp 服务为接入设备分配ip地址，end0网卡连接外网，通过 iptables 设置 Nat 规则，使得连接ap的设备能够访问外部网络 [^1]

#### wlan配置

wlan interface 作为router，配置ip网段即可

```
# /etc/network/interfaces
auto wlx2c0547a11bf8
iface wlx2c0547a11bf8 inet static
address 192.168.5.1
netmask 255.255.255.0
```

#### hostapd配置

参考已有配置[^2]
- wifi名称，密码等信息

```shell
$ sudo hostapd /etc/hostapd/hostapd.conf -B
```

```shell
$ vim /etc/hostapd/hostapd.conf

interface=wlx2c0547a11bf8 // set to the exact wlan interface
logger_syslog=-1
logger_syslog_level=2
logger_stdout=-1
logger_stdout_level=2

ssid=fhlrouter // name of the wifi
country_code=FR
ieee80211d=1
hw_mode=g
channel=11
beacon_int=100
dtim_period=2
max_num_sta=255
rts_threshold=-1
fragm_threshold=-1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wmm_enabled=1
wmm_ac_bk_cwmin=4
wmm_ac_bk_cwmax=10
wmm_ac_bk_aifs=7
wmm_ac_bk_txop_limit=0
wmm_ac_bk_acm=0
wmm_ac_be_aifs=3
wmm_ac_be_cwmin=4
wmm_ac_be_cwmax=10
wmm_ac_be_txop_limit=0
wmm_ac_be_acm=0
wmm_ac_vi_aifs=2
wmm_ac_vi_cwmin=3
wmm_ac_vi_cwmax=4
wmm_ac_vi_txop_limit=94
wmm_ac_vi_acm=0
wmm_ac_vo_aifs=2
wmm_ac_vo_cwmin=2
wmm_ac_vo_cwmax=3
wmm_ac_vo_txop_limit=47
wmm_ac_vo_acm=0
ieee80211n=1
ieee80211ac=1
eapol_version=2
eapol_key_index_workaround=0
eap_server=0
own_ip_addr=127.0.0.1
wpa=2
wpa_passphrase=12345667 // passwd of the wifi
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
```

#### dnsmasq配置

`dnsmasq` 安装之后以service模式接入到systemd中启动, 默认配置在 `/etc/dnsmasq.conf` 中

```
interface=wlx2c0547a11bf8
listen-address=192.168.5.1
dhcp-range=192.168.5.50,192.168.5.150,1m
server=/google/8.8.8.8
```

#### iptables配置

默认情况下，iptables 软连接到 nftables，而visionfive2尚不支持，因此需要修改为 legacy 实现

```shell
$ update-alternatives --set iptables /usr/sbin/iptables-legacy
$ update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
```

通过 hostapd 及 dnsmasq 已经能够构成无线局域网，因此只需设置流量转发以及Nat规则即可实现外网访问

```shell
# 允许 ipv4 流量转发
$ sysctl -w net.ipv4.ip_forward=1
```

配置Nat

```shell
$ iptables -t nat -A POSTROUTING -s 192.168.5.0/24 ! -o wlx2c0547a11bf8 -j MASQUERADE
```

#### TODO

- [ ] 一键配置脚本
- [ ] cpu freq 调度策略
- [ ] 优化的网络配置方案

[^1]: [ap配置](https://www.361way.com/hostapd-soft-ap/2933.html)
[^2]: [usb-module-eswin-6600u](https://forum.rvspace.org/t/usb-module-eswin-6600u/979/17)