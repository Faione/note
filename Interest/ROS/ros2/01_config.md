# Config ROS2


- 使得配置生效

```shell
echo "source /opt/ros/humble/setup.zsh" >> ~/.zshrc
```

- 设置 domain id

```shell
echo "export ROS_DOMAIN_ID=1" >> ~/.zshrc
```

## Turtlesim 

- zsh 无法识别占位符问题


```shell
setopt no_nomatch
# 加入配置文件
echo "setopt no_nomatch" >> ~/.zshrc
```