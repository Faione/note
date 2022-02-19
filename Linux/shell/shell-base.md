# Shell Base


## 运行
./并非是执行，而是告诉bash，要执行的文件在 ./ 当前目录下
## 循环
while ((condittion))
do
loop()
done

## 输入输出
<name>=$1 进行赋值

let <name>=2 改变值

/$NF 最后一个参数


## 解压缩文件

```shell
# 解压
# -C 指定目录
tar -zxvf /tmp/etc.tar.gz -C /etc
# 压缩
tar -zcvf FileName.tar.gz DirName
```


## nohub
[nohub](https://www.runoob.com/linux/linux-comm-nohup.html)

nohup /root/runoob.sh &

## profile

向 /etc/profile 中添加环境变量，使得所有shell都能使用

## 

~ 为家目录
$HOME 为家目录的环境变量