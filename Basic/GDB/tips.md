

1. auto-loading

gdb 导入可执行文件 `bin` 时，会寻找 `{bin}-gdb.py` 脚本并自动导入
- 前提是在 `~/.config/gdb/gdbinit` 中设置了 `set auto-load safe-path {path}`

[gdb_python_auto_loading](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-Auto_002dloading.html)