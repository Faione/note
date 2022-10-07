## CronJob

- [k8s cronjob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)

CronJobs用于执行定期计划的操作，如进行备份，生成报告等。这些任务都被设置为在长时间内重复执行，并可被定义在时间间隔之内，任务开始的时间点


```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox:1.28
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

### 定时调度语法

CronJob使用一个5元数组来进行定时，所支持的最小粒度为分钟，`* * * * *` 表示每分钟都会调度一次
- `*` 为通配，表示任意取值
- CronJob会在符合定时标识符的时刻，进行任务的调度

```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │                                   OR sun, mon, tue, wed, thu, fri, sat
# │ │ │ │ │
# * * * * *
```

### 定时任务的局限性

CronJob每次被调度时，都会创建大约一个job对象(某些情况下会创建多个，或者一个都不创建)