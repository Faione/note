## 计划池

|          |       |
| :------: | :---: |
| complete |       |
|  delay   |       |
|  cancel  |       |
|  total   |       |


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


[455](https://leetcode.cn/problems/assign-cookies/): 局部最优是将最大的饼干给胃口最大的同学, 推导至全局最优即最多同学数量, 因而实现为先对两个数组排序, 然后从后往前依次分配

[376](https://leetcode.cn/problems/wiggle-subsequence/): 由于可以删除, 故策略为计算当前序列中, 出现峰值的数量, 如果数组长度不0, 则初始化rlt为1, 每出现一次峰值, 就rlt++, 并移动 pre, 而出现峰值必须满足 `(pre <= 0 && cur > 0) || (pre >= 0 && cur < 0)`, 

[53](https://leetcode.cn/problems/maximum-subarray/): 局部最优是当前序列的和大于0, 则能够推至全局最优为最大值, 因此使用一个 sum 记录当前的最大和, 使用 rlt 记录结果(初始化为INT32_MIN), 每次循环时更新 sum, 如果 sum 大于 rlt, 则将 rlt 赋值为 sum, 而一旦 sum 小于等于 0 , 则将 sum 初始化0(即当前遍历的序列不会对最大和产生贡献)

[122](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/): 

