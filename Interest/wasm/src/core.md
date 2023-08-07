# Wasm Spec

Wasm Spec[^1] 包含了一系列与Wasm相关的规范文档, 其中Core文档[^2]定义了Wasm的核心内容，包括
- instruction set (指令集)
- binary encoding (字节码)
- validation (验证)
- execution semantics (执行语义)
- textual representation (文法)

Core文档说明了Wasm的原理，但并不包含执行Wasm环境的定义，而这一部分被称为 WebAssembly application programming interface 或 Embedding interfaces:
- JS API: 定义了一套在JS中操作wasm的接口
- Web API: 定义了适应 JS API 的扩展
- WASI API: 定义了在 Web 之外运行 Wasm 的模块化系统接口

WASI[^3] 仅作为运行wasm的一揽子接口定义，而基于此接口则由 wasmer, wasmruntime 等一系列用不同语言实现的runtime

换而言之， 如wasmer等Runtime依据Core文档定义的WASM执行原理实现了WASI接口，而在其他语言中，可以通过WASI接口即可以将WASM代码交由Runtime执行

[^1]: [wasm_spec](https://webassembly.org/specs/)
[^2]: [wasm_core](https://webassembly.github.io/spec/core/intro/index.html)
[^3]: [wasm_system_interface](https://github.com/WebAssembly/WASI)

## WASM Core

