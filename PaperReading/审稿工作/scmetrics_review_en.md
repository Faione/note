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

1. Introduced a monitoring framework based on eBPF that can estimate request-level metrics from an application's syscall activity.
2. Proposed a set of algorithms for estimating request-level metrics and validated their effectiveness through experiments on 10 different applications. The model also allows for the inclusion of QoS (Quality of Service) metrics to improve estimation accuracy.

==*== Strengths
==-==    What are the main insights, contributions, results and other
==-==    strengths of the paper that may serve as the basis for acceptance
==-==    (1-3 bullets).
==-== Markdown styling and LaTeX math supported.

1. Utilized eBPF technology for kernel observation, eliminating the need for instrumenting user applications and offering lower performance overhead compared to performance counters.

2. Demonstrated the correlation between an application's system call activity and its request-level metrics, and designed algorithms for estimating request-level metrics based on throughput and latency.

3. Provided a software library for metric querying, which can be easily integrated with work in the scheduler domain for enhanced functionality.

==*== Weaknesses
==-==    What are the main weaknesses that may prevent the paper from being
==-==    accepted (0-3 bullets).
==-== Markdown styling and LaTeX math supported.

1. System calls involve complex invocation processes, and not every part can provide useful information. In contrast, the network subsystem has a rich set of eBPF hook points, allowing for more detailed observation of the network handling process. The paper's choice to use system calls as hook points is relatively coarse-grained.

2. While using eBPF does not incur significant overhead, the process of transferring data from the kernel to user space still requires substantial resources. This is especially the case when integrated with user-space schedulers. Issues like data copying and synchronization between kernel and user space are not conducive to making accurate scheduling decisions

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

1. Formula derivations need to provide more precise symbol definitions to avoid ambiguity and facilitate understanding.

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

2

==*== Comments for authors
==-==    Please provide your comments justifying your reasons for your
==-==    overall merit. The comments should be constructive and helpful to
==-==    the authors.
==-== Markdown styling and LaTeX math supported.

The authors utilize eBPF instrumentation to monitor user application QoS from the kernel, achieving lightweight data collection without invasive changes to the user application. However, syscall action data obtained from the kernel doesn't directly reflect the application's QoS condition. To address this, the authors offer a series of algorithms to estimate request-level metrics from the raw kernel monitoring indicators. The effectiveness of these methods is substantiated through tests on 10 different applications, showing relatively accurate results. 

Nevertheless, there are some weaknesses in the paper, such as irregularities and inaccuracies in text formatting and formula explanations. On the core conceptual front, the paper uses syscall actions related to sockets and asynchronous IO as the main hook points. This approach is based on certain experiential references, which pose issues in terms of scalability. 

Overall, the authors provide a perspective for analyzing user applications from the kernel viewpoint, making a positive contribution to the field of QoS monitoring.

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

