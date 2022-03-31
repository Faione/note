# Reading

## 工作说明

大家好，ATC 2022 的第二轮审稿工作开始了，需要大家帮忙一起审一下论文，并写审稿意见（尽量英文）。由于时间比较紧急，请大家在4月3日中午前把 Review 意见反馈给我

1）review 文件中每个部分都要填，其中 comment 部分写大约 300-500 个单词的评论，尽量用英文

2）Questions for authors' response 部分需要提出 2-3 个问题

3）如果 reject，需要把拒绝的理由给的充分一些

4）请大家在 4月3日中午之前将 review 发我。

本次审稿共 5 篇论文，题目如下图所示，大家积极认领哇

## 阅读记录

### Problem & Background

- 背景
  - 应对GPU使用需求的增长，常见的方式是使用共享多GPU服务器，这样能够节省基础设施的成本
    - ？此处多GPU仅是指，GPU服务器上有多个可用的GPU，这些GPU相互独立
  - 受限于硬件技术，当前GPU提供商难以在GPU内存容量上继续扩展，而为应对GPU内存不足，当前的主要趋势是使用host内存作为GPU内存，这样的内存交换方式受限于PCIe接口速率, 产生显著的性能开销
    - Nvidia提供了NvLink，使得GPU之间能够相互访问，且带宽远高于PCIe(600GB/s -> 32GB/s)
      - A100内置NVlink支持多达12个三代NVlink的连接
- 问题
  - 在多GPU场景下，不同GPU中的内存负载相互独立，因此存在当部分GPU因内存不足而受迫使用Host内存时，其他GPU的内存仍有空闲的情况，这会导致多GPU场景下GPU内存的使用效率相对较低

### Challenges

- GPU中的空闲内存数量高度可变且难以提前预知，因此有效获取可用的邻近GPU空闲内存非常困难


### State-of-the-arts

- 应对多GPU场景的 HUVM (hierarchical unified virtual memory)以及与之配套的GPU内存管理系统 memHarvester
  - HUVM由 local GPU, spare memory of neighbor GPUs, the host memory 三部分组成，内存不足依次访问

### Key insights/ideas/techniques

### Lessons learned from experiments

## 工作内容

==+== USENIX ATC '22 Review Form
==-== DO NOT CHANGE LINES THAT START WITH "==+==" OR "==*==".
==-== For further guidance, or to upload this file when you are done, go to:
==-== https://atc22.usenix.hotcrp.com/offline

==+== =====================================================================
==+== Begin Review #1279
==+== Reviewer: Yungang Bao <baoyg@ict.ac.cn>

==+== Paper #1279
==-== Title: Memory Harvesting in Multi-GPU Systems with Hierarchical
==-==        Unified Virtual Memory

==+== Review Readiness
==-== Enter "Ready" if the review is ready for others to see:

Ready

==*== Overall merit
==-== Choices:
==-==    1. Reject
==-==    2. Weak reject
==-==    3. Weak accept
==-==    4. Accept
==-==    5. Strong accept
==-== Enter the number of your choice:

(Your choice here)

==*== Reviewer expertise
==-== Choices:
==-==    1. No familiarity
==-==    2. Some familiarity
==-==    3. Knowledgeable
==-==    4. Expert
==-== Enter the number of your choice:

(Your choice here)

==*== Paper summary
==-== Markdown styling and LaTeX math supported.



==*== Strengths
==-==    What are the paper’s important strengths? Just a couple sentences,
==-==    please.
==-== Markdown styling and LaTeX math supported.



==*== Weaknesses
==-==    What are the paper’s important weaknesses? Just a couple
==-==    sentences, please.
==-== Markdown styling and LaTeX math supported.



==*== Comments for author
==-== Markdown styling and LaTeX math supported.



==*== Questions for authors’ response
==-==    Specific questions that could affect your accept/reject decision.
==-==    Remember that the authors have limited space and must respond to
==-==    all reviewers.
==-== Markdown styling and LaTeX math supported.



==*== Comments for PC
==-== (hidden from authors)
==-== Markdown styling and LaTeX math supported.



==+== Scratchpad (for unsaved private notes)

==+== End Review

