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


[28](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/): KMP 算法, 核心在与找到 next 数组, next 数组指示了匹配串中, 某一下标所对于字符的等效位置(最长相等前后缀), 当此下标的下一个元素不匹配时, 可以对齐等效位置, 继续比较. next数组的生成在于找到下标 i 的等效位置 j, 满足 [0, j] 与 [i - j, i] 完全相同, 即最长的前后缀, 没有则 j = -1
[459](https://leetcode.cn/problems/repeated-substring-pattern/): 构建next数组, 对于重复字串的字符串, 比如有最长相等前后缀之差为一个重复单元, 满足 s_len % (s_len - 1 - next[s_len - 1]) == 0

[102](https://leetcode.cn/problems/binary-tree-level-order-traversal/): 层序遍历即广度优先遍历, 核心在于使用一个队列来保存当前层的所有节点, 每次出队某一层的所有节点, 并将其子节点再入队

[107](https://leetcode.cn/problems/binary-tree-level-order-traversal-ii/): 使用层序遍历一遍, `push_back` 每层的节点列表, 再使用 `reverse(rlt.begin(), rlt.end())` 反转即可

[199](https://leetcode.cn/problems/binary-tree-right-side-view/): 层序遍历, 每层遍历到最后一个时, 单独处理, 即将循环大小修改为 `l - 1`, 手动处理最后一个

[637](https://leetcode.cn/problems/average-of-levels-in-binary-tree/): 层序遍历, 求每层平均值

[429](https://leetcode.cn/problems/n-ary-tree-level-order-traversal/): 层序遍历, 参考模板

[515](https://leetcode.cn/problems/find-largest-value-in-each-tree-row/): 层序遍历, 每层求最大值即可, `int max = INT_MIN`

[116](https://leetcode.cn/problems/populating-next-right-pointers-in-each-node/): 层序遍历, 每层遍历到最后一个时, 单独处理

[104](https://leetcode.cn/problems/maximum-depth-of-binary-tree/): 递归, 如果当前节点为空, 返回0, 否则返回左右子树中较大的一个, 实质上每次求的都是节点高度, 但因为最大深度 = 最大高度

[111](https://leetcode.cn/problems/minimum-depth-of-binary-tree/): 层序遍历, 如遍历到某个节点没有左右字节点时, 返回当前深度即可

```c++
queue<Node*> q;

if (root != NULL) q.push(root);

while(!q.empty())
{
    // 当前层的节点数量
    int l = q.size()
    for (int i = 0; i < l; i++)
    {
        Node* n = q.front();
        q.pop();

        if (n->child != NULL) q.push(n->child);
    }
}
```

[559](https://leetcode.cn/problems/maximum-depth-of-n-ary-tree/): 层序遍历

[222](https://leetcode.cn/problems/count-complete-tree-nodes/): 递归, 如果当前节点为空, 则返回0并终止递归, 否则 `1 + countNodes(root->left) + countNodes(root->right)`

[110](https://leetcode.cn/problems/balanced-binary-tree/): 递归, 如果当前节点为空, 返回0 ,否则先计算左, 右子树高度, 如果左右子树存在不平衡, 或高度差大于, 则返回 -1, 表示不是平衡树, 否则则返回当前层高

[226](https://leetcode.cn/problems/invert-binary-tree/): 后序遍历, 每次替换左右子树即可

[590](https://leetcode.cn/problems/n-ary-tree-postorder-traversal/): 非递归写法后续遍历

[589](https://leetcode.cn/problems/n-ary-tree-preorder-traversal/): 非递归先序

[100](https://leetcode.cn/problems/same-tree/): 递归

```c
bool isSameTree(struct TreeNode* p, struct TreeNode* q){
    if (p == NULL && q == NULL) return true;
    if (p == NULL || q == NULL) return false;
    return p->val == q->val && isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
}
```

[101](https://leetcode.cn/problems/symmetric-tree/): 以左右子树对称移动进行递归

[572](https://leetcode.cn/problems/subtree-of-another-tree/): 递归将每个节点都与subtree比较

[257](https://leetcode.cn/problems/binary-tree-paths/): 迭代前序, 使用栈保存节点, 使用 vector 保存当前节点所构成的路径, 循环中每次都弹出一个节点, 极其所构成路径, 判断其是否是叶子节点, 否则将其左右节点加入到栈中, 并生成字节点对应的路径

[404](https://leetcode.cn/problems/sum-of-left-leaves/): 递归, 如果当前节点为空, 返回0, 否则判断当前节点的左节点是否是左叶子节点, 并记录其值, 与左/右探测结果一起进行返回

[513](https://leetcode.cn/problems/find-bottom-left-tree-value/submissions/): 层序遍历, 手动处理第一个, 将其值赋值给全局遍历 val, 作为左值进行返回

[112](https://leetcode.cn/problems/path-sum/): 迭代前序, 使用一个 栈 保存节点, 另一个栈保存和, 两个栈互相对应, 循环中每次都弹出一个节点和一个和, 判断其是否是叶子节点, 及和是否与 target 相同, 否则将其左右节点加入到栈中, 并生成子节点的和加入到栈中

[113](https://leetcode.cn/problems/path-sum-ii/): 迭代前序, 使用一个 栈 保存节点, 另一个 栈 保存路径, 两个栈互相对应, 循环中每次都弹出一个节点和对应路径, 如果是叶子节点, 则遍历其路径判断和是否为 target, 否则则否则将其左右节点加入到栈中, 并生成子节点的路径加入到栈中

[106](https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/submissions/): 后序列表最后一个是根, 找到其在中序列表中的位置, 左边是左子树, 右边是右子树, 而后序数组的组成为(左子树, 右子树, 根), 基于这一分析, 使用递归, 如果数组为空, 则返回空节点, 否则则根据分析得到根节点, 以及左右子树的中序 / 后序数组, 递归生成子树即可

[105](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/submissions/): 前序第一个是根, 组成为(根, 左子树, 右子树)

[654](https://leetcode.cn/problems/maximum-binary-tree/): 递归, 序列中最大的为根, 左边为左序列, 右边为右序列

[617](https://leetcode.cn/problems/merge-two-binary-trees/): 递归, 对两棵子树同时前序遍历, 某一为空时, 返回另一即可, 当两边都不为空时, 合并值, 并递归地求左, 右子树

[700](https://leetcode.cn/problems/search-in-a-binary-search-tree/): 递归, 根据搜素树的特点, 如果当前值小于目标值, 则应该向右子树搜索, 反之则搜索左子树

[98](https://leetcode.cn/problems/validate-binary-search-tree/): 迭代中序, 对于搜索树得到的一定是一个有序序列, 判断即可

[530](https://leetcode.cn/problems/minimum-absolute-difference-in-bst/): 二叉搜索树中序遍历结果是一个有序数组, 计算有序数组中的最小差值即可

[501](https://leetcode.cn/problems/find-mode-in-binary-search-tree/): 二叉搜索树中序遍历结果是一个有序数组, 众数会连续地出现, 因此使用中序遍历, 并使用一个vector保存众数, 遍历中记录上一个遍历的节点, 判断是否与当前节点值相等, 更新count, 并维护一个 maxCount, 当 count > maxCount 时, 将 vector 全部清空, 并压入新的众数

[236](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/): 递归, 向左/右子树分别搜索 p, q, 如能搜索到, 则将当前节点进行返回, 否则则返回左/右节点

[235](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/): 递归, 对于搜索树, 可根据值特性进行剪枝

[701](https://leetcode.cn/problems/insert-into-a-binary-search-tree/): 递归, 当找到的位置时, 构造节点并返回, 否则则递归地为左/右节点赋值, 并返回当前节点

[450](https://leetcode.cn/problems/delete-node-in-a-bst/): 递归, 找到位置时, 如其左节点为空, 则直接返回其右节点, 如其右节点为空, 则直接返回左节点, 否则对右子树向左探测最小值, 将左子树接在其上, 并将root的右节点替换为root, 根据 val 与 key 的大小进行左右递归 

[669](https://leetcode.cn/problems/trim-a-binary-search-tree/): 递归, 如果当前节点值小于 low, 则向右搜索, 如果当前值大于 high, 则向左搜索, 如果在 low high 之间, 则首先对左,右进行剪枝, 并返回完毕的节点

[108](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/): 递归构造, 对于有序数组, 每次取中间位置的数字构造节点即可, 然后将数组分割, 向左/右构造即可

[538](https://leetcode.cn/problems/convert-bst-to-greater-tree/): 递归, 使用一个全局的 sum 来保存当前的累加值, 然后再按 右 中 左的顺序构造即可