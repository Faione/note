## Divide & Conquer
### Q1: 找到序列A中的第n小元素
分治：找到A中第n/4、3n/4小元素
#### S2：打破cycle
寻找A的替代: 
- group medians, 确定性采样  
- 随机选择r个元素
  - 控制r足够小