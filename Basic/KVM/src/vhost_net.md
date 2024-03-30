# vHost Net

使用 virtio net时，数据在 Qemu 与 Guest OS 通过两个环形队列共享，能够一定程度上解决虚拟网卡的性能问题, 但用户态的Qemu在响应到相关的控制信息之后，还需要通过系统调用将数据从用户态拷贝到内核态再进行发送，路径长导致效率低下


vHost Net 是一个内核模块，启用并为虚拟机配置之后，数据相关的传输就不会在用户态发生，而在内核态中进行，避免了频繁的用户态内核态的切换

vHost Net 由多个内核模块组成，核心模块为 `drivers/vhost/net.c` 涵盖了 dev 操作以及通用逻辑，vHost 的实现在 `drivers/vhost/vhost.c` 模块中, 包含 vHost net 的主要逻辑

vHost Net 表现为一个 misc 设备, `vhost_net_fops` 定义了 `file_operations` 操作，打开一个 vHost Net 会触发 `vhost_net_open` 函数，其中会对 `vhost_net`、 `vhost_dev` 等关键结构体进行初始化，并将 `vhost_net` 保存到此task打开的 file 中

Vhost Net 提供一系列 ioctl 接口用于vhost的设置, 正对于 device 本身的 feature 以及 backend、 backend feature 的设置，这部分需要用户态的 Qemu 提供相关的信息并预先进行一些配置， 除此之外， ioctl 中还包含了 `vring` 的相关设置，通过 `vhost_vring_ioctl` 进行分发

`vhost_vring_ioctl` 中除对 `vring` 的基本控制以外，`VHOST_SET_VRING_KICK` 与 `VHOST_SET_VRING_CALL` 定义了关键的通知功能
- `VHOST_SET_VRING_KICK`: 将传入的 eventfd 设置为 `v->kick`, 显然此处传入的应当是 ioeventfd
- `VHOST_SET_VRING_CALL`: 将传入的 eventfd 的 ctx 设置为 `vq->call_ctx.ctx`, 显然此时传入的应当是  irqfd

vhost net 中会初始化两个 virtqueue， 分别用于发送与接收网络数据，两个队列都预先注册了一个 `handle_kick` 回调，vhost net 中的具体实现为 `handle_tx_kick` 与 `handle_rx_kick`, 其中 `handle_tx` 和 `handle_tx` 为关键函数 

最后再根据当前的状态调用 `vhost_poll_start` 对 `v->kick` 进行 poll. vHost net 中有两个 handle kick 的回调 `handle_tx_kick` 与 `handle_rx_kick`, 分别由 Guest OS 和 Tun 设备进行触发，对应Guest OS发送数据，与 Tun 设备回写数据。

同时注意到，virtqueue实际上保存在 vHost dev 结构体中，而初始化 virtqueue 所依赖的 eventfd 均来自于 vhost.c 模块中的 ioctl 函数。即 vHost dev 完成了 kick 操作的注册，这些kick回调保存在vq对应的 vhost_poll事件中。

而 vHost net 结构体中还额外有两个 vhost_poll 事件，分别注册了 `handle_tx_net` 与 `handle_rx_net` 两个回调，这两个函数同样会调用 `handle_xx` 方法进行网络包的发送与读取，区别在于 vhost net 中的 vhost_poll 事件仅由 tun 设备的 sock 触发，其中 `handle_tx_net` 是当 sock 可写时触发，而 `handle_rx_net` 当 sock 可读时触发。这些事件的发生在 `handle_xx` 的处理中， 并通过 `vhost_net_enable_vq` 与 `vhost_net_disable_vq` 来管理 poll 事件的在 tun sock 的注册

## 发送数据

guest os 中virio驱动数据准备好后，就退出虚拟机执行，由kvm write event 来 kick 唤起poll wait事件，即唤醒一个 vhost worker 内核线程，执行 `handle_tx_kick` 回调，并在 `handl_tx` 进行发送处理，过程中会循环进行包的发送，正常情况下包发送完毕后 `handle_tx_kick` 就会返回，而如果过程中 tun 设备出现了繁忙，则会注册 vhost 上的 tx vhost_poll 事件，并调用 `vhost_net_enable_vq` 注册回调 vhost_poll，然后提前返回，worker 中会调用 schedule 让出CPU资源

这种情况下，如果一段时间后 tun 设备不再繁忙，则会触发回调，并唤起 worker 执行 `handle_tx_net`, 当然如果worker此时并未休眠，则也可以是 worker 读取到下一个 vhost poll work 并调用`handle_tx_net`回调