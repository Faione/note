# Kernel Module

## Env

使用 bear -- <make cmd> 生成编译信息，指导 clangd 正确地获取头文件等信息

## Tasks

通过 `init_struct` 就可以拿到init进程的 task_struct, 通过 `get_current()` 可以拿到当前cpu上运行的进程的 task_struct

在 task_struct 中， 存在 `children` 与 `sibling` 两个链表头，分别指向 child / sibling task_struct 中的相同位置，从而能够通过 `list_for_each_entry` 进行遍历

```c
// list 宏实际展开为一个循环，其中 pos 会被赋值为每次遍历到的 entry 的指针， head 则是链表头的指针
// member 则告知了每次循环时所要遍历的 list head 对应在 entry 中的成员变量名
#define list_for_each_entry(pos, head, member)


// 以 &(&init_task)->children 为头，遍历 init_task 子 task_struct 中的 sibling， 即所有的子 task_struct
list_for_each_entry(task, &(&init_task)->children, sibling)
```