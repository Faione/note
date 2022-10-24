# Helm value

## 将value注入到配置中

[values_files](https://helm.sh/docs/chart_template_guide/values_files/)

## 将文件的内容注入到配置中

[accessing_files](https://helm.sh/docs/chart_template_guide/accessing_files/)

如果文件中有多行，务必需要逐行注入

```yaml
data:
  some-file.txt: {{ range .Files.Lines "foo/bar.txt" }}
    {{ . }}{{ end }}
```