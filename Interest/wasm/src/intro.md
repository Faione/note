# intro

[concepts]
- [rust wasm](https://rustwasm.github.io/docs/book/)
- [wasi](https://wasi.dev/)

[wasm-tools]
- [wasm-pack](https://rustwasm.github.io/wasm-pack/book)
- [wasm-shell](https://docs.wasmer.io/ecosystem/webassembly.sh)

[wasm-crate]
- [wasm-bindgen](https://rustwasm.github.io/docs/wasm-bindgen/introduction.html)

[wasm-runtimes](https://github.com/appcypher/awesome-wasm-runtimes)
- [wasmer](https://wasmer.io/)
- [wasmtime](https://docs.wasmtime.dev/)




如果您想了解WebAssembly虚拟机，可以参考以下几个资源：

1.WebAssembly规范：https://webassembly.github.io/spec/

2.WebAssembly开发者指南：https://developer.mozilla.org/zh-CN/docs/WebAssembly

3.WebAssembly样例库：https://webassembly.org/demo/

4.WebAssembly学习资源：https://webassembly.org/getting-started/developers-guide/

5.WebAssembly虚拟机实现：https://github.com/WebAssembly/wasm-js-api

6.WebAssembly虚拟机白皮书：https://webassembly.org/docs/wasm-vm-for-dummies/


## WASM虚拟机

Wasm 是 WebAssembly 的简称，它是一种新的跨平台、轻量级的二进制编码格式，旨在提供一个可移植、高效的方式来在网页上运行高性能的应用程序。Wasm 栈式虚拟机是一种用于执行 Wasm 代码的虚拟机，它的工作方式类似于其他语言的栈式虚拟机，例如 Java 虚拟机或 .NET Common Language Runtime（CLR）。

栈式虚拟机通常由两部分组成：一个执行引擎和一个内存管理器。执行引擎负责读取二进制代码并执行它，而内存管理器负责维护内存并确保代码正确地访问内存。

在 Wasm 栈式虚拟机中，执行引擎通常使用一个基于栈的指令集来执行 Wasm 二进制代码。这些指令操作码（opcodes）的执行方式类似于现代计算机的指令集，但通常更简单、更小。执行引擎会按顺序读取每条指令，并根据指令的类型执行相应的操作。例如，一条加法指令可能会从栈中弹出两个数字，将它们相加，并将结果压入栈中。


在 Wasm 栈式虚拟机中，内存管理器负责维护内存并确保 Wasm 代码正确地访问内存。这通常是通过在执行引擎和内存之间建立一个抽象层来实现的，该抽象层负责管理内存并处理内存访问请求。

为了实现动态内存分配，内存管理器通常会使用一些算法来分配和回收内存。例如，可以使用垃圾回收算法来自动清理不再使用的内存，或使用内存池来预先分配一定量的内存并动态地分配给 Wasm 代码使用。

总的来说，Wasm 栈式虚拟机是一种执行 Wasm 代码的平台，它通过执行引擎和内存管理器来实现 Wasm 代码的执行和内存管理。这样的虚拟机能够提供一个可移植、高效的运行环境，使 Wasm 代码能够在不同平台上运行。

## WASM 编译

Wasm（WebAssembly）是一种新的跨平台、轻量级的二进制编码格式，旨在提供一个可移植、高效的方式来在网页上运行高性能的应用程序。Wasm 的编译流程一般包括如下几个步骤：

1. 预处理：在编译之前，首先会对源代码进行预处理，这一步主要是对代码进行词法分析、语法分析和语义分析。这一步的目的是将源代码转换成一种中间表示，以便后续的编译步骤能够更容易地处理代码。

2. 优化：在预处理完成后，编译器会进行优化处理，这一步的目的是提高代码的性能。编译器会执行一些常见的优化技术，例如代码重排、常量传播、消除冗余代码等，以便提高代码的执行效率。

3. 目标代码生成：在优化完成后，编译器会根据优化后的中间表示生成目标代码。目标代码通常是一种特定的机器语言，例如 x86 指令集、ARM 指令集等。这一步的目的是将源代码转换成可以在特定平台上执行的代码。

4. 汇编：在目标代码生成完成后，编译器会在目标代码生成完成后，编译器会将目标代码转换成机器语言指令的二进制表示。这一步通常称为汇编（assembly）。汇编器会将目标代码中的每条指令转换成一个或多个机器语言指令的二进制形式，并将它们连接起来生成最终的二进制文件.

5. 链接：最后，编译器会将生成的二进制文件连接起来，以便在实际运行时能够顺利加载和执行。连接阶段会检查代码中的各种引用，并将它们链接到实际的目标代码上。这一步完成后，编译器会输出最终的可执行文件，供用户使用。

总的来说，Wasm 编译流程包括预处理、优化、目标代码生成、汇编和链接五个步骤。每个步骤都是为了提高代码的性能和可执行性，并将源代码转换成可以在特定平台上运行的代码