# Diannao

## 阅读记录

- 题目
  - DianNao: A Small-Footprint High-Throughput Accelerator for Ubiquitous Machine-Learning
- 作者
  - Tianshi Chen
- 会议
  -

### Problem & Background

- 为特定的机器学习算法设计相应的硬件加速器是可行的
- 当前这些计算负载大多运行在使用SIMD的多核平台、GPUs、FPGAs上，先行的许多工作工作重点在于高效地实现各种机器学习算法的计算原语，而要么为了实现简单而忽略内存传输，要么通过DMA直接将加速器接入到内存上



### Challenges



### State-of-the-arts



### Key insights/ideas/techniques

- 将加速器的设计集中在内存使用上，并研究了加速器架构和控制，以最小化内存传输，并尽可能有效地执行它们
- 对于DNN与CNN，逐层进行加速优化
  - Inputs/Outputs
  - Synapses

#### Accelerator for Small Neural Networks


### Lessons learned from experiments