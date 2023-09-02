# sed-basic

- [修改文件的某一行](https://www.cnblogs.com/azureology/p/13039573.html)

```shell
# 修改 hello.c 的第5行为 "printf($1);"
$ sed -i "5c printf($1);" hello.c
```

```shell
$ sed -i -e "s/{AGENT_GUID}/${guid}/g" $root_dir/docker-compose.yaml
```