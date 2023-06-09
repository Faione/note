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


[59](https://leetcode.cn/problems/spiral-matrix-ii/): 以圈为粒度进行计算, 每条边按照 始开终闭 的思路填充, 注意如果存在中间元素, 需要手动填充, 而在循环体中, 每条边的区间为 [x, x + offset) 计算即可

[jz29](https://leetcode.cn/problems/shun-shi-zhen-da-yin-ju-zhen-lcof/): 同样以圈为粒度进行计算, 考虑到矩阵并非都是正方形, 因此当剩下的最后一部分不能构成圈时, 通常是一条直线,需要特殊处理

[203](https://leetcode.cn/problems/remove-linked-list-elements/): 使用dummyhead, 以 `cur->next->val` 为遍历项, 当 val 匹配时, 删除下一个node, 当 val 不匹配时, 移动 dummyhead, 最终返回 dummyhead->next

[707](https://leetcode.cn/problems/design-linked-list/): 使用dummyhead

[206](https://leetcode.cn/problems/reverse-linked-list/): dummyhead可以使用头插法, 或基于 cur, pre 和 next三个节点

[24](https://leetcode.cn/problems/swap-nodes-in-pairs/): 使用dummyhead, 仔细画图分析

[19](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/): 使用dummyhead, 既可以遍历求长度后再求index, 也可让快指针移动 n 之后, 再与慢指针一起移动, 以将 slow定位到倒数第 n 个的前一个位置, 再进行删除

[](https://leetcode.cn/problems/intersection-of-two-linked-lists-lcci/): 对于长度不等的链表,需要末端对齐, 即计算两者的长度, 移动较长的链表使得与短链表对齐, 如果两链表相交, 则必有相等的指针, 因此可以此为条件开始同时移动, 并再做判断

[142](https://leetcode.cn/problems/linked-list-cycle-ii/): 快慢指针, 如果相遇, 则存在环, 设圈入口点为 x, 相遇点距离入口 y, 则有 (x + y) 是圈长度的整数倍(fast = 2 slow), 此时在起始点设置一个指针, 与在相遇点的指针按1的步长同步移动, 由以上内容可推, 这两个指针必然在相遇点再次相遇(x+y是圈长的整数倍), 而由于两者步长一致, 从而可知其必然在入口点处相遇, 因此求入口只需让两个指针移动直到相遇即可

[242](https://leetcode.cn/problems/valid-anagram/): 考虑字符串为字母且均为小写, 因此可以使用一个 int[26] 数组作为hash表, 使用 `*s - 'a'` 计算下标

[349](https://leetcode.cn/problems/intersection-of-two-arrays/): 使用数组hash, 遍历一个得到map ,再遍历另一个, 注意修改 map 值以处理另一个数组中的重复

[202](https://leetcode.cn/problems/happy-number/): 存储计算的结果到map中 ,如果某次计算结果与之前的相同, 则说明会进入无限循环

[1](https://leetcode.cn/problems/two-sum/): 保存已遍历值的下标为map, 后续比较即可

[454](https://leetcode.cn/problems/4sum-ii/): 四数看成两两组合(也可以1,3, 但不如22效率搞), 记录22组合的和构成map, 然后再对剩余的部分进行遍历即可

[383](https://leetcode.cn/problems/ransom-note/): 使用 wordMap