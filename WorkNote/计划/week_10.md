## 计划池

|          |       |
| :------: | :---: |
| complete |   0   |
|  delay   |   0   |
|  cancel  |   0   |
|  total   |  30   |

华为合作
- [ ] {文档} 调研典型业务画像过程
- [ ] {文档} 调研典型业务负载分析方式
- [ ] {代码} 典型应用 syscall 画像
- [ ] {文档} memtier 压测工具调研
- [ ] {文档} 制定 perf 采集方案
- [ ] {文档} otel 采集


arceos
- [ ] {文档} arceos源码阅读
- [ ] {文档} opensbi
- [ ] {代码} 网卡移植
- [ ] {文档} hypervisor 练习

工作
- [ ] {文档} 开源之夏项目文档

学术
- [ ] {文档} laTex语法学习
- [ ] {文档} LibOS/Unikernel调研

ebpf
- [ ] {文档} cloudflare/ebpf-exporter ebpf 代码加载源码分析
- [ ] {文档} cloudflare/ebpf-exporter ebpf 输出读写分析
- [ ] {代码} hist/guage/count metric in kernel
- [ ] {代码} otel exporter: metric for metric ebpf, log for event ebpf
- [ ] {文档} 了解 ebpf opcode 和 verify 过程
- [ ] {代码} 为 libbpf 社区贡献 rust example 代码
- [ ] {代码} 系统调用采集器

k8s
- [ ] {文档} k8s原理复习
- [ ] {文档} k8s 各组件之间如何响应资源的CRUD
- [ ] {代码} operator 相关api
- [ ] {文档} operator 教程

container
- [ ] {文档} podman调研
- [ ] {文档} docker原理复习
- [ ] {文档} runC架构
- [ ] {文档} youki调研
- [ ] {文档} 尝试解决youki在podman rootless下的问题
- [ ] {文档} LXC与Docker等的异同
- [ ] {文档} OCI标准调研

其他
- [ ] {文档} 整理 rust 相关内容(引用与解引用)


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
1. 组会
</th>

<!-- 周二 -->
<th>
2. 简历
</th>

<!-- 周三 -->
<th>
3. ebpf网络性能调优
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

<!-- ---------------- 完成 ---------------- -->
<tr>
<th>完成</th>

<!-- 周一 -->
<th>

</th>

<!-- 周二 -->
<th>

</th>

<!-- 周三 -->
<th>

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

209: 滑动窗口, 注意并非找到滑动窗口的最优解并跳出, 而是基于滑动窗口来实现 On 的遍历, 在暴力算法中, 可以通过移动右边界, 再遍历左边界的方式来遍历所有可能的子序列, 但考虑到假如一个子序列满足 sum >= target, 那么左边界以左的区间实际并没有考虑的意义, 因为其长度必然大于当前的长度, 故可以在当前的基础上, 向左移动左边界来找到最优解
26: 快慢指针, 可以想象为两个数组,一个是原数组, 用来遍历, 另一个是结果数组, 保存符合要求的数据, 只不过在同一个实际数组上, 有序情况下, 慢指针的移动只需判断最后一个值即可
283: 快慢指针, 遍历完毕之后, 末尾填充0即可
844: 快慢指针, 首先通过快慢指针处理字符串中的 '#', 再进行比较


快慢指针模板, 其中 flag 用来判断当前元素是否符合要求

```
int slow = 0;
for (int fast = 0; fast < numsSize; fast++)
{
    bool flag = ;
    if (flag)
    {
        nums[slow++] = nums[fast];
    }
}
```

```
int removeElement(int* nums, int numsSize, int val){

    int left, right;
    left = 0;
    right = numsSize - 1;

    while (left <= right)
    {
        while ((left <= right) && (nums[left] != val))
        {
            left++;
        }
        while ( (left <= right) && nums[right] == val)
        {
            right--;
        }

        if (left < right)
        {
            nums[left++] = nums[right--];
        }

    }
    return left;
}
```