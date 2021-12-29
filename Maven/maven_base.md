# Maven
[maven仓库地址](https://mvnrepository.com/)

## 一. 配置本地maven
[本地maven配置](https://blog.csdn.net/liu_shi_jun/article/details/78733633)
### 1. 安装maven  
[下载maven](http://maven.apache.org/)
### 2. 配置环境变量
- 运行环境：java
- java 环境配置：
   - 下载jdk：jre ∈ jdk，jre是java程序的运行时环境，而jdk同时还提供开发工具
   - 环境配置：
       - JAVA_HOME: jdk目录
       - Path: %JAVA_HOME%/bin, %JAVA_HOME%/jre/bin， 前者为开发工具（如javac编译工具），后者为   运行时环境
       - Classpath：.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar， 标识jvm载入时的路径
       > ？jdk5之后不必再配置
  - maven 环境配置：
     - Mavnen_HOME: maven所在目录
     - Path: %Mavnen_HOME%/bin
      
```shell
# 查看是否配置成功
mvn -v
```
### 3. 自定义maven  
修改配置文件: \conf\setting.xml
```xml
  <localRepository>‪E:\MavenRepository</localRepository>
```

```shell
# 检查是否配置成功
mvn help:system
```

### 4. 导入ide工具

建议使用ide自带maven，修改仓库地址到其他路径即可
