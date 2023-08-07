## 数组

[704](https://leetcode.cn/problems/binary-search/): 二分查找，注意根据是 左闭右开 还是 左闭右闭 来决定 right 初始化为 size() 还是 size() -1 left = right 是否由意义，以及内部边界的移动

[35](https://leetcode.cn/problems/search-insert-position/description/): 二分查找，使用 左闭右开， 最终的right是target应该在，但数组中没有的位置，即要插入的位置

[34](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/description/): 使用二分法分别查找target在数组中最左边-1 和最右边 + 1 的位置，-2 标记搜索不到，搜索左边界时， 即在 target <= nums[mid] 分支中寻找, right - left > 1 是， 返回  {left + 1, right - 1}， 否则返回 {-1, -1}

[27](https://leetcode.cn/problems/remove-element/): 双指针， slow指向不是val的数组的后一个(空位)， fast 遍历数组，将不是val的元素放入到slow中

[977](https://leetcode.cn/problems/squares-of-a-sorted-array/): 双指针，考虑数组递减，那么最大值一定再左端或右端，因此设置两个指针与一个新数组，分别从左往右，从右往左进行遍历，平方较大加入到新数组末尾

[209](https://leetcode.cn/problems/minimum-size-subarray-sum/): 滑动窗口, 注意并非找到滑动窗口的最优解并跳出, 而是基于滑动窗口来实现 On 的遍历, 在暴力算法中, 可以通过移动右边界, 再遍历左边界的方式来遍历所有可能的子序列, 但考虑到假如一个子序列满足 sum >= target, 那么左边界以左的区间实际并没有考虑的意义, 因为其长度必然大于当前的长度, 故可以在当前的基础上, 向左移动左边界来找到最优解

```c++
int minSubArrayLen(int target, vector<int>& nums) {
    int left = 0;
    int rlt = INT_MAX;
    int sum = 0;
    for(int i = 0; i < nums.size(); i++) {
        sum += nums[i];
        while(sum >= target) {
            rlt = min(rlt, i-left+1);
            sum-=nums[left++];
        }
    }

    return rlt == INT_MAX? 0 : rlt;
}
```

[26](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/): 快慢指针, 可以想象为两个数组,一个是原数组, 用来遍历, 另一个是结果数组, 保存符合要求的数据, 只不过在同一个实际数组上, 有序情况下, 慢指针的移动只需判断最后一个值即可

[283](https://leetcode.cn/problems/move-zeroes/): 快慢指针, 遍历完毕之后, 末尾填充0即可

[844](https://leetcode.cn/problems/backspace-string-compare/): 快慢指针, 首先通过快慢指针处理字符串中的 '#', 再进行比较


快慢指针模板, 其中 flag 用来判断当前元素是否符合要求

```c++
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

```c++
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

[59](https://leetcode.cn/problems/spiral-matrix-ii/): 以圈为粒度进行计算, 每条边按照 始开终闭 的思路填充, 注意如果存在中间元素, 需要手动填充, 而在循环体中, 每条边的区间为 [x, x + offset) 计算即可

[jz29](https://leetcode.cn/problems/shun-shi-zhen-da-yin-ju-zhen-lcof/): 同样以圈为粒度进行计算, 考虑到矩阵并非都是正方形, 因此当剩下的最后一部分不能构成圈时, 通常是一条直线,需要特殊处理

## 链表

[203](https://leetcode.cn/problems/remove-linked-list-elements/): 使用dummyhead, 以 `cur->next->val` 为遍历项, 当 val 匹配时, 删除下一个node, 当 val 不匹配时, 移动 dummyhead, 最终返回 dummyhead->next

[](https://leetcode.cn/problems/LGjMqU/): 对于比较复杂的链表重排，没有时间复杂度要求前提的下，可以使用数组保存链表，然后基于数组的随机访问特性进行处理

[707](https://leetcode.cn/problems/design-linked-list/): 使用dummyhead

[206](https://leetcode.cn/problems/reverse-linked-list/): 
- 使用dummyhead，反转过程即不断使用头插法将元素插入到 dummyhead中， dummyhead 初始化的 next 为 nullptr, 头插法会改变cur->next, 因此使用 cur + tmp 两个节点进行链表遍历
- 使用 pre, cur, tmp 三个节点， pre 初始化为 nullptr， cur 初始化为 head， tmp 初始化为 nullptr， while(cur) 开始遍历，过程中将 保存 cur->next 到 tmp， 随后进行反转，即 cur->next = pre, 然后移动 pre 到 cur，cur 到tmp 进入下一个循环

[92](https://leetcode.cn/problems/reverse-linked-list-ii/description/): 题目要求反转链表中的某一部分，相比于反转链表是一种拓展，思路为找到3个节点， 反转部分的前一个，反转部分的尾部，反转部分的后面一个，其中反转部分可以按206中任意一种方式反转，结束之后，判断 反转部分的前一个 是否为空，如果是，则说明反转部分从头部开始，那么需要将 head 设置为 dummyHead->next， 否则则需要将 反转部分的前一个 与 dummyHead->next接起来，然后再将 反转部分的尾部 与反转部分的后面一个 接起来即可

[24](https://leetcode.cn/problems/swap-nodes-in-pairs/): 使用dummyhead, 循环中设计 pre, cur, tmp 三个节点，循环的条件为 cur != nullptr, cur->next != nullptr, tmp 保存的是 cur->next->next

[19](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/): 使用dummyhead, 既可以遍历求长度后再求index, 也可让快指针移动 n 之后, 再与慢指针一起移动, 以将 slow定位到倒数第 n 个的前一个位置, 再进行删除

[](https://leetcode.cn/problems/intersection-of-two-linked-lists-lcci/): 对于长度不等的链表,需要末端对齐, 即计算两者的长度, 移动较长的链表使得与短链表对齐, 如果两链表相交, 则必有相等的指针, 因此可以此为条件开始同时移动, 并再做判断

[142](https://leetcode.cn/problems/linked-list-cycle-ii/): 快慢指针, 如果相遇, 则存在环, 设圈入口点为 x, 相遇点距离入口 y, 则有 (x + y) 是圈长度的整数倍(fast = 2 * slow), 此时在起始点设置一个指针, 与在相遇点的指针按1的步长同步移动, 由以上内容可知，行进x之后，环中节点相对入口点走了 x + y, 即回到入口点，从head出发的节点也到达了入口,即 这两个指针必然在相遇点再次相遇(x+y是圈长的整数倍), 返回此时的节点即可

## 哈希表

[1207](https://leetcode.cn/problems/unique-number-of-occurrences/description/): 使用hash记录每个元素的count, 然后再用一个hash记录每个count是否出现过，连续出现两次则意味着不是独一无二

[242](https://leetcode.cn/problems/valid-anagram/): 考虑字符串为字母且均为小写, 因此可以使用一个 int[26] 数组作为hash表, 使用 `*s - 'a'` 计算下标

[349](https://leetcode.cn/problems/intersection-of-two-arrays/): 使用数组hash, 遍历一个得到map ,再遍历另一个, 注意修改 map 值以处理另一个数组中的重复

[202](https://leetcode.cn/problems/happy-number/): 存储计算的结果到map中 ,如果某次计算结果与之前的相同, 则说明会进入无限循环

[1](https://leetcode.cn/problems/two-sum/): 保存已遍历值的下标为map, 后续比较即可

[454](https://leetcode.cn/problems/4sum-ii/): 四数看成两两组合(也可以1,3, 但不如22效率搞), 记录22组合的和构成map, 然后再对剩余的部分进行遍历即可

[383](https://leetcode.cn/problems/ransom-note/): 使用 wordMap


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

[77](https://leetcode.cn/problems/combinations/): 使用回溯模板进行构造, 使用 `n - (k - path.size()) + 1` 进行剪枝

```c++
class Solution {
private:
    vector<vector<int>> rlt;
    vector<int> path;

    void backtrace(int n, int k, int start_indext)
    {
        if (path.size() == k)
        {
            rlt.push_back(path);
            return;
        }

        for (int i = start_indext; i <= n - (k - path.size()) + 1 ; i++)
        {
            path.push_back(i);
            backtrace(n, k, i + 1);
            path.pop_back();
        }

        return;
    }

public:
    vector<vector<int>> combine(int n, int k) {
        rlt.clear();
        path.clear();

        backtrace(n, k, 1);
        return rlt;
    }
};
```

[216](https://leetcode.cn/problems/combination-sum-iii/): 基于回溯模板, 增加 sum 计算当前 path 的综合, 用于判断是否继续往子节点进行回溯

[17](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/): 基于回溯模板, 实际仍然是一个组合问题, 数字map到对应的字符串进行回溯, 需要计算当前数字对应的 字符串起点与长度

[39](https://leetcode.cn/problems/combination-sum/): 组合, 使用 start 避免重复选择, 考虑到单个元素可重复, 因此 start 设置为当前的 i即可

[40](https://leetcode.cn/problems/combination-sum-ii/): 组合, 使用 start 避免重复选择, 单个元素不可重复,应此 start 应当设置为 i+1, 同时由于 candidates 可能存在重复, 应此应当对 candidates 进行排序, 然后在垂直方向探测时, 如果当前元素与上一个元素相同, 则不进行回溯

[131](https://leetcode.cn/problems/palindrome-partitioning/): 回溯, 将分割理解为切 [start, i] 字符串下来, 然后再对剩余部分(i+1)进行回溯, 使用一个函数来判断字符串是否为回文串

[93](https://leetcode.cn/problems/restore-ip-addresses/submissions/): 回溯, 是基于切割字符串类似, 使用一个函数来判断一个字符串是否为合法的ip地址部分, 如果 start 到最后一个字符, 并且 path 长度为 4 则找到了一个合法的IP

[78](https://leetcode.cn/problems/subsets/): 组合, 使用 start 避免重复, 而由于子集没有长度限制, 因次每次回溯直接将当前path放入rlt中即可, 注意空集是任何集合的子集, 因此不必处理path为空的情况

[90](https://leetcode.cn/problems/subsets-ii/): 组合, 由于数组本身可能存在重复元素, 因此在树层遍历时需要避免重复, 故首先对数组进行排序, 然后在循环中判断当前i是否与 i-1 相同, 只有不同时才进行回溯

[491](https://leetcode.cn/problems/non-decreasing-subsequences/): 回溯, 考虑不能对数组进行排序, 因此需要使用 used 来避免树层的重复, 回溯逻辑中, 只要当前 num 没有当前数层遍历 ,且不比 path.back() 小, 则继续进行回溯, 每次回溯都将大于 1 path 放入到结果集中

[46](https://leetcode.cn/problems/permutations/): 全排列, 由于不是组合, 所以每次回溯时, 都对没有树枝上没有被 used 的值进行回溯, 故需要一个全局的 `used<bool>` 数组, `used.assign(nums.size(), false)` 初始化, 并在每次回溯时, 如果已经被used, 就跳过

```c++
class Solution {
private:
    vector<vector<int>> rlt;
    vector<int> path;
    vector<bool> used;

    void backtrace(vector<int>& nums) {
        if (path.size() == nums.size()) {
            rlt.push_back(path);
            return;
        }

        for(int i = 0; i < nums.size(); i++) {
            if (used[i]) continue;

            path.push_back(nums[i]);
            used[i] = true;
            backtrace(nums);
            path.pop_back();
            used[i] = false;
        }
        
    }

public:
    vector<vector<int>> permute(vector<int>& nums) {
        rlt.clear();
        path.clear();
        used.assign(nums.size(), false);

        backtrace(nums);

        return rlt;   
    }
};
```

[47](https://leetcode.cn/problems/permutations-ii/): 全排列, 但是原数据可能存在重复, 使用used数组避免树枝上的重复, 而为避免树层的重复, 使用一个map, 记录当前层已经遍历过的值, 并在循环中跳过已经遍历过的相同的值 || 或者对数组排序, 然后利用 `(i > 0 && nums[i] == nums[i-1] && used[i-1] == false` 判断当前值已经被使用过

[455](https://leetcode.cn/problems/assign-cookies/): 局部最优是将最大的饼干给胃口最大的同学, 推导至全局最优即最多同学数量, 因而实现为先对两个数组排序, 然后从后往前依次分配

[376](https://leetcode.cn/problems/wiggle-subsequence/): 由于可以删除, 故策略为计算当前序列中, 出现峰值的数量, 如果数组长度不0, 则初始化rlt为1, 每出现一次峰值, 就rlt++, 并移动 pre, 而出现峰值必须满足 `(pre <= 0 && cur > 0) || (pre >= 0 && cur < 0)`, 

[53](https://leetcode.cn/problems/maximum-subarray/): 局部最优是当前序列的和大于0, 则能够推至全局最优为最大值, 因此使用一个 sum 记录当前的最大和, 使用 rlt 记录结果(初始化为INT32_MIN), 每次循环时更新 sum, 如果 sum 大于 rlt, 则将 rlt 赋值为 sum, 而一旦 sum 小于等于 0 , 则将 sum 初始化0(即当前遍历的序列不会对最大和产生贡献)

[122](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/): 贪心， 第 1 天买， 第 3 天卖的收益为 price[3] - price[1] = price[3] - price[2] + price[2] - price[1], 即最大收益取决于间隔中隔天为正的差值，因此题目退化为数组中，连续元素的最大和， 而又考虑到买，卖可自由选择，那么题目可进一步退化为所有正赢利之和

[55](https://leetcode.cn/problems/jump-game/): 贪心，设置当前能够跳跃的最远的下标为 cover， 初始为0， 局部最优为寻找最所能跳跃范围内最大的数字并依靠其增加cover， 一旦cover到达数组最后一个，那么就能够到达最后一个位置，否则则不行， 可以用一个 tmp 记录当前循环的元素与当前下标之和，如果其大于当前cover则对cover进行更新

[45](https://leetcode.cn/problems/jump-game-ii/): 贪心， 原理与55相同，区别在于要求最小跳数，显然当cover覆盖最后一个时，即满足最小跳数，目标在于如何计算跳数，使用 step 记录跳数，使用 pre_cover 记录上一跳能够到达的最大范围， 当遍历置 pre_cover 时， 如还没到达最后一个， 则必须进行跳跃，此时将 pre_cover 更新为当 cover

[1005](https://leetcode.cn/problems/maximize-sum-of-array-after-k-negations/): 贪心， 将负数取反能够使得总和增加，因此首先对数组按绝对值大小从小到大排序并倒序遍历，遇到负数则取反并减少 k 的值， 如果循环结束k仍不为0，若k是奇数， 则将绝对值最小的数取反，此处取绝对值的原因在于， 如果最小正数的绝对值大于最大负数，此时若要将正数取反，不如将负数取反后再取反

[134](https://leetcode.cn/problems/gas-station/): 贪心， 从0开始累计余量，如果 sum 小于0， 则说明 [0, i] 都不能作为起点, start 必须为 i+1, 并重新计算sum， 同时记录 total, 如果最后 total < 0, 则返回-1

[860](https://leetcode.cn/problems/lemonade-change/description/): 贪心，账单5直接手下; 账单10，消耗5，增加10; 账单20，优先消耗一个10和一个5，如果不够，则再消耗三个5

[406](https://leetcode.cn/problems/queue-reconstruction-by-height/description/): 贪心， 将序列按身高降序，相同身高按前面的人数升序重排，即先处理身高高的人，相同身高优先处理前面人少的人。使用一个list保存结果(方便插入)， 前面有多少个就是list中 pos， 因而每次都取list的开头位置(q.begin()) 作为it, 按照 pos 计算要插入的位置，实现局部最优。由于重拍后从身高最高的开始处理，相同身高按前面人少的进行处理，后续的处理不会影响到先前的结果，因此可以从局部最优推导至全局最优

[452](https://leetcode.cn/problems/minimum-number-of-arrows-to-burst-balloons/): 贪心，首先将序列按一维度从小到大重排(左边界)， 可知当points不为0时，至少需要1箭，是否需要增加箭取决于下一个气球是否与上一个有重叠(i左 < i-1 右)， 无重叠则必须增加一箭，同时重置当前气球的右边界为重叠部分， 判断下一个气球

[435](https://leetcode.cn/problems/non-overlapping-intervals/description/): 贪心，思路与气球相同，核心在于重叠区域，如发现当前区域与下一个重叠， 则必须删除其中一个(rlt++), 并重置下一个的右边界为重叠区域，因为如果在下一个与此区域重叠， 则必须再删除一个

[763](https://leetcode.cn/problems/partition-labels/description/): 贪心， 首先遍历字符串获取每个字符最后出现的位置，保存到一个map(int hash[26])中，随后再次遍历字符串，使用right保存遍历过的字符的最后出现位置中的最远出现位置， 如果right与当前下标相同，则说明 left, right 包含了所有已遍历过的元素，此时更新 left 为 i+1

[56](https://leetcode.cn/problems/merge-intervals/description/): 贪心， 首先对将序列按一维度重新排列， 发现重叠时，则更新将下一个节点更新为并集，未重叠则将当前序列添加到数组中，由于会漏掉最后一个，因此对最后一个单独处理即可。该过程也可以完全在结果数组中进行， 即将第一个push到数组中， 然后使用 rlt.back() 进行操作

[738](https://leetcode.cn/problems/monotone-increasing-digits/description/): 贪心，从右向左遍历每一位，如果发现当前位大于上一位，即不满足从左到右递增， 则将当前位--， 上一位换成9， 需要注意的是，如果这种情况发生在高位，则需要将低位全部置为9，才能够保证最大，因此使用一个 flag 来记录最后一个被修改  9 的位置， 随后只需从次开始依次修改即可

[968](https://leetcode.cn/problems/binary-tree-cameras/description/): 贪心， 局部最优是为每个叶子节点的父节点按照摄像机，同时对于父节点，每隔1一个安装1个摄像机，基于此，确定需要使用后序遍历， 同时使用0, 1, 2来表示节点当前状态为 无覆盖、有摄像头、有覆盖，考虑叶子节点的子节点为空节点，因而空节点认为是有覆盖
- 左右均有覆盖，此时当前节点为 0
- 左右中有一个无覆盖，则当前节点为 1
- 左右中有一个摄像头，则当前节点为 2
- 递归完毕后，若头节点无覆盖，则还需单独处理


### 动态规划

[509](https://leetcode.cn/problems/fibonacci-number/description/): dp[i] 定义为第i个斐波那契数;递推: dp[i] = dp[i-1] + dp[i-2];初始化时， dp[0]=0，dp[1]=1;从2到n遍历;

[70](https://leetcode.cn/problems/climbing-stairs/description/): dp[i] 定义为n阶台阶的不同方法;dp[i] = dp[i-1] + dp[i-2];初始化时，dp[0]=1, dp[1]=1;从2开始遍历

[746](https://leetcode.cn/problems/min-cost-climbing-stairs/description/): dp[i]定义为跳到n台阶的最低花费;dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]); dp[0]=0, dp[1] = 0; 从2开始遍历，遍历到 cost.size(), 即使此处没有cost

[62](https://leetcode.cn/problems/unique-paths/description/): dp[i][j]定义为到点 i，j 的不同路径;dp[i][j] = dp[i-1][j] + dp[i][j-1]; dp[0][*], dp[*][0] 初始化为1；从 1, 1 开始运动

[63](https://leetcode.cn/problems/unique-paths-ii/description/): dp[i][j]定义为到点 i，j 的不同路径;dp[i][j] = dp[i-1][j] + dp[i][j-1]; dp[*][0] 初始化为1, 其中 * 为障碍点之前的点；从1，1开始移动，遇到障碍点则跳过

[343](https://leetcode.cn/problems/integer-break/): dp[i]定义为数字i拆分的最大乘积;  dp[i] = max(dp[i], max(j*(i-j), j*dp[i-j])), 即遍历j， 取最大的 d[i];dp[2] = 1; 从 3 开始， j 从 1 开始

[96](https://leetcode.cn/problems/unique-binary-search-trees/): dp[i]定义为1到i组成的二叉搜索树数量; dp[i] += dp[j-1] * dp[i-j], 其中 j-1 表示以j为头的左子树的数量，i-j表示以j为头的右子树的数量; 初始化为0， 考虑有乘法故dp[0]=1; 从1开始

[416](https://leetcode.cn/problems/partition-equal-subset-sum/description/): 分成两个子集的前提时集合元素和不是奇数，这部确认完成后可得到和的一半作为 target， 于是题目就转化为装箱问题，是否能找到一些元素，这些元素的和恰好为 target, 并且物品的价格既是元素的值;dp[i]定义为装满 i 大小箱子的最大值， i需要初始化为总和最大的一半;;;遍历物品，背包从 target 开始遍历， 通过 dp[target] == target 判断是否能恰好组成

[1049](https://leetcode.cn/problems/last-stone-weight-ii/): 将石头分为两个大小非常接近的集合(注意是离散，不可直接分)，差值即为最后剩余的石头的最小值，因此问题转化为计算能够装入石头总重一半的集合的重量的最大值，即求分成两个子集之差最小的问题

[494](https://leetcode.cn/problems/target-sum/): 分析题目可知，实际是寻找两个子集left， right 使得子集内之和 left - right = target，即求分成两个子集之差为目标值的问题，可知前提是 left = (sum + target) / 2, 其中 left 是整数， 故首先判断，然后转化为将元素装入 left 的装箱问题;dp[i], i为箱子大小，而dp[i]是组合数量，显然 dp[j] += dp[j-nums[i]];dp[0]初始化为1

[474](https://leetcode.cn/problems/ones-and-zeroes/): 由于0和1的数量直接由当前遍历的字符串 str 决定， 故实际上仍然是一个01背包问题， dp[i][j] 表示 i个0, j个1 的最大组合数，显然 dp[i][j] = max(dp[i][j], dp[i-numof0][j-numof1] + 1)； dp[0][0] 为 0 即可

[518](https://leetcode.cn/problems/coin-change-ii/description/): 硬币可以无限使用，因此是一个完全背包问题，故需**从小到大**遍历背包，由于次数使用累计，需要初始化 dp[0] 为 1

[377](https://leetcode.cn/problems/combination-sum-iv/): 数字使用无数次，同时不同的顺序是不同的组合，即需要考虑排列，因此需要先遍历背包，再遍历物品; c++ 中需要考虑 INT_MAX 溢出问题(不要判断 a + b < INT_MAX, 而判断 a < INT_MAX - b)

[70](https://leetcode.cn/problems/climbing-stairs/): 爬楼梯也是一个完全背包问题，即对于层高n, 可选任意次数的 1， 2， 3..m;

```c++
vector<int> dp(n+1, 0);
dp[0] = 1;

// 背包
for (int i = 1; i <= n; i++) {
    // 物品, 即一次1, 2，3..m台阶
    for (int j = 1; j <= m; j++) {
        if (j<=i) dp[i] += dp[i-j];
    }
}
```

[322](https://leetcode.cn/problems/coin-change/description/): dp[i] 表示凑足 i 的最小硬币数量; dp[i] = min(dp[i], dp[i - coin] + 1);初始化dp[0]为0， 其余为 INT_MAX, INT_MAX指示未初始化过的值，而递推中存在 +1 操作， dp[0]=0也合理; 求组合，故先物品后背包；如最后 amount 都仍然是初始化状态，则说明没有找到合适的组合

[279](https://leetcode.cn/problems/perfect-squares/description/): 完全背包， dp[i] 表示和为 i 的最小平方数数量; dp[i] = min(dp[i], dp[i - num] + 1); 初始化dp[0]为0， 其余为 INT_MAX; 注意的是，物品是 1, 4 .. i*i, 其中 i*i <= n, 其余与322类似

[139](https://leetcode.cn/problems/word-break/description/): 字符串可重复使用，因此是一个完全背包问题，同时考虑排列问题，需要先遍历背包再遍历物品, dp[i] 表示长度为 i 的字符串能否被由字典中的单词组成， dp[i] = dp[j] and s[j, i] in dict; 显然需要初始化 dp[0] = true; `unordered_set<string> wordSet(wordDict.begin(), wordDict.end())` 构造集合，并使用 wordSet.find() 查找对应字符串的下标

[198](https://leetcode.cn/problems/house-robber/description/): dp[i] 定义为到下标i为止的房屋能偷盗的最高金额; dp[i] = max(dp[i-2] + pro[i], dp[i-1]); dp[0] = pro[0], dp[1] = max(pro[0], pro[1]), 其余初始化为0

[213](https://leetcode.cn/problems/house-robber-ii/description/): 相比于 198, 213是一个循环队列，由于头尾相接，而相邻两个不能同时偷窃，因此可以将循环队列分位不包括头，不包括尾，头尾均不包括三种情况进行分析，其中第三种情况包括在前两种中，因此可以抽象 robRange 的逻辑，处理与198相同，但增加了 start 和 end 两个位置标识限定了dp的范围, 分别计算两种情况下的值

[337](https://leetcode.cn/problems/house-robber-iii/description/): 此时的拓扑结构是树形， 父子关系的两个房屋不能被同时偷窃， 考虑是否偷窃父节点需要考虑子树的值，因此需使用后序遍历方法，同时dp不再是一个全局的数组，而是在递归中进行传递，定义一个二维数据dp[2], 其中 dp[0], dp[1] 表示偷与不偷当前节点锁获得的最大值，因此对父节点而言，fdp[0] = ldp[1] + rdp[1] + c->val, fdp[1] = max(ldp[0], ldp[1]) + max(rdp[0], rdp[1]);

[121](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/description/): 分析题意，可以得知存在两种状态，持有股票， 不持有股票， 故设置 dp[i][0] 表示第 i 天持有股票的最大收入，而 dp[i][1] 表示第 i 天不持有股票的最大收益， 遍历每天的股票价格; dp[i][0] = max(dp[i-1][0], -prices[i]), dp[i][1] = max(dp[i-1][1], dp[i-1][0] + prices[i]);dp[0][0] = -prices[0];
- 可以使用滚动数组进行优化，即只需为每个状态维护一个数据即可
- 无需考虑顺序，即使先更新了当天持有的最高利润，也不影响当前不持有的利润，因为当天买，当天卖不影响总利润(即使不被允许)

[122](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/): 相较于121， 由于股票可以多次买入，卖出，使得当天持有股票不在基于0的初始利润，而是基于上次卖出时的利润
- 当天买，当天卖收益为0，故最大收益时，状态一定是售出股票
- 最多持有一支股票，故不可能出现 x =  x - prices[i]

```c++
int maxProfit(vector<int>& prices) {
    int x = -prices[0];
    int y = 0;

    for (int i = 1; i < prices.size(); i++) {
        // 如果只能出售一次则 x = max(x, 0 - prices[i]);
        x = max(x, y - prices[i]);
        y = max(y, x + prices[i]);
    }

    return max(x, y);
}
```

[123](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/): 相较于 121, 最多能够买卖两次 ，需要对状态进行拓展， 即 持有第一支股票，不持有第一支股票，持有第二支股票，不持有第二支股票, 其中除了 dp[1] 和 dp[3] 为 -price[0] 外都初始化为0, 考虑可以当天买卖，那么dp[4] 一定是最大
- 持有一 dp[1] = max(dp[1], dp[0] - price[i])
- 不持有一 dp[2] = max(dp[2], dp[1] + price[i])
- 持有二 dp[3] = max(dp[3], dp[2] - price[i])
- 不持有二 dp[4] = max(dp[4], dp[3] + price[i])

[188](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/description/): 相较于 123,  **买卖次数为k次**，状态有 2*k 个

```c++
int maxProfit(int k, vector<int>& prices) {
    vector<int> dp(2*k + 1, 0);

    for (int i = 0; i < k; i++) dp[2*i+1] = -prices[0];

    for (int i = 1; i < prices.size(); i++) {
        for(int j = 1; j < 2*k + 1; j+=2) {
            dp[j] = max(dp[j], dp[j-1] - prices[i]);
            dp[j+1] = max(dp[j+1], dp[j] + prices[i]);
        }
    }

    return dp[2*k];
}
```

[309](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/): 根据题意建模，每天的状态可分为
- dp[0]: 持有股票       dp[0] = max(dp[0], max(dp[3] - price, dp[2] - price))
- dp[1]: 当天卖出股票    dp[1] = dp[0] + price
- dp[2]: 冷冻期         dp[2] = dp[1]
- dp[3]: 不持有股票       dp[3] = max(dp[3], dp[1])
最终返回的 当天卖出股票，冷冻期，不持有股票 都有可能是最大值，因此选择这些求最大值返回

[714](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/description/): 每天都有两个状态，持有股票或不持有股票, 其中 dp[0] = max(dp[0], dp[1] - price[i]), dp[1] = dp[0] + price[i] - fee;

[300](https://leetcode.cn/problems/longest-increasing-subsequence/): dp[i]为对于当前数组而言，以i为结尾的数组对应的最长递增的子序列长度; 求解dp[i] 需要遍历 d[j], j [0, i), 只要nums[j] < nums[i], dp[i] = max(dp[i], dp[j] + 1);显然对于任意子序列， 最长严格递增子序列的长度都至少是1， 故dp[*] = 1

[674](https://leetcode.cn/problems/longest-continuous-increasing-subsequence/): dp[i]为对于当前数组而言， 以i为结尾的数组对应的最长连续递增的子序列长度, 相比于300，因连续，只需要对 i-1 判断即可，不必遍历 0, i-1

[718](https://leetcode.cn/problems/maximum-length-of-repeated-subarray/): dp[i][j]对于nums1和nums2而言，指以nums1中以i-1为结尾，nums2中以j-1为结尾的最长公共子数组的长度(不适用之前的初始化方式是为了减少初始化工作); nums1[i-1] == nums2[j-1] 时， dp[i][j] = dp[i-1][j-1] + 1; 如不这样设置， dp[0][*] 和 dp[*][0] 都需要进行初始化才能进行判断

[1143](https://leetcode.cn/problems/longest-common-subsequence/): 与718不同的是，子序列无需连续，这意味在不相等时，还需要继续判断, dp定义与718相同;s1[i-1] = s2[j-1]时，dp[i][j] = dp[i-1][j-1] + 1, 而else时不再时初始化的值，而是 dp[i][j] = max(dp[i-1][j], dp[i][j-1]) (#此处dp[i-1][j-1]无意义，因为上一个也来自次)， 即回退; dp初始时均为0;考虑 dp[i][j] 由左、上，左上推得，故最大值必然出现在右下角

[1035](https://leetcode.cn/problems/uncrossed-lines/): 题目转化后，即是寻找 nums1 与 nums2 的最长公共子序列，故做法与 1143 相同

[53](https://leetcode.cn/problems/maximum-subarray/): 使用动态规划时， dp[i] 定义为以i为结尾的最大连续子序列和; 若dp[i-1] < 0, 显然dp[i] 需要从nums[i]重新计算，即dp[i] = max(nums[i], dp[i-1] + nums[i]); dp[0] = nums[0];

[392](https://leetcode.cn/problems/is-subsequence/): 可以直接使用 1143 的思路，最后判断最长公共子序列长度是否与s相等即可

[115](https://leetcode.cn/problems/distinct-subsequences/): dp[i][j] 定义为 以 i-1 结尾的 s 中 ，出现以 j-1 结尾的 t 的个数; 判断 s[i-1] 和 t[i-1]
- 相等， 则 dp[i][j] = dp[i-1][j-1] + dp[i-1][j], 考虑了使用 s[i-1] 和不使用 s[i-1] 匹配的情况, 而不相等时，dp[i][j] = dp[i-1][j], 模拟删除 s[i-1];按定义可知推导方向为左上和上，故 dp[*][0] = 1, dp[0][*] = 0, dp[0][0] = 1

[583](https://leetcode.cn/problems/delete-operation-for-two-strings/): dp[i][j] 定义为对以 i-1 结尾的 word1, 和以 j-1 为结尾的 word2, 使其相同做需的最小步骤; 如果 word1[i-1] == word2[j-1], 无需操作，即与dp[i-1][j-1] 相同, 反之则需要删除word1[i-1] 或 word[j-1], 取最小值;初始化时， dp[i][0] = i, dp[0][j] = j
- 另外一种解法时找到两个字符串的最长公共子序列， 删除操作的数量等于将两个字符串都删除到公共子序列的差值

[72](https://leetcode.cn/problems/edit-distance/description/): 与只删除不同的时，编辑距离中允许使用插入或替换;s[i-1] 和 t[i-1]相同时，不操作，不同时，则需要考虑插入，删除或替换， 即 dp[i][j] = max({dp[i-1][j-1], dp[i-1][j], dp[i][j-1]});初始化时， dp[i][0] = i, dp[0][j] = j

```c++
    int minDistance(string word1, string word2) {
        vector<vector<int>> dp(word1.size() + 1, vector<int>(word2.size() + 1, 0));
        for(int i = 0; i<=word1.size(); i++) dp[i][0] = i;
        for(int j = 0; j<=word2.size(); j++) dp[0][j] = j;

        for(int i = 1; i<=word1.size(); i++) {
            for(int j = 1; j<=word2.size(); j++) {
                if(word1[i-1] == word2[j-1]) dp[i][j] = dp[i-1][j-1];
                // 只删除时， dp[i][j] = min({dp[i-1][j], dp[i][j-1]}) + 1
                else dp[i][j] = min({dp[i-1][j-1], dp[i-1][j], dp[i][j-1]}) + 1;
            }
        }

        return dp[word1.size()][word2.size()];
    }
```

[647](https://leetcode.cn/problems/palindromic-substrings/description/): dp[i][j] 定义为 [i, j] 为回文串; 如果s[i] == s[j]时，如果 j-i < 1, 则必然时回文串，否则若 dp[i+1][j-1] 为 true ，则也为回文串; 注意 d[i][j] 由 dp[i+1][j-1] 推导而来，因此 i必须从大到小，j必须从小到大

```c++
int countSubstrings(string s) {
    vector<vector<bool>> dp(s.size(), vector<bool>(s.size(), false));

    int rlt = 0;
    for(int i = s.size() - 1; i >= 0; i--) {
        for(int j = i; j < s.size(); j++) {
            if (s[i]==s[j] && (j-i <= 1 || dp[i+1][j-1]) ) {
                rlt++;
                dp[i][j]=true;
            }
        }
    }

    return rlt;
}
```

[516](https://leetcode.cn/problems/longest-palindromic-subsequence/):  dp[i][j] 定义为 [i, j] 内最长的回文子串长度;只要s[i] == s[j]， dp[i][j] = dp[i+1][j-1] + 2, 否则 dp[i][j] = max(dp[i+1][j], dp[i][j-1]);为了遍历时的方便，可以将 dp[i][i] = 1， 这样就不用在循环中考虑 i == j 的情况


## 单调栈

使用一个栈来保存遍历过的数据，同时栈中的数据保证递增或递减(栈底到栈顶)
- 递减则意味着压入的数据不大于栈中的任何一个数据，对解决寻数组中第一个比起大的元素，当发现当前元素大于栈顶元素时，就必须将栈中元素出栈以找到适合放入当前元素的位置，来保证栈的单调性，而因此出栈的元素，当前元素即时比其大的第一个元素

[739](https://leetcode.cn/problems/daily-temperatures/description/): 分析题意即可知目标在于寻找比第一个比第i天高的温度的时间与i的差值, rlt初始化为0

[496](https://leetcode.cn/problems/next-greater-element-i/description/): 仍然是寻找下一个更大的元素，此处通过num1数据限定了需要查询的目标，因此可以通过一个map维护 num1 中值到下标的映射，这样在 num2 中完成的查询时，就可以通过map获取num1中的下标进行rlt的填充，rlt初始化为-1
- 使用 `unordered_map<int, int> umap` 定义 map， 使用 `umap.count(obj) > 0` 判断key是否存在， 使用 `umap[key]` 获取值

[503](https://leetcode.cn/problems/next-greater-element-ii/description/): 考虑循环数组，遍历两圈才能得到正确的数值

[42](https://leetcode.cn/problems/trapping-rain-water/description/): 考虑出现凹陷的地方才能装雨水，这部分的低点满足 >=左， <右, 从而在单调栈中使用 top - 1, top, i 就能够计算雨水数量 min(val[st[top - 1]], val[i]) * (i - st[top-1] -1) (注意只填平了最低的一层)

[84](https://leetcode.cn/problems/largest-rectangle-in-histogram/description/): 寻找波峰， 单调栈中单调递增排序, heights[mid] 为当前最高点， 则最大面积为 heights[mid] * (i-1 - st.top()), 其中 i-1 为当前所见到的最高柱子的下标， heights[mid] 为大于等于 heights[i] 的高度， i-1 - st.top() 即 heights[mid] 与 heights[cmax] 的距离， while进行直到栈顶元素 >= height[i];初始化时，向头和尾各插入一个 0， 其中在头部插入的0， 使得当只有一个元素时，循环也能进行下去， 而在尾部插入的0则意味着柱子非常平坦时，通过 > 0 找到最大的柱子


## 杂

[1365](https://leetcode.cn/problems/how-many-numbers-are-smaller-than-the-current-number/description/): 从小到大排序后，下标即是小于当前元素的数量，而对于相同的元素，构建hash表时从后向前遍历即可

[941](https://leetcode.cn/problems/valid-mountain-array/description/): 从右边找递增的最后一个元素， 从左找递减的最后一个元素，如果两个都移动了，且值相等时，即为山脉数组

[283](https://leetcode.cn/problems/move-zeroes/description/): 双指针， slow表示没有0的数组的后一个

[189](https://leetcode.cn/problems/rotate-array/description/): 向右轮转的效果实质与交换数组 x 与 y 部分逻辑类似，解法首先将 k 与 num.size() 运算以排除周期，然后将数组整体反转，再分别反转 [0, k-1], [k, num.size()-1]即可

[724](https://leetcode.cn/problems/find-pivot-index/description/): 对整体求和，然后开始遍历每个元素进行判断

[922](https://leetcode.cn/problems/sort-array-by-parity-ii/description/): 最简单的方式使用一个 rlt 数据， 然后遍历原数组将奇数、偶数分别写入rlt中;也可以原地进行修改，记录odd下标，初始化odd = 1， 并遍历偶数下标，当遇到一个非偶数时，while 直到找到一个奇数下标非偶数， swap 即可

[234](https://leetcode.cn/problems/palindrome-linked-list/description/): list -> vec, 再进行回文判断

[143](https://leetcode.cn/problems/reorder-list/description/): list->vec, 将中点(对偶数长度而言是中间位置坐标第一个)的后一个设置为 nullptr, 这样使得无论长度是否为偶数，重排后的最后一个总能指向 nullptr， 然后从i=0, j=v.size()-1向中间遍历即可

[141](https://leetcode.cn/problems/linked-list-cycle/description/): 使用slow，fast两个指针遍历，如果两者相遇，则说明有环(比较指针)

[205](https://leetcode.cn/problems/isomorphic-strings/description/): 单映射，使用两个map保存相互的映射，如果存在 1 对 n 或 n 对 1, 则返回错误

[1002](https://leetcode.cn/problems/find-common-characters/description/): 共用字符即统计某一个字符在所有字符串中的最小出现次数，即每个字符串中都至少有n个该字符，注意插入字符串到尾部时，要么使用 string s(1, c)， 这是因为，vector push_back 不会调用构造函数， 而 vector emplace_back 则不必如此，因为其会调用构造函数


## 剑指offer

5. 根据先序，中序重建二叉树，采用分而治之，递归的思想，preorder[0] 为根， inorder中根左边为左子树，右边为右子树，可获得子树长度，再回到preorder中, 由于总是先左子树再右子树，同时又知道子树长度，因此很容易得到preorder中的左/右子树
6. 双栈队列，其中一个用于尾插，另一个用于头出，实际实现中，正常入栈进行尾插，而再头出时，会将尾插栈全部出栈并保存到头出栈中，实现逆序，再进行头出
7. 无意义
8. 进阶斐波那契, 考虑最后一跳要么是1级, 要么是2级, 应此跳上n级台阶所用的次数就存在`d[n] = d[n-1] + d[n-2]`，从而分而治之
9. 可硬解，也可以使用二分查找优化，即旋转的点一定在 arr[left] > arr[right] 的区间中

12. dfs 深度优先遍历, 使用 used 数组来取代 visited 数组，即将已遍历过的字符设置为 `#` 等特殊字符，标记其已经被遍历过，同时注意C中需使用 `strlen` 来获取字符串长度
13. dfs 深度优先遍历，构造 visited 数组用来判断某个格子是否已经被访问过
14. 动态规划, 对于长度为i的绳子，考虑仁义剪法，都可将其视为两部分，其中一段不剪开，长度为j, 则另一段长度为 i-j, 如果另一段也不剪，则乘积为 j * (i-j), 而另一段如果要剪，则问题变为了求长度 i-j 绳子的最大乘积，显然可以用一个(n + 1)数组 dp[n + 1] 来保存从长度为 2 到长度为 n 的绳子的最大乘积, 则思路就从长度为2的绳子开始，依次补全dp, 最后返回dp[n]即可
15. 对大数进行判断，更换思路，考虑当  m = n / e 时能够取得极大值，因而如果能够将 n 拆成3和2的组合，并在能取到3的前提下，尽可能地使得3多出现，就能够达到最大值，因而只需要不断让 n 减去3, 同时在过程中，使用 long 存储结果，并在每次计算时取模，解决大数问题
16. n &= (n-1) 消去最右边的1
17. 快速幂的原理在于，如果指数是偶数，则可以将指数减半，底数取平方的形式减少连续乘法的次数，如果是奇数，则可以提取出一个，对余下部分继续使用快速幂，使用快速幂，同时使用 long 替换int 类型的指数，以保证求绝对值时不会发生溢出错误(负数总比正数多一个)