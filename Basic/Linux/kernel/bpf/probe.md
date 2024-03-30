# Probe

[ebpf_动态观测](https://fuweid.com/post/2022-bpf-kprobe-fentry-poke/)

eBPF 中可以通过 kprobe/fentry 实现对内核函数的观测
- 内核通过增加`-mfentry`编译选项，在每个函数的入口处增加一个埋点
- 内核链接时，将此埋点替换为一个 nop5 指令，以保证运行性能
- 当BPF程序加载时，此空指令会被替换一个 neal call 指令，跳转到BPF trampoline，trampoline会准备好相应的参数
- trampoline中再找到注册的fentry BPF函数并执行

