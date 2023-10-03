==+== HPCA 2024 Review Form
==-== DO NOT CHANGE LINES THAT START WITH "==+==" OR "==*==".
==-== For further guidance, or to upload this file when you are done, go to:
==-== https://hpca2024.hotcrp.com/offline

==+== =====================================================================
==+== Begin Review #99
==+== Reviewer: Yungang Bao <baoyg@ict.ac.cn>

==+== Paper #99
==-== Title: SCMetrics: Estimating Request-Level Application Metrics from
==-==        System Calls with eBPF
    
==+== Review Readiness
==-== Enter "Ready" if the review is ready for others to see:

Ready

==*== Problematic paper formatting?
==-== (hidden from authors)
==-==    In an effort to assure that fairness among all the submissions, we
==-==    have asked all authors to follow the formatting guidelines
==-==    carefully. Please select if the paper follows the HPCA2024
==-==    formatting guidelines, or if it deviates enough to offer an unfair
==-==    advantage to the authors.
==-== Choices:
==-==    1. No Problem: The paper seems to follow the HPCA 2024 formatting
==-==       guidelines
==-==    2. The paper seems to violate the HPCA 2024 formatting guidelines
==-==       but not in a way that offers the authors an unfair advantage
==-==       over other submissions
==-==    3. Problem: The paper seems to violate the HPCA 2024 formatting
==-==       guidelines in a way that offers the authors an unfair advantage
==-==       over other submissions
==-== Enter the number of your choice:

1

==*== Paper summary
==-==    Provide an overview of the paper that can help other committee
==-==    members understand the key ideas and contributions of the work
==-==    (3-5 bullets).
==-== Markdown styling and LaTeX math supported.

1. 提出了一种基于ebpf监测框架，能够从应用的syscall activiy中估算应用的request-level指标
2. 提出了一系列表征request-level指标的估算算法，通过对于10种应用的的实验验证了算法的有效性，并允许输入QoS指标增加模型估计的准确性

==*== Strengths
==-==    What are the main insights, contributions, results and other
==-==    strengths of the paper that may serve as the basis for acceptance
==-==    (1-3 bullets).
==-== Markdown styling and LaTeX math supported.

1. 使用ebpf技术对内核进行观测，无需对用户应用进行插桩，且相较于perfmance counter性能开销更小
2. 证明了应用的系统调用活动与应用request-level指标之间的相关性，并设计了基于吞吐量和延迟的请求级指标估算算法
3. 提供了一套程序库来对进行指标查询，能够方便地与调度器领域的工作结合发挥作用

==*== Weaknesses
==-==    What are the main weaknesses that may prevent the paper from being
==-==    accepted (0-3 bullets).
==-== Markdown styling and LaTeX math supported.

1. 系统调用包含了复杂的调用过程，并非每个部分都能提供有效信息，而在网络子系统中有丰富的ebpf hook点，能够对网络处理过程进行更加细致的观测，论文中以系统调用作为hook点的粒度较粗
2. 使用ebpf的确不会带来较大的开销，但从内核中取出数据到用户态的这一过程仍然需要占用相当的资源，尤其与用户态的调度程序结合时，内核态与用户态的数据拷贝、同步处理等并不利于准确的调度决策

==*== Contributions (Novelty & Impact)
==-== Choices:
==-==    1. Supringly new contribution or likely to have a major impact on
==-==       future research and/or products, inspire new research, or start
==-==       a new line of research/products
==-==    2. New contribution or likely to impact future research and/or
==-==       products
==-==    3. Incremental improvement or likely to have a minor impact
==-==    4. No novelty or unlikely to have an impact
==-== Enter the number of your choice:

4

==*== How easy it is to read and understand the paper? (Writing quality)
==-== Choices:
==-==    1. Very clear: I had no trouble understanding the work
==-==    2. Could be better: some non-trivial bits are missing and/or
==-==       difficult to understand; the writing is rough in some places.
==-==    3. Below the bar: significant gaps in the presented ideas and/or
==-==       poor writing in many places.
==-== Enter the number of your choice:

1

==*== Reviewer expertise
==-== Choices:
==-==    1. Expert: I have written one or more papers on this topic and/or
==-==       I currently work in this area.
==-==    2. Knowledgeable: I used to work in this area and/or I try to keep
==-==       up with the literature but might not know the latest
==-==       developments.
==-==    3. Some familiarity: I have a passing knowledge of this topic but
==-==       do not follow the relevant literature.
==-==    4. No familiarity: I do not have any knowledge of this topic.
==-== Enter the number of your choice:

2

==*== Reviewer confidence
==-==    Note that confidence is entirely orthogonal to expertise. It is
==-==    absolutely okay to be an expert in the area of the paper yet have
==-==    limited confidence in the review (e.g., because the paper was
==-==    difficult to understand). Similarly, you can be very confident in
==-==    the review despite low expertise.
==-== Choices:
==-==    1. High: I understand the key aspects of the paper to a great
==-==       extent.
==-==    2. Medium: I understand much of the paper but not all of it.
==-==    3. Low: I did not understand the key aspects of the paper.
==-== Enter the number of your choice:

1

==*== Questions/Issues for the authors to address in the rebuttal/revision
==-==    Please raise specific issues and/or suggest specific improvements
==-==    that would influence your post-rebuttal overall merit. Please be
==-==    specific and realistic, keeping in mind that the authors will have
==-==    only 10 days for the revision.
==-== Markdown styling and LaTeX math supported.

- V部分中的公式推导需要更精确的符号说明，避免引起歧义

==*== Pre-rebuttal overall merit
==-== Choices:
==-==    1. Strong accept -- excellent paper that moves the needle in at
==-==       least one major dimension (e.g., radically new insights, new
==-==       research direction, methodological break-through). Must have in
==-==       the program and will champion the paper.
==-==    2. Accept -- high quality paper with minor issues that can be
==-==       easily overlooked. Should have in the program.
==-==    3. Weak accept -- solid paper with some deficiencies. May consider
==-==       including in the program.
==-==    4. Weak reject -- fair work with some flaws that are difficult to
==-==       overlook. Would prefer it doesn't appear in the program, but
==-==       will not fight strongly.
==-==    5. Reject -- serious problems that entirely compromise the paper.
==-==       Will fight against this paper.
==-== Enter the number of your choice:

3

==*== Impact of revision/rebuttal
==-== (hidden from authors)
==-==    How likely are you to change your overall merit based on the
==-==    revision/rebuttal?
==-== Choices:
==-==    1. Very likely
==-==    2. Somewhat likely
==-==    3. Somewhat unlikely
==-==    4. Very unlikely
==-== Enter the number of your choice:

3

==*== Comments for authors
==-==    Please provide your comments justifying your reasons for your
==-==    overall merit. The comments should be constructive and helpful to
==-==    the authors.
==-== Markdown styling and LaTeX math supported.

作者利用ebpf插桩从内核监测用户应用QoS，实现轻量的数据采集的同时不必侵入用户应用，然而从内核获取的系统调用action数据并不能直接反映出应用程序的QoS情况，作者提供了一系列算法用来从原始的内核监测指标来对request-level指标进行估算，在10种应用都能够得到较为准确的效果，充分说明的方法的有效性。然而论文中也存在一些不足，如在一些文本格式、公式说明上存在不规范、不准确的纰漏，在核心思路上，论文中使用与socket和异步IO相关的syscall action作为主要的hook点，这种方法基于一定的经验参考，在扩展性上存在一定的问题。总体而言，作者提供了一种从内核视角分析用户应用的思路，在QoS监测领域是有一定积极意义的贡献。

==*== Comments for PC
==-== (hidden from authors)
==-== Markdown styling and LaTeX math supported.



==*== Suggestion of reviewers
==-== (shown only to administrators)
==-==    Feel free to suggest PC members or external reviewers that you
==-==    believe should review this paper.   If you believe that the scope
==-==    of this work overlaps with another venue (e.g., SIGCOMM for a
==-==    networking paper), please provide the name of such venues where
==-==    external expertise can potentially help in reviewing the paper.
==-== Markdown styling and LaTeX math supported.



==+== Scratchpad (for unsaved private notes)

==+== End Review

