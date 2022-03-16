# Helm

- [helm官方文档](https://helm.sh/zh/docs/)
- [helm go client](https://manuelmazzuola.dev/2021/03/28/deploy-helm-chart-go#the-helm-go-sdk)

## What is Helm

- helm是k8s的包管理工具
  - helm管理的包即是 chart，本质上是一个模板文件的组合，用来对要部署的k8s资源进行描述，以及一个用于评估的值文件

> Helm installs charts into Kubernetes, creating a new release for each installation. And to find new charts, you can search Helm chart repositories