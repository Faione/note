# How Program Get Run

[how_program_get_run](https://lwn.net/Articles/630727/)

## execve族系统调用

Linux内核侧程序的运行在 execve族系统调用 中完成
- [`execve()`](https://man7.org/linux/man-pages/man2/execve.2.html): 标准的程序执行系统调用，根据传入的程序路径执行程序
- [`fexecve()`](https://man7.org/linux/man-pages/man3/fexecve.3.html): 使用fd而不是路径，使用更加灵活
- [`execveat()`](https://man7.org/linux/man-pages/man2/execveat.2.html): 允许传入 dirfd, 从而能够在指定的目录下，使用相对路径寻找要执行的程序