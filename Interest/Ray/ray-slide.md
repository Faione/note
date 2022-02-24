---
presentation:
  width: 1600
  height: 1200
  theme: "white.css"
---

<!-- slide -->

# Ray

## 高性能分布式执行框架

<p align="right"> 方浩镭</p>

<!-- slide align="left" -->
## 目录

- **Ray-用户视角**
  - 从 init() 开始
  - Remote Function
  - Remote Object
  - Remote Class
- **Ray-编程模型**
  - task 编程模型
  - actor 编程模型

<!-- slide  align="left"-->

## 从 init() 开始

普通程序

```python
def add(value):
    return value + 1

result = add(1)

print(result)

```

Ray 程序

```python
ray.init()

@ray.remote
def add(value):
    return value + 1

result_ref = add.remote(1)
result = ray.get(result_ref)

print(result)
```