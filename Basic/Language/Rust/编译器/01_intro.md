# Rust Compiler

## Brief to Compiler

### Lexing and parsing

rust 原始代码文本首先通过 rustc_lexer 中的一个 low-lever lexer 进行分析。在这个阶段，源码文本将会被转化为被称为 `tokens` 的原子源码单元流

[lexing-and-parsing](https://rustc-dev-guide.rust-lang.org/the-parser.html#lexing-and-parsing)

编译器所做的第一件事情就是将程序(Unicode 编码)转化为对编译器来说比字符串更方便的形式，而这需要通两个阶段完成: Lexing and Parsing

Lexing 以字符串为输入，并将他们转化为 tokens 流, 如 `a.b + c` 将被转化为 `a, ., b, + , c`

Parsing 随后取得 tokens 流，并将他们转化为对编译器而言更方便理解的结构化形式，这种形式通常被称为 AST(Abstract syntax tree), AST 在内存中反应出 rust 代码的结构，并使用 `Span` 来将特定的AST链接回原始文本(即某AST对应原始文本的那些部分)