## file commands

[cmake_file_commands](https://cmake.org/cmake/help/latest/command/file.html)

```cmake
# 获取通配符指定的文件，存储到变量Bins中
file(GLOB Bins *.c)

# 获取文件的名称属性，如`NAME`对应不带任何前后缀的文件名称
get_filename_component(target ${Bin} NAME)
```

## loop

```cmake
 foreach(<loop_var> <items>)
   <commands>
 endforeach()
``