# Env

类似于 shell, uboot shell 也支持环境变量, 使用方法与 shell 中类似, 通过 `setenv k v` 进行设置
- 存在特殊字符时, 使用 `'` 或 `"` 将 value 包含进去
- 可以使用 `;` 将多个命令包含在一起
- 如果 `v` 为空, 则会将环境变量删除


`printenv` 将打印所有的环境变量, `printenv k` 将打印 `k=v`, 使用 `echo $k` 也可以打印变量, 与在 shell 中的使用方法类似

`saveenv` 将会把所有的环境变量写入到 `SPI flash` 中, 使得下次重启时, 能获得之前保存的环境变量