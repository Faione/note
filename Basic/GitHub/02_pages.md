# GitHub Pages

github pages可以用来发布静态网页，相比于gitbook, 支持更多样化的网站类型，同时操作简单，只需要在相应的仓库下面开启pages选项即可

github pages通常与github actions配合使用，也可以手动push编译好的网站


## 创建空白分支

```shell
# 创建孤立分支(无头)
$ git checkout --orphan gh-pages

# 删除缓冲区的所有文件
git rm -rf .
```