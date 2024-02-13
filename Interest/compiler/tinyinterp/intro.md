# TinyInterpreter

解释器/编译器工作通常分为以下几个阶段, 每个阶段都依赖上一个阶段的输出

## 词法分析

### token

代码中每个有意义的符号, 都可以保存到一个 token 中, 并在其中标注其类型, 或保存值

```
foo = 123
```

其中有3个符号 `foo`, `=`, `123`, 其中 `foo` 是变量, `=` 是操作符, `123` 是数值

读入代码文件之后, 可以依次对每个符号进行收集, 从而能够形成一个 token 流

### 符号表

符号表中保存了变量的各种信息, 这些变量类型包括 Num（数值）, Char（字符）, Str（字符串）, Array（数组）, Func（函数）

### 作用域

作用域及变量有效的区域, 如函数中的局部变量与函数外的全局变量, 可以通过一个 `currentlevel` 来标记当前的嵌套深度, 以便在进入/退出时进行变量的回收

## 语法分析

即按照一定的语法来组织token, 从而构成一个 抽象语法树. 语法分析依赖相关的理论

BNF: `Backus-Naur` 符号是描述语言的形式化的数学方法, 可以认为是描述某种语言的范式(Form). 如下定义了3种基本符号 `<expression>` `<term>` `<factor>`, 而符号本身可由推导式右边的产生式构成

```
<expression> ::= <term> | <expression> "+" <term> | <expression> "-" <term>
<term>       ::= <factor> | <term> "*" <factor> | <term> "/" <factor>
<factor>     ::= <number> | "(" <expression> ")"
<number>     ::= [0-9]+
```

EBNF: 是BNF的一种扩展, 主要对BNF中常见的两种情况，即重复项和可选项添加了相应的语法规则，如用方括号 `[ …. ]` 表示可选部分，用花括号 `{ … }` 表示重复出现的部分


> 非终结符是可以再被分解的符号, 而终结符是不可以再被分解的符号

> 左递归问题: 某个非终结符在产生式的第一个符号或者多个符号中包含自身的情况, 这导致如使用递归下降文法时出现无限递归的问题

递归下降文法: 基本思想是将每个非终结符定义为一个对应的函数，然后在该函数中根据当前的输入符号逐步匹配所需的产生式、调用其他的函数来完成更深层次的分析、以及生成对应的语法树或 AST（抽象语法树）等结果.递归下降文法的优点是简单直观、易于理解和实现，并且能够组合多个语法规则进行分析。缺点是容易出现无限循环和回溯等问题，导致效率较低，并且不适用于所有类型的文法，特别是存在左递归的情况下

分析逻辑
- 基于EBNF文法定义语言, 如四则表达式与布尔运算
- 按照递归下降的思想进行实现


四则运算
```
exp -> term { addop term }
term -> factor { mulop factor }
factor -> number | ( exp )
addop -> + | -
mulop -> * | /
```

布尔运算
```
boolop -> > | < | >= | <= | ==
boolexp -> exp boolop exp | (boolOR) | !boolexp
boolAND -> boolexp  { '&&' boolexp }
boolOR -> boolAND { '||' boolAND}
```

声明
```
statement -> '{' { statement } '}'                                   |       // 语句块
            if-stmt -> if ( exp ) statement [ else statement ]       |       // 选择语句
            while-stmt -> while ( exp ) statement                    |       // 循环语句
            Sym = exp;                                               |       // 赋值语句
            print ( exp );                                           |       // 输入输出语句
            puts ( Str );                                            |
            read ( Sym );                                            |
            return ( exp );                                          |       // 函数的返回语句
            func func_name statement;                                |       // 函数定义    
            array array_name length;                                 |
            func_name;                                               |       // 函数调用
```

## 语义分析