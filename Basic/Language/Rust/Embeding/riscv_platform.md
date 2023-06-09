# Rust On Risc-V Linux Platform

## Tools

|         Tool          | Version |
| :-------------------: | :-----: |
|         cargo         | 1.66.0  |
|         rustc         | 1.66.0  |
|        rustup         | 1.25.1  |
| riscv64-linux-gnu-gcc | 12.2.0  |

## Cross-compiling Env

preparing cross-compiling environment, we need addition compiler-backend for  riscv64-linux-platform, just:

```shell
rustup target add riscv64gc-unknown-linux-gnu

# see what we have installed
rustup target list
```

normally we could use cargo flags like `--target` to set compiling args, but the best way is to add a cargo config file

```toml
# .cargo/config
[build]
target = "riscv64gc-unknown-linux-gnu"
rustflags = ["-C", "target-feature=+crt-static"]

[target.riscv64gc-unknown-linux-gnu]
# using riscv toolchains 
linker = "riscv64-linux-gnu-gcc"
```

we set our target to "riscv64gc-unknown-linux-gnu" [^1], and using riscv toolchains [^2]. rust-analysis may not work fine, and we should add some configs in `.vscode/setting.json`.

```json
{
    "rust-analyzer.check.allTargets": false,
    "rust-analyzer.check.extraArgs": [
        "--target",
        "riscv64gc-unknown-linux-gnu"
    ]
}
```


after above, now we can compile rust code to riscv_platform, just try it!






[^1]: https://doc.rust-lang.org/nightly/rustc/platform-support.html

[^2]: https://stackoverflow.com/questions/64308644/rust-unable-to-build-64-bit-risc-v-binary

