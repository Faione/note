# Cobra

## 一、基础

### (1) Cobra

cobra是一个命令行程序库，可以用来编写命令行程序，同时也提供了一个脚手架，用于生成基于cobra的应用程序框架

### (2) 命令结构

Cobra命令结构由三部分组成: 命令 (commands)、参数 (arguments)、标志 (flags)
   - commands 代表行为，是应用的中心点
   - arguments 代表行为作用的对象
   - flags 是行为的修饰符

```shell
$ git clone URL --bare
```
- git: 程序名称
   - shell会从当前的PATH环境变量中寻找 git 二进制文件, 之后的作为参数传入 
- clone: 命令
- URL: 参数, 命令 clone 作用的对象
- --bare: 标志

### (3) cobra工具

cobra工具: 协助进行快速方便的CLI App构建
   - 初始化app架子
   - 提供快速增加样版代码的命令, 如增加子命令
   - [安装 cobra 工具](https://github.com/spf13/cobra/blob/master/cobra/README.md)

## 二、Cobra库

### (1) 基础使用

```go
// 构造一条命令
test := &cobra.Command{
   Use:   "test", // 一行的使用说明信息, 其中，首个单词作为 命令, 也可以使用 Aliases 增加别名
   Short: " test",
   Long:  ` a demo to test cobra`, // ``包裹的字符串不进行转义，效率更高
   RunE: func(cmd *cobra.Command, args []string) error { // 命令执行时触发的函数，args为命令传入的参数
      return rootInfo(name, args)
   },
   TraverseChildren: true, // 如果不加此设置，则挂载子命令后，根命令后的参数会认为是子命令，导致无法识别
}

// 执行一条命令

if err := test.Execute(); err != nil { // 如果存在字命令，若输入符合，也会在此处执行，显然，无参数的情况下(直接执行)，默认执行的就是第一个创建的命令
   fmt.Fprintln(os.Stderr, err)
   os.Exit(1)
}

```

### (2) 使用Cobra构建CLi

构建方式, 根命令可以挂载多个子命令，挂载在最低一层使用统一挂载，分别实现的方式，而更高的层次(无业务逻辑)，只挂钩子并进行说明
main中构建根命令, 并执行, 子命令构造函数中以根命令作为参数输入(指针), 

