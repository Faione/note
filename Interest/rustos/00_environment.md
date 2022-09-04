# 环境配置

- [tutorial](http://rcore-os.cn/rCore-Tutorial-Book-v3/)
- [2022训练营](https://learningos.github.io/rust-based-os-comp2022/)
- [guidence](https://github.com/LearningOS/rCore-Tutorial-Code-2022S)
- [blogos](https://os.phil-opp.com/freestanding-rust-binary/)


**RiscV**

- [guidence](https://github.com/riscv-non-isa/riscv-asm-manual/blob/master/riscv-asm.md)
- [参考](https://riscv.org/wp-content/)


- 解决vscode rust报错`can't find crate for `test``
  - [](https://www.cnblogs.com/dou-fu-gan/p/15870905.html)

- 当前工作区中增加配置

```json
{
	"rust-analyzer.checkOnSave.allTargets": false,
	"rust-analyzer.checkOnSave.extraArgs": [
			"--target",
			"riscv64gc-unknown-none-elf"
	]
}
```