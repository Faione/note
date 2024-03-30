# OpenRC

openrc是alpine linux中默认采用的轻量级init系统。OpenRC的核心部分处理依赖管理和init脚本分析。OpenRC通过扫描运行级别，建造依赖图，接着启动需要的服务脚本来工作。一旦脚本都已经启动它就退出。缺省的，OpenRC使用一个修改版本的start-stop-daemon用于守护进程管理

## Service Script

openrc中的init脚本采用shell语法，具体配置[openrc_service_script_guide](https://github.com/OpenRC/openrc/blob/master/service-script-guide.md)

```shell
#!/sbin/openrc-run

description="Mount control zone image repo"

tag="hostshare"
mountp="/mnt"

depend() {
    # localmount 与 bootmisc 都是定义在 /etc/init.d/ 中的脚本，即当是当前脚本需要启动的前置脚本 
    need localmount 
    after bootmisc
}

start() {
    ebegin "Mounting cz image repo"

    mount -t 9p -o trans=virtio,version=9p2000.L $tag $mountp
    if [ $? -eq 0 ]; then
        cat $mountp/configs/storage.conf > /etc/containers/storage.conf
    else
        echo "image repo mount failed for tag: $tag, mountp: $mountp"
    fi

    eend $?
}

stop() {
    ebegin "Unmounting cz image repo"
    
    if [ -e $mountp/configs/def.storage.conf ]; then
        cat $mountp/configs/def.storage.conf > /etc/containers/storage.conf
    fi

    umount $mountp
    
    eend $?
}
```