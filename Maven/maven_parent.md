# Maven 父子工程
[参考](https://blog.csdn.net/a1103313049/article/details/107221812)  
[Maven继承参考](https://blog.csdn.net/qq_32224047/article/details/107416990)
[Maven父子工程依赖管理](https://www.cnblogs.com/alice-cj/p/11442228.html)
## 一、基础概念  
maven是依赖管理的工具，因而绝大多数pom的配置，都与依赖有关  
使用maven父子工程时，父子工程的依赖仍然相互独立，即子工程不能直接使用父工程中的依赖，除非自己也引入

- 依赖版本管理
idea中，以module为粒度区分不同的project，同一个project中，可以有多个module  
其中，父module中使用 \<dependencyManagement\> 声明的依赖，子module中可不声明版本地使用  
使用\<dependencies\>声明的依赖，子module可直接引用  
因而，可以利用父子工程，对多个子module的依赖版本进行管理 
   > 这也是为什么parent为spring framework的工程，不必在dependence中声明依赖版本的原因

- 子模块调用
同时，子module可以相互以maven本地库的方式引入，以进行相互之间的方法调用

- 父子工程的编译
选择父工程的 maven 进行 package，则会将所有关连的子module进行编译，产生多个jar包

## 二、构建父子工程
### (1) 创建父工程  
需要明确，父工程不承担业务，仅进行管理，因而不需要src目录，同时注意到父工程没有src目录，因而编译时也无需打包成jar包，所以在pom文件中，需要加入
```xml
<!--如不填写，则idea会提示错误，并要求修改为pom-->
<packaging>pom</packaging>
```

### (2) 创建子工程
以module的方式创建子工程，可以选择maven的方式，此时idea会帮助生成父子工程的关联关系，否正则需要进一步在pom文件中进行配置

### (3) 关联父子工程  
首先，父工程需要知道子工程的存在，在其pom文件中添加
```xml
<modules>
    <module>agent-service</module>
    <module>controller-service</module>
    <module>reporter-service</module>
</modules>
```

同时，子工程也需要关联父工程
```xml
<parent>
    <artifactId>agent-cloud</artifactId>
    <groupId>org.example</groupId>
    <version>1.0-SNAPSHOT</version>
</parent>
```

## 三、依赖的调用  
- 父工程中引入的依赖，子工程可以不书写版本的引入  
- 不同的子工程，可以通过 dependency的方式进行引入
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>controller-service</artifactId>
    <version>0.0.1-SNAPSHOT</version>
</dependency>
```