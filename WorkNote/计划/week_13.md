## 计划池

|          |       |
| :------: | :---: |
| complete |       |
|  delay   |       |
|  cancel  |       |
|  total   |       |

华为合作
- [ ] {文档} 调研典型业务画像过程
- [ ] {文档} 调研典型业务负载分析方式
- [ ] {文档} memtier 压测工具调研
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
1. 准备组会内容 <br>
</th>

<!-- 周二 -->
<th>
1. 尝试解决 prometheus 采集时间差问题
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
1. 为 prometheus 增加 honor_timestamp 解决此问题
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

