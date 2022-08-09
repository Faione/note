# Yaml 配置文件

## 特殊符号

- `|` 保留文本每行尾部的换行符，而 `>` 则会将所有的换行符视为空格
  - 当 value 为多行文本时

```
include_newlines: |
            exactly as you see
            will appear these three
            lines of poetry

fold_newlines: >
            this is really a
            single line of text
            despite appearances
```

- `|+` 在保留文本每行尾部的换行符的同时，还保留结尾行的换行符
- `|-` 在保留文本每行尾部的换行符的同时，去除结尾行的换行符