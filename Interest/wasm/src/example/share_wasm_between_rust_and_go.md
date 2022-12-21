# share wasm between rust and go

目标:
- 使用 rust 编写程序, 并编译为 wasm
- 使用 wasmer 调用 wasm
  - 在 rust 中调用
  - 在 go 中调用

项目树

```
├── Cargo.lock
├── Cargo.toml
├── test-wasm // wasm package
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── test-wasm-user // rust user app package
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── test-wasm-user-go // go user app package
    ├── go.mod
    ├── go.sum
    └── main.go
```

## wasm

wasm 项目配置

TODO: ? crate-type, ? wasm-bindgen

```ini
# Cargo.toml
...

[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2.83"
```

为方法添加 `#[wasm_bindgen]` 标记

```rust
// test-wasm/src/lib.rs

use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn add(left: u32, right: u32) -> u32 {
    left + right
}
```

编译 rust 代码为 wasm

```shell
$ cargo wasi build -p test-wasm --release 
```

## Wasm in Rust

增加依赖 `wasmer = "3.0"`

```ini
[dependencies]
wasmer = "3.0"
```

在用户程序中, 使用 `wasmer` 提供的 wasm 运行时来执行 wasm 程序

```rust {.line-numbers}
use wasmer::{imports, Instance, Module, Store, TypedFunction};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let wasm_bytes = std::fs::read("target/wasm32-wasi/release/test_wasm.wasm")?;
    let mut store = Store::default();
    let module = Module::new(&store, wasm_bytes)?;

    let imports = imports! {};
    let instance = Instance::new(&mut store, &module, &imports)?;

    let add: TypedFunction<(u32, u32), u32> =
        instance.exports.get_function("add")?.typed(&mut store)?;

    let result = add.call(&mut store, 1, 2)?;
    assert_eq!(result, 3);

    println!("Results of `add_one`: {:?}", result);

    Ok(())
}
```

- 代码第 1 行首先从 `.wasm` 文件中读取 wasm 字节码
- 代码第 5~6 行则初始化 wasm 引擎
- 代码第 8~9 行构造 wasm 实例
- 代码第 11~14 行则从实例中获取要执行的方法, 并执行


## Wasm in Go

在 go 代码中引用 `github.com/wasmerio/wasmer-go/wasmer` 执行引擎

```go {.line-numbers}
func main() {
	wasmBytes, err := os.ReadFile("../target/wasm32-wasi/release/test_wasm.wasm")
	if err != nil {
		log.Fatal(err)
	}

	engine := wasmer.NewEngine()
	store := wasmer.NewStore(engine)
	module, err := wasmer.NewModule(store, wasmBytes)
	if err != nil {
		log.Fatal(err)
	}

	importObject := wasmer.NewImportObject()
	instance, err := wasmer.NewInstance(module, importObject)
	if err != nil {
		log.Fatal(err)
	}

	addOne, err := instance.Exports.GetFunction("add")
	if err != nil {
		log.Fatal(err)
	}

	rlt, err := addOne(1, 2)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("result is: ", rlt)
}
```