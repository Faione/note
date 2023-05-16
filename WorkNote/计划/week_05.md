## 计划池

|          |       |
| :------: | :---: |
| complete |  10   |
|  delay   |  24   |
|  cancel  |   0   |
|  total   |  34   |

ebpf
- [ ] {文档} 了解 ebpf opcode 和 verify 过程
- [ ] {代码} 为 libbpf 社区贡献 rust example 代码

k8s
- [ ] {文档} 调研 k8s Reconcile 相关内容
- [ ] {代码} operator 相关api
- [ ] {文档} operator 教程

rcore
- [ ] {代码} 完成基于virtio的block dev，通过相关测例{5.1}
- [x] {代码} 确定第一阶段日程，提交相关代码
- [ ] {文档} 整理 rust 相关内容(引用与解引用)
- [x] {文档} 补充lab1报告
- [x] {文档} 补充lab2报告
- [x] {文档} 补充lab3报告
- [x] {文档} 补充lab4报告
- [x] {文档} 补充lab5报告

找工作
- [x] {代码} 刷题 5 
- [ ] {代码} 刷题 5
- [ ] {代码} 刷题 5
- [ ] {代码} 刷题 5
- [ ] {代码} 刷题 5
- [ ] {文档} docker原理复习
- [ ] {文档} k8s原理复习

信息高铁
- [ ] {文档} harbor p2p 分发功能调研
- [x] {代码} perf exporter on arm && 增加 server exporter 算力暴露

华为合作
- [ ] {文档} 调研典型业务画像过程
- [ ] {文档} 调研典型业务负载分析方式
- [ ] {文档} redis， memcache， nginx， mysql， kafka， keydb， elasitc search，clickhouse，spark，hive
- [ ] {代码} 典型应用 syscall 画像
 
其他
- [x] {文档} 教材编写
- [x] {文档} 教材内容优化
- [ ] {代码} tokio && async rust
- [ ] {文档} runC架构
- [ ] {文档} rust youki等调研
- [ ] {文档} OScamp系统功能赛道
- [ ] {文档} laTex语法学习{5.1}
- [ ] {文档} LibOS/Unikernel调研


<table>
<tr>
<th></th>
<th>周一</th>
<th>周二</th>
<th>周三</th>
<th>周四</th>
<th>周五</th>
<th>周六</th>
<th>周天</th>
</tr>

<!-- ---------------- 计划 ---------------- -->
<tr>
<th>计划</th>

<!-- 周一 -->
<th>
1. 教材编写 <br>
2. tokio && async rust看完 <br>
</th>

<!-- 周二 -->
<th>
1. perf exporter on arm && 增加 server exporter 算力暴露 <br>
2. docker原理复习 <br>
3. k8s原理复习 <br>
</th>

<!-- 周三 -->
<th>
1. 了解 ebpf opcode 和 verify 过程 <br>
2. 调研 k8s Reconcile 相关内容 <br>
3. 完成基于virtio的block dev，通过相关测例 <br>
4. 教材内容优化 <br>
5. 刷题 5 <br>
</th>

<!-- 周四 -->
<th>
1. 了解 ebpf opcode 和 verify 过程 <br>
2. 调研 k8s Reconcile 相关内容 <br>
3. 完成基于virtio的block dev，通过相关测例 <br>
</th>

<!-- 周五 -->
<th>
1. 补充lab1报告 <br>
2. 补充lab2报告 <br>
3. 补充lab3报告 <br>
4. 补充lab4报告 <br>
5. 补充lab5报告 <br>
6. 完成基于virtio的block dev，通过相关测例 <br>
</th>

<!-- 周六 -->
<th>
1. 完成基于virtio的block dev，通过相关测例 <br>
</th>

<!-- 周天 -->
<th>
1. 完成基于virtio的block dev，通过相关测例 <br>
</th>

</tr>

<!-- ---------------- 完成 ---------------- -->
<tr>
<th>完成</th>

<!-- 周一 -->
<th>
1. 教材编写成，待修改 <br>
</th>

<!-- 周二 -->
<th>
1. 需求开发完成，解决arm上 `/proc/cpuinfo` 内容差异导致的数据问题<br>
2. 基于chroot, busybox搭建简易沙箱，docker原理简单复习 <br>
3. 复习部分 k8s 原理 <br>
</th>

<!-- 周三 -->
<th>
1. pass <br>
2. pass <br>
3. 提交task1 <br>
4. 教材内容优化 <br>
</th>

<!-- 周四 -->
<th>
1. 确定以ebpf学习为主要目标的方针 <br>
2. pass <br>
3. 完成lab1-lab5所有测例 <br>
</th>

<!-- 周五 -->
<th>
1. 补充lab1报告 <br>
2. 补充lab2报告 <br>
3. 补充lab3报告 <br>
4. 补充lab4报告 <br>
5. 补充lab5报告 <br>
6. pass <br>
</th>

<!-- 周六 -->
<th>
1. 调研MMIO <br>
</th>

<!-- 周天 -->
<th>
1. 整理virtio相关内容 <br>
</th>

</tr>

<!-- ---------------- 刷题 ---------------- -->
<tr>
<th>刷题</th>

<!-- 周一 -->
<th>
</th>

<!-- 周二 -->
<th>
</th>

<!-- 周三 -->
<th>
5
</th>

<!-- 周四 -->
<th>
</th>

<!-- 周五 -->
<th>
</th>

<!-- 周六 -->
<th>
</th>

<!-- 周天 -->
<th>
</th>

</tr>

</table>


5. 根据先序，中序重建二叉树，采用分而治之，递归的思想，preorder[0] 为根， inorder中根左边为左子树，右边为右子树，可获得子树长度，再回到preorder中, 由于总是先左子树再右子树，同时又知道子树长度，因此很容易得到preorder中的左/右子树
6. 双栈队列，其中一个用于尾插，另一个用于头出，实际实现中，正常入栈进行尾插，而再头出时，会将尾插栈全部出栈并保存到头出栈中，实现逆序，再进行头出
7. 无意义
8. 进阶斐波那契, 考虑最后一跳要么是1级, 要么是2级, 应此跳上n级台阶所用的次数就存在`d[n] = d[n-1] + d[n-2]`，从而分而治之
9. 可硬解，也可以使用二分查找优化，即旋转的点一定在 arr[left] > arr[right] 的区间中