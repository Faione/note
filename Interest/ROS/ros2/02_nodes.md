# Basic Background

- [Basic Background](#basic-background)
  - [node](#node)
    - [重映射](#重映射)
    - [node info](#node-info)
  - [topics](#topics)

## node

- ROS2 图
  - ROS2 node
    - 每个ROS node负责一个单一模块的用途
    - 每个模块能够发送与接收其他node的数据
      - 通过 topics、services、actions、或 parameters
    - 一个完整的机器人协作系统有多个node构成，每个可执行的文件可以包含一个或多个node

- [continue](https://docs.ros.org/en/humble/Tutorials/Understanding-ROS2-Nodes.html)


### 重映射

- 创建一个新的节点，但是名称进行重映射
  - `--remap __node:=my_turtle`

```shell
ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle
```

### node info

- 查看节点的信息

```shell
ros2 node info <node_name>
```

## topics