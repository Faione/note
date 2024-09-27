throughput

```
/usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.26.16) or chardet (3.0.4) doesn't match a supported version!
  RequestsDependencyWarning)
INFO:root:from 1712111986 to 1712112006, total: 0.006h
INFO:root:split to 1 batchs
INFO:root:all data fetched
INFO:root:all data formatted
INFO:root:collector initialized
INFO:root:1712112007 experiment start
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.196 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       61084 ops,   61131 (avg:   61131) ops/se[RUN #1 50%,   1 secs]  4 threads:      127648 ops,   66552 (avg:   63843) ops/se[RUN #1 75%,   2 secs]  4 threads:      194614 ops,   66954 (avg:   64880) ops/se[RUN #1 100%,   3 secs]  4 threads:      260563 ops,   65939 (avg:   65145) ops/s[RUN #1 100%,   4 secs]  0 threads:      260769 ops,   65939 (avg:   65067) ops/sec, 2.73MB/sec (avg: 2.70MB/sec),  3.03 (avg:  3.07) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         5937.40          ---          ---         3.46677         2.83100        13.50300        59.64700       456.70
Gets        59122.30        49.90     59072.40         3.03213         2.83100         5.56700        14.01500      2305.20
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      65059.71        49.90     59072.40         3.07179         2.83100         5.63100        16.51100      2761.89
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.196 --test-time 32 -t 1 -c 1
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   1 secs]  1 threads:        4236 ops,    4235 (avg:    4235) ops/sec[RUN #1 6%,   2 secs]  1 threads:        8505 ops,    4268 (avg:    4252) ops/sec[RUN #1 9%,   3 secs]  1 threads:       12766 ops,    4260 (avg:    4254) ops/sec[RUN #1 13%,   4 secs]  1 threads:       17021 ops,    4254 (avg:    4254) ops/se[RUN #1 16%,   5 secs]  1 threads:       21241 ops,    4219 (avg:    4247) ops/se[RUN #1 19%,   6 secs]  1 threads:       25434 ops,    4192 (avg:    4238) ops/se[RUN #1 22%,   7 secs]  1 threads:       29807 ops,    4372 (avg:    4257) ops/se[RUN #1 25%,   8 secs]  1 threads:       34184 ops,    4376 (avg:    4272) ops/se[RUN #1 28%,   9 secs]  1 threads:       38498 ops,    4313 (avg:    4277) ops/se[RUN #1 31%,  10 secs]  1 threads:       42687 ops,    4188 (avg:    4268) ops/se[RUN #1 34%,  11 secs]  1 threads:       46922 ops,    4234 (avg:    4265) ops/se[RUN #1 38%,  12 secs]  1 threads:       51211 ops,    4288 (avg:    4267) ops/se[RUN #1 41%,  13 secs]  1 threads:       55478 ops,    4266 (avg:    4267) ops/se[RUN #1 44%,  14 secs]  1 threads:       59742 ops,    4263 (avg:    4266) ops/se[RUN #1 47%,  15 secs]  1 threads:       63996 ops,    4253 (avg:    4265) ops/se[RUN #1 50%,  16 secs]  1 threads:       68246 ops,    4249 (avg:    4264) ops/se[RUN #1 53%,  17 secs]  1 threads:       72509 ops,    4262 (avg:    4264) ops/se[RUN #1 56%,  18 secs]  1 threads:       76700 ops,    4190 (avg:    4260) ops/se[RUN #1 59%,  19 secs]  1 threads:       80969 ops,    4268 (avg:    4261) ops/se[RUN #1 63%,  20 secs]  1 threads:       85261 ops,    4291 (avg:    4262) ops/se[RUN #1 66%,  21 secs]  1 threads:       89527 ops,    4265 (avg:    4262) ops/se[RUN #1 69%,  22 secs]  1 threads:       93786 ops,    4258 (avg:    4262) ops/se[RUN #1 72%,  23 secs]  1 threads:       98019 ops,    4232 (avg:    4261) ops/se[RUN #1 75%,  24 secs]  1 threads:      102289 ops,    4269 (avg:    4261) ops/se[RUN #1 78%,  25 secs]  1 threads:      106529 ops,    4239 (avg:    4260) ops/se[RUN #1 81%,  26 secs]  1 threads:      110769 ops,    4239 (avg:    4259) ops/se[RUN #1 84%,  27 secs]  1 threads:      115019 ops,    4249 (avg:    4259) ops/se[RUN #1 88%,  28 secs]  1 threads:      119298 ops,    4278 (avg:    4260) ops/se[RUN #1 91%,  29 secs]  1 threads:      123585 ops,    4286 (avg:    4261) ops/se[RUN #1 94%,  30 secs]  1 threads:      126936 ops,    3350 (avg:    4230) ops/se[RUN #1 97%,  31 secs]  1 threads:      131171 ops,    4234 (avg:    4230) ops/se[RUN #1 100%,  32 secs]  0 threads:      135366 ops,    4234 (avg:    4230) ops/sec, 179.79KB/sec (avg: 179.57KB/sec),  0.23 (avg:  0.23) msec latency

1         Threads
1         Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets          384.56          ---          ---         0.23489         0.22300         0.43100         0.71100        29.63
Gets         3845.57         4.41      3841.16         0.23401         0.22300         0.43100         0.95100       149.94
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals       4230.13         4.41      3841.16         0.23409         0.22300         0.43100         0.93500       179.57
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.196 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       66944 ops,   66996 (avg:   66996) ops/se[RUN #1 50%,   1 secs]  4 threads:      135025 ops,   68068 (avg:   67532) ops/se[RUN #1 75%,   2 secs]  4 threads:      202126 ops,   67090 (avg:   67385) ops/se[RUN #1 100%,   3 secs]  4 threads:      268841 ops,   66703 (avg:   67214) ops/s[RUN #1 100%,   4 secs]  0 threads:      269051 ops,   66703 (avg:   67088) ops/sec, 2.76MB/sec (avg: 2.78MB/sec),  3.00 (avg:  2.98) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         6118.72          ---          ---         2.99924         2.78300         7.03900        13.05500       470.69
Gets        60938.23        49.85     60888.38         2.97689         2.78300         5.43900        13.88700      2375.95
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      67056.95        49.85     60888.38         2.97893         2.78300         5.43900        13.82300      2846.63
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.196 --test-time 32 -t 1 -c 2
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:        8546 ops,    8546 (avg:    8546) ops/sec[RUN #1 6%,   2 secs]  1 threads:       16987 ops,    8440 (avg:    8493) ops/sec[RUN #1 9%,   3 secs]  1 threads:       25417 ops,    8429 (avg:    8471) ops/sec[RUN #1 13%,   4 secs]  1 threads:       33939 ops,    8521 (avg:    8484) ops/se[RUN #1 16%,   5 secs]  1 threads:       42496 ops,    8556 (avg:    8498) ops/se[RUN #1 19%,   6 secs]  1 threads:       50992 ops,    8495 (avg:    8498) ops/se[RUN #1 22%,   7 secs]  1 threads:       59394 ops,    8401 (avg:    8484) ops/se[RUN #1 25%,   8 secs]  1 threads:       67877 ops,    8482 (avg:    8483) ops/se[RUN #1 28%,   9 secs]  1 threads:       76245 ops,    8367 (avg:    8470) ops/se[RUN #1 31%,  10 secs]  1 threads:       84701 ops,    8454 (avg:    8469) ops/se[RUN #1 34%,  11 secs]  1 threads:       93131 ops,    8428 (avg:    8465) ops/se[RUN #1 38%,  12 secs]  1 threads:      101575 ops,    8443 (avg:    8463) ops/se[RUN #1 41%,  13 secs]  1 threads:      109901 ops,    8325 (avg:    8453) ops/se[RUN #1 44%,  14 secs]  1 threads:      118574 ops,    8672 (avg:    8468) ops/se[RUN #1 47%,  15 secs]  1 threads:      127129 ops,    8554 (avg:    8474) ops/se[RUN #1 50%,  16 secs]  1 threads:      135559 ops,    8429 (avg:    8471) ops/se[RUN #1 53%,  17 secs]  1 threads:      144016 ops,    8456 (avg:    8470) ops/se[RUN #1 56%,  18 secs]  1 threads:      152378 ops,    8361 (avg:    8464) ops/se[RUN #1 59%,  19 secs]  1 threads:      160827 ops,    8448 (avg:    8463) ops/se[RUN #1 63%,  20 secs]  1 threads:      169256 ops,    8428 (avg:    8461) ops/se[RUN #1 66%,  21 secs]  1 threads:      177749 ops,    8492 (avg:    8463) ops/se[RUN #1 69%,  22 secs]  1 threads:      186201 ops,    8451 (avg:    8462) ops/se[RUN #1 72%,  23 secs]  1 threads:      194667 ops,    8465 (avg:    8462) ops/se[RUN #1 75%,  24 secs]  1 threads:      203440 ops,    8772 (avg:    8475) ops/se[RUN #1 78%,  25 secs]  1 threads:      212076 ops,    8635 (avg:    8482) ops/se[RUN #1 81%,  26 secs]  1 threads:      220789 ops,    8712 (avg:    8491) ops/se[RUN #1 84%,  27 secs]  1 threads:      229296 ops,    8506 (avg:    8491) ops/se[RUN #1 88%,  28 secs]  1 threads:      237649 ops,    8352 (avg:    8486) ops/se[RUN #1 91%,  29 secs]  1 threads:      246025 ops,    8375 (avg:    8482) ops/se[RUN #1 94%,  30 secs]  1 threads:      254496 ops,    8470 (avg:    8482) ops/se[RUN #1 97%,  31 secs]  1 threads:      262954 ops,    8457 (avg:    8481) ops/se[RUN #1 100%,  32 secs]  0 threads:      271307 ops,    8457 (avg:    8478) ops/sec, 359.07KB/sec (avg: 359.90KB/sec),  0.23 (avg:  0.23) msec latency

1         Threads
2         Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets          770.77          ---          ---         0.23765         0.22300         0.43900         2.89500        59.38
Gets         7707.46         8.81      7698.65         0.23366         0.21500         0.42300         4.28700       300.52
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals       8478.23         8.81      7698.65         0.23402         0.21500         0.43100         4.12700       359.90
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.196 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       67177 ops,   67231 (avg:   67231) ops/se[RUN #1 50%,   1 secs]  4 threads:      134527 ops,   67334 (avg:   67283) ops/se[RUN #1 75%,   2 secs]  4 threads:      201490 ops,   66952 (avg:   67173) ops/se[RUN #1 100%,   3 secs]  4 threads:      268005 ops,   66505 (avg:   67006) ops/s[RUN #1 100%,   4 secs]  0 threads:      268215 ops,   66505 (avg:   66925) ops/sec, 2.75MB/sec (avg: 2.77MB/sec),  3.00 (avg:  2.99) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         6107.87          ---          ---         3.00371         2.79900         6.14300        13.18300       469.85
Gets        60807.48        49.90     60757.59         2.98472         2.78300         5.47100        13.43900      2370.85
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      66915.35        49.90     60757.59         2.98645         2.78300         5.47100        13.43900      2840.69
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.196 --test-time 32 -t 1 -c 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:       16834 ops,   16836 (avg:   16836) ops/sec[RUN #1 6%,   2 secs]  1 threads:       33128 ops,   16291 (avg:   16563) ops/sec[RUN #1 9%,   3 secs]  1 threads:       49244 ops,   16114 (avg:   16414) ops/sec[RUN #1 13%,   4 secs]  1 threads:       65397 ops,   16151 (avg:   16348) ops/se[RUN #1 16%,   5 secs]  1 threads:       81742 ops,   16342 (avg:   16347) ops/se[RUN #1 19%,   6 secs]  1 threads:       97889 ops,   16145 (avg:   16313) ops/se[RUN #1 22%,   7 secs]  1 threads:      113942 ops,   16050 (avg:   16275) ops/se[RUN #1 25%,   8 secs]  1 threads:      129808 ops,   15864 (avg:   16224) ops/se[RUN #1 28%,   9 secs]  1 threads:      145411 ops,   15601 (avg:   16155) ops/se[RUN #1 31%,  10 secs]  1 threads:      161023 ops,   15610 (avg:   16100) ops/se[RUN #1 34%,  11 secs]  1 threads:      176416 ops,   15391 (avg:   16036) ops/se[RUN #1 38%,  12 secs]  1 threads:      191638 ops,   15220 (avg:   15968) ops/se[RUN #1 41%,  13 secs]  1 threads:      206555 ops,   14915 (avg:   15887) ops/se[RUN #1 44%,  14 secs]  1 threads:      221617 ops,   15060 (avg:   15828) ops/se[RUN #1 47%,  15 secs]  1 threads:      237115 ops,   15496 (avg:   15806) ops/se[RUN #1 50%,  16 secs]  1 threads:      252736 ops,   15619 (avg:   15794) ops/se[RUN #1 53%,  17 secs]  1 threads:      268608 ops,   15870 (avg:   15798) ops/se[RUN #1 56%,  18 secs]  1 threads:      284252 ops,   15642 (avg:   15790) ops/se[RUN #1 59%,  19 secs]  1 threads:      299908 ops,   15654 (avg:   15782) ops/se[RUN #1 63%,  20 secs]  1 threads:      315439 ops,   15529 (avg:   15770) ops/se[RUN #1 66%,  21 secs]  1 threads:      331268 ops,   15827 (avg:   15772) ops/se[RUN #1 69%,  22 secs]  1 threads:      347357 ops,   16087 (avg:   15787) ops/se[RUN #1 72%,  23 secs]  1 threads:      363262 ops,   15902 (avg:   15792) ops/se[RUN #1 75%,  24 secs]  1 threads:      378927 ops,   15662 (avg:   15786) ops/se[RUN #1 78%,  25 secs]  1 threads:      394701 ops,   15772 (avg:   15786) ops/se[RUN #1 81%,  26 secs]  1 threads:      410264 ops,   15561 (avg:   15777) ops/se[RUN #1 84%,  27 secs]  1 threads:      426112 ops,   15846 (avg:   15780) ops/se[RUN #1 88%,  28 secs]  1 threads:      441219 ops,   15105 (avg:   15756) ops/se[RUN #1 91%,  29 secs]  1 threads:      456543 ops,   15322 (avg:   15741) ops/se[RUN #1 94%,  30 secs]  1 threads:      472365 ops,   15820 (avg:   15743) ops/se[RUN #1 97%,  31 secs]  1 threads:      488505 ops,   16138 (avg:   15756) ops/se[RUN #1 100%,  32 secs]  0 threads:      504275 ops,   16138 (avg:   15758) ops/sec, 684.82KB/sec (avg: 668.95KB/sec),  0.25 (avg:  0.25) msec latency

1         Threads
4         Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         1432.67          ---          ---         0.25773         0.23100         0.32700         8.44700       110.37
Gets        14325.70        16.75     14308.95         0.25190         0.22300         0.31100         8.25500       558.58
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      15758.37        16.75     14308.95         0.25243         0.23100         0.31100         8.25500       668.95
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.196 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       66000 ops,   66053 (avg:   66053) ops/se[RUN #1 50%,   1 secs]  4 threads:      131747 ops,   65734 (avg:   65893) ops/se[RUN #1 75%,   2 secs]  4 threads:      196204 ops,   64444 (avg:   65410) ops/se[RUN #1 100%,   3 secs]  4 threads:      260709 ops,   64493 (avg:   65181) ops/s[RUN #1 100%,   4 secs]  0 threads:      260909 ops,   64493 (avg:   65094) ops/sec, 2.67MB/sec (avg: 2.70MB/sec),  3.10 (avg:  3.07) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         5940.08          ---          ---         3.12091         2.87900         8.31900        16.51100       456.90
Gets        59151.07        49.90     59101.17         3.06530         2.87900         5.63100        14.52700      2306.32
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      65091.14        49.90     59101.17         3.07037         2.87900         5.66300        14.71900      2763.22
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.196 --test-time 32 -t 1 -c 8
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:       24465 ops,   24470 (avg:   24470) ops/sec[RUN #1 6%,   1 secs]  1 threads:       49183 ops,   24715 (avg:   24592) ops/sec[RUN #1 9%,   3 secs]  1 threads:       74856 ops,   25670 (avg:   24951) ops/sec[RUN #1 13%,   4 secs]  1 threads:       98761 ops,   23902 (avg:   24689) ops/se[RUN #1 16%,   5 secs]  1 threads:      122499 ops,   23735 (avg:   24498) ops/se[RUN #1 19%,   6 secs]  1 threads:      147380 ops,   24878 (avg:   24562) ops/se[RUN #1 22%,   7 secs]  1 threads:      171366 ops,   23983 (avg:   24479) ops/se[RUN #1 25%,   8 secs]  1 threads:      196223 ops,   24853 (avg:   24526) ops/se[RUN #1 28%,   9 secs]  1 threads:      223339 ops,   27112 (avg:   24813) ops/se[RUN #1 31%,  10 secs]  1 threads:      257255 ops,   33912 (avg:   25723) ops/se[RUN #1 34%,  11 secs]  1 threads:      292631 ops,   35372 (avg:   26600) ops/se[RUN #1 38%,  12 secs]  1 threads:      323889 ops,   31254 (avg:   26988) ops/se[RUN #1 41%,  13 secs]  1 threads:      352428 ops,   28535 (avg:   27107) ops/se[RUN #1 44%,  14 secs]  1 threads:      381521 ops,   29089 (avg:   27248) ops/se[RUN #1 47%,  15 secs]  1 threads:      410765 ops,   29240 (avg:   27381) ops/se[RUN #1 50%,  16 secs]  1 threads:      439019 ops,   28251 (avg:   27436) ops/se[RUN #1 53%,  17 secs]  1 threads:      464210 ops,   25188 (avg:   27303) ops/se[RUN #1 56%,  18 secs]  1 threads:      488461 ops,   24248 (avg:   27134) ops/se[RUN #1 59%,  19 secs]  1 threads:      517139 ops,   28674 (avg:   27215) ops/se[RUN #1 63%,  20 secs]  1 threads:      543515 ops,   26372 (avg:   27173) ops/se[RUN #1 66%,  21 secs]  1 threads:      569937 ops,   26419 (avg:   27137) ops/se[RUN #1 69%,  22 secs]  1 threads:      596101 ops,   26161 (avg:   27092) ops/se[RUN #1 72%,  23 secs]  1 threads:      624290 ops,   28185 (avg:   27140) ops/se[RUN #1 75%,  24 secs]  1 threads:      651008 ops,   26715 (avg:   27122) ops/se[RUN #1 78%,  25 secs]  1 threads:      676126 ops,   25115 (avg:   27042) ops/se[RUN #1 81%,  26 secs]  1 threads:      702626 ops,   26497 (avg:   27021) ops/se[RUN #1 84%,  27 secs]  1 threads:      732948 ops,   30318 (avg:   27143) ops/se[RUN #1 88%,  28 secs]  1 threads:      763405 ops,   30454 (avg:   27261) ops/se[RUN #1 91%,  29 secs]  1 threads:      793944 ops,   30535 (avg:   27374) ops/se[RUN #1 94%,  30 secs]  1 threads:      825595 ops,   31647 (avg:   27517) ops/se[RUN #1 97%,  31 secs]  1 threads:      855769 ops,   30170 (avg:   27602) ops/se[RUN #1 100%,  32 secs]  0 threads:      885153 ops,   30170 (avg:   27660) ops/sec, 1.25MB/sec (avg: 1.15MB/sec),  0.26 (avg:  0.29) msec latency

1         Threads
8         Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         2514.69          ---          ---         0.29161         0.26300         0.40700         9.59900       193.73
Gets        25145.70        29.47     25116.24         0.28832         0.26300         0.39900         9.66300       980.47
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      27660.40        29.47     25116.24         0.28862         0.26300         0.39900         9.66300      1174.20
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.196 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       64583 ops,   64636 (avg:   64636) ops/se[RUN #1 50%,   1 secs]  4 threads:      128066 ops,   63471 (avg:   64053) ops/se[RUN #1 75%,   2 secs]  4 threads:      192662 ops,   64584 (avg:   64230) ops/se[RUN #1 100%,   3 secs]  4 threads:      256693 ops,   64020 (avg:   64177) ops/s[RUN #1 100%,   4 secs]  0 threads:      256896 ops,   64020 (avg:   64103) ops/sec, 2.65MB/sec (avg: 2.66MB/sec),  3.12 (avg:  3.12) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         5849.83          ---          ---         3.13023         2.94300         6.33500        14.07900       449.94
Gets        58249.00        49.90     58199.10         3.11663         2.94300         5.75900        14.20700      2271.23
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      64098.83        49.90     58199.10         3.11787         2.94300         5.75900        14.20700      2721.17
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.196 --test-time 32 -t 1 -c 16
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:       45786 ops,   45802 (avg:   45802) ops/sec[RUN #1 6%,   1 secs]  1 threads:      102099 ops,   56306 (avg:   51055) ops/sec[RUN #1 9%,   2 secs]  1 threads:      158472 ops,   56367 (avg:   52826) ops/sec[RUN #1 12%,   3 secs]  1 threads:      214677 ops,   56200 (avg:   53670) ops/se[RUN #1 16%,   5 secs]  1 threads:      270747 ops,   56064 (avg:   54149) ops/se[RUN #1 19%,   6 secs]  1 threads:      325924 ops,   55169 (avg:   54319) ops/se[RUN #1 22%,   7 secs]  1 threads:      382018 ops,   56086 (avg:   54571) ops/se[RUN #1 25%,   8 secs]  1 threads:      437928 ops,   55903 (avg:   54738) ops/se[RUN #1 28%,   9 secs]  1 threads:      494026 ops,   56092 (avg:   54888) ops/se[RUN #1 31%,  10 secs]  1 threads:      550260 ops,   56228 (avg:   55022) ops/se[RUN #1 34%,  11 secs]  1 threads:      606200 ops,   55934 (avg:   55105) ops/se[RUN #1 38%,  12 secs]  1 threads:      662136 ops,   55930 (avg:   55174) ops/se[RUN #1 41%,  13 secs]  1 threads:      718261 ops,   56120 (avg:   55247) ops/se[RUN #1 44%,  14 secs]  1 threads:      774346 ops,   56079 (avg:   55306) ops/se[RUN #1 47%,  15 secs]  1 threads:      830451 ops,   56099 (avg:   55359) ops/se[RUN #1 50%,  16 secs]  1 threads:      886594 ops,   56138 (avg:   55408) ops/se[RUN #1 53%,  17 secs]  1 threads:      942646 ops,   56047 (avg:   55445) ops/se[RUN #1 56%,  18 secs]  1 threads:      998765 ops,   56113 (avg:   55482) ops/se[RUN #1 59%,  19 secs]  1 threads:     1054964 ops,   56193 (avg:   55520) ops/se[RUN #1 63%,  20 secs]  1 threads:     1111114 ops,   56145 (avg:   55551) ops/se[RUN #1 66%,  21 secs]  1 threads:     1167215 ops,   56095 (avg:   55577) ops/se[RUN #1 69%,  22 secs]  1 threads:     1223222 ops,   56001 (avg:   55596) ops/se[RUN #1 72%,  23 secs]  1 threads:     1279309 ops,   56081 (avg:   55617) ops/se[RUN #1 75%,  24 secs]  1 threads:     1335544 ops,   56229 (avg:   55643) ops/se[RUN #1 78%,  25 secs]  1 threads:     1391583 ops,   56033 (avg:   55658) ops/se[RUN #1 81%,  26 secs]  1 threads:     1447643 ops,   56054 (avg:   55674) ops/se[RUN #1 84%,  27 secs]  1 threads:     1503865 ops,   56216 (avg:   55694) ops/se[RUN #1 88%,  28 secs]  1 threads:     1560060 ops,   56189 (avg:   55711) ops/se[RUN #1 91%,  29 secs]  1 threads:     1616376 ops,   56310 (avg:   55732) ops/se[RUN #1 94%,  30 secs]  1 threads:     1672605 ops,   56223 (avg:   55748) ops/se[RUN #1 97%,  31 secs]  1 threads:     1728898 ops,   56287 (avg:   55766) ops/se[RUN #1 100%,  32 secs]  0 threads:     1785162 ops,   56287 (avg:   55784) ops/sec, 2.33MB/sec (avg: 2.31MB/sec),  0.28 (avg:  0.29) msec latency

1         Threads
16        Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         5235.17          ---          ---         0.28974         0.28700         0.35100         0.64700       403.30
Gets        52348.99        61.06     52287.92         0.28639         0.28700         0.35100         0.65500      2041.16
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      57584.15        61.06     52287.92         0.28670         0.28700         0.35100         0.64700      2444.47
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.196 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:      110384 ops,  110476 (avg:  110476) ops/se[RUN #1 50%,   1 secs]  4 threads:      220579 ops,  110177 (avg:  110327) ops/se[RUN #1 75%,   2 secs]  4 threads:      330586 ops,  109989 (avg:  110214) ops/se[RUN #1 100%,   3 secs]  4 threads:      441812 ops,  111210 (avg:  110463) ops/s[RUN #1 100%,   4 secs]  0 threads:      442029 ops,  111210 (avg:  110385) ops/sec, 4.61MB/sec (avg: 4.58MB/sec),  1.80 (avg:  1.81) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets        10059.10          ---          ---         1.81454         1.71100         3.05500        12.15900       774.14
Gets       100331.25       149.84    100181.41         1.81058         1.71100         2.87900        12.22300      3913.92
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals     110390.35       149.84    100181.41         1.81094         1.71100         2.89500        12.22300      4688.06
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.196 --test-time 32 -t 1 -c 32
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:       43694 ops,   43722 (avg:   43722) ops/sec[RUN #1 6%,   1 secs]  1 threads:       88359 ops,   44659 (avg:   44190) ops/sec[RUN #1 9%,   2 secs]  1 threads:      132759 ops,   44394 (avg:   44258) ops/sec[RUN #1 12%,   3 secs]  1 threads:      187592 ops,   54827 (avg:   46901) ops/se[RUN #1 16%,   4 secs]  1 threads:      240992 ops,   53394 (avg:   48200) ops/se[RUN #1 19%,   5 secs]  1 threads:      298438 ops,   57438 (avg:   49740) ops/se[RUN #1 22%,   7 secs]  1 threads:      352222 ops,   53778 (avg:   50317) ops/se[RUN #1 25%,   8 secs]  1 threads:      409435 ops,   57206 (avg:   51178) ops/se[RUN #1 28%,   9 secs]  1 threads:      467621 ops,   58179 (avg:   51956) ops/se[RUN #1 31%,  10 secs]  1 threads:      525698 ops,   58071 (avg:   52567) ops/se[RUN #1 34%,  11 secs]  1 threads:      583940 ops,   58235 (avg:   53083) ops/se[RUN #1 38%,  12 secs]  1 threads:      632612 ops,   48666 (avg:   52715) ops/se[RUN #1 41%,  13 secs]  1 threads:      681585 ops,   48967 (avg:   52426) ops/se[RUN #1 44%,  14 secs]  1 threads:      735653 ops,   54062 (avg:   52543) ops/se[RUN #1 47%,  15 secs]  1 threads:      792308 ops,   56649 (avg:   52817) ops/se[RUN #1 50%,  16 secs]  1 threads:      851251 ops,   58937 (avg:   53199) ops/se[RUN #1 53%,  17 secs]  1 threads:      909782 ops,   58524 (avg:   53513) ops/se[RUN #1 56%,  18 secs]  1 threads:      967406 ops,   57618 (avg:   53741) ops/se[RUN #1 59%,  19 secs]  1 threads:     1016110 ops,   48698 (avg:   53475) ops/se[RUN #1 63%,  20 secs]  1 threads:     1073991 ops,   57875 (avg:   53695) ops/se[RUN #1 66%,  21 secs]  1 threads:     1132547 ops,   58549 (avg:   53926) ops/se[RUN #1 69%,  22 secs]  1 threads:     1191423 ops,   58870 (avg:   54151) ops/se[RUN #1 72%,  23 secs]  1 threads:     1248412 ops,   56982 (avg:   54274) ops/se[RUN #1 75%,  24 secs]  1 threads:     1305794 ops,   57375 (avg:   54403) ops/se[RUN #1 78%,  25 secs]  1 threads:     1364357 ops,   58557 (avg:   54570) ops/se[RUN #1 81%,  26 secs]  1 threads:     1422646 ops,   58283 (avg:   54712) ops/se[RUN #1 84%,  27 secs]  1 threads:     1479920 ops,   57268 (avg:   54807) ops/se[RUN #1 88%,  28 secs]  1 threads:     1536860 ops,   56934 (avg:   54883) ops/se[RUN #1 91%,  29 secs]  1 threads:     1592771 ops,   55905 (avg:   54918) ops/se[RUN #1 94%,  30 secs]  1 threads:     1651743 ops,   58965 (avg:   55053) ops/se[RUN #1 97%,  31 secs]  1 threads:     1707590 ops,   55841 (avg:   55079) ops/se[RUN #1 100%,  32 secs]  1 threads:     1754394 ops,   46836 (avg:   54821) ops/s[RUN #1 100%,  32 secs]  0 threads:     1754409 ops,   46836 (avg:   54821) ops/sec, 1.94MB/sec (avg: 2.27MB/sec),  0.68 (avg:  0.58) msec latency

1         Threads
32        Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         4984.15          ---          ---         0.58692         0.55100         1.23900         8.63900       383.95
Gets        49836.98        51.71     49785.27         0.58325         0.55100         1.23100         8.63900      1943.00
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      54821.14        51.71     49785.27         0.58358         0.55100         1.23100         8.63900      2326.95
```

response

```
/usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.26.16) or chardet (3.0.4) doesn't match a supported version!
  RequestsDependencyWarning)
INFO:root:from 1712112161 to 1712112181, total: 0.006h
INFO:root:split to 1 batchs
INFO:root:all data fetched
INFO:root:all data formatted
INFO:root:collector initialized
INFO:root:1712112182 experiment start
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.197 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       68651 ops,   68708 (avg:   68708) ops/se[RUN #1 50%,   1 secs]  4 threads:      140186 ops,   71521 (avg:   70115) ops/se[RUN #1 75%,   2 secs]  4 threads:      210905 ops,   70703 (avg:   70311) ops/se[RUN #1 100%,   3 secs]  4 threads:      281213 ops,   70296 (avg:   70307) ops/s[RUN #1 100%,   4 secs]  0 threads:      281431 ops,   70296 (avg:   70227) ops/sec, 2.91MB/sec (avg: 2.91MB/sec),  2.84 (avg:  2.85) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         6407.73          ---          ---         2.96758         2.62300        10.75100        22.01500       492.98
Gets        63820.99        49.91     63771.09         2.83402         2.62300         5.37500        13.43900      2488.23
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      70228.72        49.91     63771.09         2.84620         2.62300         5.43900        15.16700      2981.21
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.197 --test-time 32 -t 1 -c 1
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   1 secs]  1 threads:        4341 ops,    4340 (avg:    4340) ops/sec[RUN #1 6%,   2 secs]  1 threads:        8681 ops,    4339 (avg:    4340) ops/sec[RUN #1 9%,   3 secs]  1 threads:       12998 ops,    4316 (avg:    4332) ops/sec[RUN #1 13%,   4 secs]  1 threads:       17336 ops,    4337 (avg:    4333) ops/se[RUN #1 16%,   5 secs]  1 threads:       21716 ops,    4379 (avg:    4342) ops/se[RUN #1 19%,   6 secs]  1 threads:       26109 ops,    4392 (avg:    4351) ops/se[RUN #1 22%,   7 secs]  1 threads:       30506 ops,    4396 (avg:    4357) ops/se[RUN #1 25%,   8 secs]  1 threads:       34914 ops,    4407 (avg:    4363) ops/se[RUN #1 28%,   9 secs]  1 threads:       39400 ops,    4485 (avg:    4377) ops/se[RUN #1 31%,  10 secs]  1 threads:       43823 ops,    4422 (avg:    4381) ops/se[RUN #1 34%,  11 secs]  1 threads:       48267 ops,    4443 (avg:    4387) ops/se[RUN #1 38%,  12 secs]  1 threads:       52713 ops,    4445 (avg:    4392) ops/se[RUN #1 41%,  13 secs]  1 threads:       57140 ops,    4426 (avg:    4395) ops/se[RUN #1 44%,  14 secs]  1 threads:       61579 ops,    4438 (avg:    4398) ops/se[RUN #1 47%,  15 secs]  1 threads:       66024 ops,    4444 (avg:    4401) ops/se[RUN #1 50%,  16 secs]  1 threads:       70474 ops,    4449 (avg:    4404) ops/se[RUN #1 53%,  17 secs]  1 threads:       74930 ops,    4455 (avg:    4407) ops/se[RUN #1 56%,  18 secs]  1 threads:       79379 ops,    4448 (avg:    4409) ops/se[RUN #1 59%,  19 secs]  1 threads:       83831 ops,    4451 (avg:    4411) ops/se[RUN #1 63%,  20 secs]  1 threads:       88292 ops,    4460 (avg:    4414) ops/se[RUN #1 66%,  21 secs]  1 threads:       92749 ops,    4456 (avg:    4416) ops/se[RUN #1 69%,  22 secs]  1 threads:       97202 ops,    4452 (avg:    4417) ops/se[RUN #1 72%,  23 secs]  1 threads:      101648 ops,    4445 (avg:    4419) ops/se[RUN #1 75%,  24 secs]  1 threads:      106093 ops,    4444 (avg:    4420) ops/se[RUN #1 78%,  25 secs]  1 threads:      110553 ops,    4459 (avg:    4421) ops/se[RUN #1 81%,  26 secs]  1 threads:      115037 ops,    4483 (avg:    4424) ops/se[RUN #1 84%,  27 secs]  1 threads:      119501 ops,    4463 (avg:    4425) ops/se[RUN #1 88%,  28 secs]  1 threads:      123968 ops,    4466 (avg:    4427) ops/se[RUN #1 91%,  29 secs]  1 threads:      128440 ops,    4471 (avg:    4428) ops/se[RUN #1 94%,  30 secs]  1 threads:      132909 ops,    4468 (avg:    4429) ops/se[RUN #1 97%,  31 secs]  1 threads:      137367 ops,    4457 (avg:    4430) ops/se[RUN #1 100%,  32 secs]  0 threads:      141810 ops,    4457 (avg:    4431) ops/sec, 189.10KB/sec (avg: 188.12KB/sec),  0.22 (avg:  0.22) msec latency

1         Threads
1         Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets          402.87          ---          ---         0.22741         0.22300         0.26300         2.28700        31.04
Gets         4028.62         4.78      4023.84         0.22305         0.21500         0.26300         2.04700       157.09
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals       4431.49         4.78      4023.84         0.22345         0.21500         0.26300         2.06300       188.12
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.197 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       70430 ops,   70487 (avg:   70487) ops/se[RUN #1 50%,   1 secs]  4 threads:      142653 ops,   72209 (avg:   71349) ops/se[RUN #1 75%,   2 secs]  4 threads:      246016 ops,  103345 (avg:   82017) ops/se[RUN #1 100%,   3 secs]  4 threads:      350314 ops,  104281 (avg:   87585) ops/s[RUN #1 100%,   4 secs]  0 threads:      350521 ops,  104281 (avg:   87487) ops/sec, 4.33MB/sec (avg: 3.63MB/sec),  1.92 (avg:  2.28) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         7974.60          ---          ---         2.30828         2.25500         5.37500        11.77500       613.69
Gets        79492.18        99.81     79392.37         2.28250         2.25500         5.08700        11.00700      3100.73
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      87466.77        99.81     79392.37         2.28485         2.25500         5.11900        11.07100      3714.42
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.197 --test-time 32 -t 1 -c 2
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:        7848 ops,    7850 (avg:    7850) ops/sec[RUN #1 6%,   1 secs]  1 threads:       15646 ops,    7797 (avg:    7823) ops/sec[RUN #1 9%,   2 secs]  1 threads:       23553 ops,    7906 (avg:    7851) ops/sec[RUN #1 13%,   4 secs]  1 threads:       31349 ops,    7795 (avg:    7837) ops/se[RUN #1 16%,   5 secs]  1 threads:       38984 ops,    7634 (avg:    7796) ops/se[RUN #1 19%,   6 secs]  1 threads:       46854 ops,    7869 (avg:    7808) ops/se[RUN #1 22%,   7 secs]  1 threads:       54760 ops,    7904 (avg:    7822) ops/se[RUN #1 25%,   8 secs]  1 threads:       62970 ops,    8208 (avg:    7870) ops/se[RUN #1 28%,   9 secs]  1 threads:       71304 ops,    8333 (avg:    7922) ops/se[RUN #1 31%,  10 secs]  1 threads:       79636 ops,    8330 (avg:    7962) ops/se[RUN #1 34%,  11 secs]  1 threads:       87914 ops,    8276 (avg:    7991) ops/se[RUN #1 38%,  12 secs]  1 threads:       96158 ops,    8243 (avg:    8012) ops/se[RUN #1 41%,  13 secs]  1 threads:      104454 ops,    8295 (avg:    8034) ops/se[RUN #1 44%,  14 secs]  1 threads:      112724 ops,    8269 (avg:    8051) ops/se[RUN #1 47%,  15 secs]  1 threads:      120879 ops,    8153 (avg:    8057) ops/se[RUN #1 50%,  16 secs]  1 threads:      129049 ops,    8168 (avg:    8064) ops/se[RUN #1 53%,  17 secs]  1 threads:      137262 ops,    8212 (avg:    8073) ops/se[RUN #1 56%,  18 secs]  1 threads:      145412 ops,    8149 (avg:    8077) ops/se[RUN #1 59%,  19 secs]  1 threads:      153573 ops,    8159 (avg:    8082) ops/se[RUN #1 63%,  20 secs]  1 threads:      161720 ops,    8146 (avg:    8085) ops/se[RUN #1 66%,  21 secs]  1 threads:      169831 ops,    8110 (avg:    8086) ops/se[RUN #1 69%,  22 secs]  1 threads:      177541 ops,    7709 (avg:    8069) ops/se[RUN #1 72%,  23 secs]  1 threads:      185103 ops,    7561 (avg:    8047) ops/se[RUN #1 75%,  24 secs]  1 threads:      192705 ops,    7601 (avg:    8028) ops/se[RUN #1 78%,  25 secs]  1 threads:      200387 ops,    7681 (avg:    8014) ops/se[RUN #1 81%,  26 secs]  1 threads:      208231 ops,    7843 (avg:    8008) ops/se[RUN #1 84%,  27 secs]  1 threads:      216086 ops,    7854 (avg:    8002) ops/se[RUN #1 88%,  28 secs]  1 threads:      223950 ops,    7863 (avg:    7997) ops/se[RUN #1 91%,  29 secs]  1 threads:      231839 ops,    7888 (avg:    7993) ops/se[RUN #1 94%,  30 secs]  1 threads:      239726 ops,    7886 (avg:    7990) ops/se[RUN #1 97%,  31 secs]  1 threads:      247574 ops,    7847 (avg:    7985) ops/se[RUN #1 100%,  32 secs]  0 threads:      255460 ops,    7847 (avg:    7982) ops/sec, 333.25KB/sec (avg: 338.89KB/sec),  0.25 (avg:  0.25) msec latency

1         Threads
2         Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets          725.73          ---          ---         0.25261         0.23900         0.33500         2.60700        55.91
Gets         7257.21         8.84      7248.37         0.24754         0.23900         0.31900         2.49500       282.98
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals       7982.94         8.84      7248.37         0.24800         0.23900         0.31900         2.51100       338.89
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.197 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       71552 ops,   71603 (avg:   71603) ops/se[RUN #1 50%,   1 secs]  4 threads:      141654 ops,   70088 (avg:   70845) ops/se[RUN #1 75%,   2 secs]  4 threads:      212185 ops,   70518 (avg:   70736) ops/se[RUN #1 100%,   3 secs]  4 threads:      284333 ops,   72136 (avg:   71086) ops/s[RUN #1 100%,   4 secs]  0 threads:      284531 ops,   72136 (avg:   70986) ops/sec, 2.99MB/sec (avg: 2.94MB/sec),  2.77 (avg:  2.81) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         6475.18          ---          ---         2.85333         2.59100         6.27100        15.10300       498.19
Gets        64497.91        49.89     64448.02         2.81166         2.59100         5.24700        14.46300      2514.59
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      70973.10        49.89     64448.02         2.81547         2.59100         5.31100        14.59100      3012.77
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.197 --test-time 32 -t 1 -c 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:       15455 ops,   15456 (avg:   15456) ops/sec[RUN #1 6%,   2 secs]  1 threads:       30869 ops,   15411 (avg:   15434) ops/sec[RUN #1 9%,   3 secs]  1 threads:       46218 ops,   15347 (avg:   15405) ops/sec[RUN #1 13%,   4 secs]  1 threads:       61480 ops,   15260 (avg:   15368) ops/se[RUN #1 16%,   5 secs]  1 threads:       76824 ops,   15341 (avg:   15363) ops/se[RUN #1 19%,   6 secs]  1 threads:       91339 ops,   14513 (avg:   15221) ops/se[RUN #1 22%,   7 secs]  1 threads:      105489 ops,   14148 (avg:   15068) ops/se[RUN #1 25%,   8 secs]  1 threads:      121005 ops,   15514 (avg:   15124) ops/se[RUN #1 28%,   9 secs]  1 threads:      136825 ops,   15818 (avg:   15201) ops/se[RUN #1 31%,  10 secs]  1 threads:      152656 ops,   15829 (avg:   15264) ops/se[RUN #1 34%,  11 secs]  1 threads:      168663 ops,   16005 (avg:   15331) ops/se[RUN #1 38%,  12 secs]  1 threads:      185011 ops,   16346 (avg:   15415) ops/se[RUN #1 41%,  13 secs]  1 threads:      201401 ops,   16388 (avg:   15490) ops/se[RUN #1 44%,  14 secs]  1 threads:      217763 ops,   16360 (avg:   15552) ops/se[RUN #1 47%,  15 secs]  1 threads:      234106 ops,   16341 (avg:   15605) ops/se[RUN #1 50%,  16 secs]  1 threads:      250343 ops,   16235 (avg:   15644) ops/se[RUN #1 53%,  17 secs]  1 threads:      266701 ops,   16356 (avg:   15686) ops/se[RUN #1 56%,  18 secs]  1 threads:      282934 ops,   16231 (avg:   15716) ops/se[RUN #1 59%,  19 secs]  1 threads:      299234 ops,   16298 (avg:   15747) ops/se[RUN #1 63%,  20 secs]  1 threads:      314086 ops,   14850 (avg:   15702) ops/se[RUN #1 66%,  21 secs]  1 threads:      329935 ops,   15847 (avg:   15709) ops/se[RUN #1 69%,  22 secs]  1 threads:      346270 ops,   16333 (avg:   15737) ops/se[RUN #1 72%,  23 secs]  1 threads:      362414 ops,   16142 (avg:   15755) ops/se[RUN #1 75%,  24 secs]  1 threads:      377714 ops,   15298 (avg:   15736) ops/se[RUN #1 78%,  25 secs]  1 threads:      392955 ops,   15239 (avg:   15716) ops/se[RUN #1 81%,  26 secs]  1 threads:      408201 ops,   15244 (avg:   15698) ops/se[RUN #1 84%,  27 secs]  1 threads:      424228 ops,   16025 (avg:   15710) ops/se[RUN #1 88%,  28 secs]  1 threads:      440165 ops,   15935 (avg:   15718) ops/se[RUN #1 91%,  29 secs]  1 threads:      456119 ops,   15952 (avg:   15726) ops/se[RUN #1 94%,  30 secs]  1 threads:      472044 ops,   15923 (avg:   15733) ops/se[RUN #1 97%,  31 secs]  1 threads:      488137 ops,   16091 (avg:   15744) ops/se[RUN #1 100%,  32 secs]  0 threads:      504101 ops,   16091 (avg:   15752) ops/sec, 682.84KB/sec (avg: 668.74KB/sec),  0.25 (avg:  0.25) msec latency

1         Threads
4         Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         1432.12          ---          ---         0.25602         0.23900         0.67100         2.81500       110.33
Gets        14320.61        17.62     14302.99         0.25218         0.23100         0.61500         2.84700       558.41
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      15752.73        17.62     14302.99         0.25253         0.23100         0.61500         2.83100       668.74
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.197 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       70105 ops,   70164 (avg:   70164) ops/se[RUN #1 50%,   1 secs]  4 threads:      141063 ops,   70944 (avg:   70554) ops/se[RUN #1 75%,   2 secs]  4 threads:      212545 ops,   71469 (avg:   70859) ops/se[RUN #1 100%,   3 secs]  4 threads:      283372 ops,   70816 (avg:   70848) ops/s[RUN #1 100%,   4 secs]  0 threads:      283575 ops,   70816 (avg:   70789) ops/sec, 2.93MB/sec (avg: 2.93MB/sec),  2.82 (avg:  2.82) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         6460.52          ---          ---         2.85470         2.60700         6.43100        12.41500       497.05
Gets        64345.73        49.94     64295.80         2.82031         2.59100         5.15100        12.15900      2508.68
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      70806.25        49.94     64295.80         2.82345         2.59100         5.27900        12.15900      3005.73
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.197 --test-time 32 -t 1 -c 8
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:       29391 ops,   29397 (avg:   29397) ops/sec[RUN #1 6%,   1 secs]  1 threads:       58375 ops,   28980 (avg:   29188) ops/sec[RUN #1 9%,   3 secs]  1 threads:       88330 ops,   29950 (avg:   29442) ops/sec[RUN #1 13%,   4 secs]  1 threads:      117494 ops,   29160 (avg:   29372) ops/se[RUN #1 16%,   5 secs]  1 threads:      146436 ops,   28938 (avg:   29285) ops/se[RUN #1 19%,   6 secs]  1 threads:      174614 ops,   28175 (avg:   29100) ops/se[RUN #1 22%,   7 secs]  1 threads:      202567 ops,   27949 (avg:   28936) ops/se[RUN #1 25%,   8 secs]  1 threads:      232298 ops,   29727 (avg:   29034) ops/se[RUN #1 28%,   9 secs]  1 threads:      262275 ops,   29973 (avg:   29139) ops/se[RUN #1 31%,  10 secs]  1 threads:      290610 ops,   28331 (avg:   29058) ops/se[RUN #1 34%,  11 secs]  1 threads:      319196 ops,   28582 (avg:   29015) ops/se[RUN #1 38%,  12 secs]  1 threads:      347874 ops,   28675 (avg:   28986) ops/se[RUN #1 41%,  13 secs]  1 threads:      377808 ops,   29930 (avg:   29059) ops/se[RUN #1 44%,  14 secs]  1 threads:      405964 ops,   28152 (avg:   28994) ops/se[RUN #1 47%,  15 secs]  1 threads:      430894 ops,   24926 (avg:   28723) ops/se[RUN #1 50%,  16 secs]  1 threads:      454721 ops,   23824 (avg:   28417) ops/se[RUN #1 53%,  17 secs]  1 threads:      478699 ops,   23975 (avg:   28156) ops/se[RUN #1 56%,  18 secs]  1 threads:      503484 ops,   24782 (avg:   27968) ops/se[RUN #1 59%,  19 secs]  1 threads:      528742 ops,   25255 (avg:   27825) ops/se[RUN #1 63%,  20 secs]  1 threads:      552943 ops,   24198 (avg:   27644) ops/se[RUN #1 66%,  21 secs]  1 threads:      577219 ops,   24273 (avg:   27483) ops/se[RUN #1 69%,  22 secs]  1 threads:      601422 ops,   24200 (avg:   27334) ops/se[RUN #1 72%,  23 secs]  1 threads:      625610 ops,   24185 (avg:   27197) ops/se[RUN #1 75%,  24 secs]  1 threads:      650197 ops,   24584 (avg:   27088) ops/se[RUN #1 78%,  25 secs]  1 threads:      674432 ops,   24232 (avg:   26974) ops/se[RUN #1 81%,  26 secs]  1 threads:      698319 ops,   23884 (avg:   26855) ops/se[RUN #1 84%,  27 secs]  1 threads:      722245 ops,   23923 (avg:   26747) ops/se[RUN #1 88%,  28 secs]  1 threads:      745916 ops,   23668 (avg:   26637) ops/se[RUN #1 91%,  29 secs]  1 threads:      770644 ops,   24725 (avg:   26571) ops/se[RUN #1 94%,  30 secs]  1 threads:      795157 ops,   24510 (avg:   26502) ops/se[RUN #1 97%,  31 secs]  1 threads:      819571 ops,   24411 (avg:   26435) ops/se[RUN #1 100%,  32 secs]  0 threads:      843913 ops,   24411 (avg:   26371) ops/sec, 1.01MB/sec (avg: 1.09MB/sec),  0.33 (avg:  0.30) msec latency

1         Threads
8         Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         2397.50          ---          ---         0.30724         0.27900         2.02300         3.19900       184.70
Gets        23973.72        28.84     23944.88         0.30226         0.27100         1.95100         3.18300       934.80
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      26371.21        28.84     23944.88         0.30271         0.27100         1.95100         3.18300      1119.50
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.197 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       70500 ops,   70552 (avg:   70552) ops/se[RUN #1 50%,   1 secs]  4 threads:      141346 ops,   70832 (avg:   70692) ops/se[RUN #1 75%,   2 secs]  4 threads:      213602 ops,   72242 (avg:   71209) ops/se[RUN #1 100%,   3 secs]  4 threads:      284871 ops,   71256 (avg:   71221) ops/s[RUN #1 100%,   4 secs]  0 threads:      285077 ops,   71256 (avg:   71113) ops/sec, 2.95MB/sec (avg: 2.95MB/sec),  2.80 (avg:  2.81) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         6487.18          ---          ---         2.82259         2.59100         5.08700        13.43900       499.11
Gets        64619.59        49.89     64569.71         2.80936         2.59100         5.05500        13.69500      2519.32
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      71106.77        49.89     64569.71         2.81057         2.59100         5.05500        13.63100      3018.43
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.197 --test-time 32 -t 1 -c 16
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:       37211 ops,   37224 (avg:   37224) ops/sec[RUN #1 6%,   1 secs]  1 threads:       74803 ops,   37587 (avg:   37406) ops/sec[RUN #1 9%,   2 secs]  1 threads:      112553 ops,   37746 (avg:   37519) ops/sec[RUN #1 12%,   3 secs]  1 threads:      150693 ops,   38136 (avg:   37673) ops/se[RUN #1 16%,   5 secs]  1 threads:      198466 ops,   47768 (avg:   39692) ops/se[RUN #1 19%,   6 secs]  1 threads:      247651 ops,   49178 (avg:   41274) ops/se[RUN #1 22%,   7 secs]  1 threads:      295510 ops,   47854 (avg:   42214) ops/se[RUN #1 25%,   8 secs]  1 threads:      342469 ops,   46955 (avg:   42806) ops/se[RUN #1 28%,   9 secs]  1 threads:      389424 ops,   46950 (avg:   43267) ops/se[RUN #1 31%,  10 secs]  1 threads:      437218 ops,   47789 (avg:   43719) ops/se[RUN #1 34%,  11 secs]  1 threads:      485020 ops,   47796 (avg:   44090) ops/se[RUN #1 38%,  12 secs]  1 threads:      523248 ops,   38223 (avg:   43601) ops/se[RUN #1 41%,  13 secs]  1 threads:      561687 ops,   38434 (avg:   43203) ops/se[RUN #1 44%,  14 secs]  1 threads:      599409 ops,   37718 (avg:   42811) ops/se[RUN #1 47%,  15 secs]  1 threads:      636454 ops,   37041 (avg:   42427) ops/se[RUN #1 50%,  16 secs]  1 threads:      683219 ops,   46760 (avg:   42697) ops/se[RUN #1 53%,  17 secs]  1 threads:      730447 ops,   47222 (avg:   42964) ops/se[RUN #1 56%,  18 secs]  1 threads:      771682 ops,   41230 (avg:   42867) ops/se[RUN #1 59%,  19 secs]  1 threads:      818628 ops,   46941 (avg:   43082) ops/se[RUN #1 63%,  20 secs]  1 threads:      867012 ops,   48379 (avg:   43347) ops/se[RUN #1 66%,  21 secs]  1 threads:      915374 ops,   48357 (avg:   43585) ops/se[RUN #1 69%,  22 secs]  1 threads:      964002 ops,   48622 (avg:   43814) ops/se[RUN #1 72%,  23 secs]  1 threads:     1011890 ops,   47883 (avg:   43991) ops/se[RUN #1 75%,  24 secs]  1 threads:     1053682 ops,   41787 (avg:   43899) ops/se[RUN #1 78%,  25 secs]  1 threads:     1101777 ops,   48090 (avg:   44067) ops/se[RUN #1 81%,  26 secs]  1 threads:     1151119 ops,   49336 (avg:   44270) ops/se[RUN #1 84%,  27 secs]  1 threads:     1199690 ops,   48565 (avg:   44429) ops/se[RUN #1 88%,  28 secs]  1 threads:     1248149 ops,   48454 (avg:   44572) ops/se[RUN #1 91%,  29 secs]  1 threads:     1297132 ops,   48978 (avg:   44724) ops/se[RUN #1 94%,  30 secs]  1 threads:     1345420 ops,   48283 (avg:   44843) ops/se[RUN #1 97%,  31 secs]  1 threads:     1394890 ops,   49465 (avg:   44992) ops/se[RUN #1 100%,  32 secs]  0 threads:     1443456 ops,   49465 (avg:   45106) ops/sec, 2.05MB/sec (avg: 1.87MB/sec),  0.32 (avg:  0.35) msec latency

1         Threads
16        Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         4100.80          ---          ---         0.35798         0.31900         1.13500         3.24700       315.92
Gets        41005.73        51.50     40954.23         0.35415         0.31900         1.08700         3.18300      1599.01
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      45106.54        51.50     40954.23         0.35450         0.31900         1.08700         3.18300      1914.94
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram -s 10.208.129.197 --test-time 4
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 25%,   0 secs]  4 threads:       71416 ops,   71469 (avg:   71469) ops/se[RUN #1 50%,   1 secs]  4 threads:      142358 ops,   70928 (avg:   71199) ops/se[RUN #1 75%,   2 secs]  4 threads:      213507 ops,   71137 (avg:   71178) ops/se[RUN #1 100%,   3 secs]  4 threads:      284145 ops,   70627 (avg:   71040) ops/s[RUN #1 100%,   4 secs]  0 threads:      284352 ops,   70627 (avg:   70944) ops/sec, 2.92MB/sec (avg: 2.94MB/sec),  2.83 (avg:  2.82) msec latency

4         Threads
50        Connections per thread
4         Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         6475.32          ---          ---         2.83822         2.59100         5.56700        13.05500       498.20
Gets        64503.87        49.92     64453.94         2.81524         2.59100         5.21500        13.05500      2514.86
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      70979.19        49.92     64453.94         2.81734         2.59100         5.24700        13.05500      3013.05
INFO:root:run: docker exec -it redis-client-1 memtier_benchmark --hide-histogram  -s 10.208.129.197 --test-time 32 -t 1 -c 32
Writing results to stdout
[RUN #1] Preparing benchmark client...
[RUN #1] Launching threads now...
[RUN #1 3%,   0 secs]  1 threads:       45005 ops,   45035 (avg:   45035) ops/sec[RUN #1 6%,   1 secs]  1 threads:       91803 ops,   46791 (avg:   45914) ops/sec[RUN #1 9%,   2 secs]  1 threads:      137960 ops,   46151 (avg:   45993) ops/sec[RUN #1 12%,   3 secs]  1 threads:      179723 ops,   41758 (avg:   44934) ops/se[RUN #1 16%,   4 secs]  1 threads:      226069 ops,   46340 (avg:   45215) ops/se[RUN #1 19%,   5 secs]  1 threads:      275432 ops,   49356 (avg:   45905) ops/se[RUN #1 22%,   7 secs]  1 threads:      328644 ops,   53206 (avg:   46948) ops/se[RUN #1 25%,   8 secs]  1 threads:      382398 ops,   53747 (avg:   47798) ops/se[RUN #1 28%,   9 secs]  1 threads:      440777 ops,   58371 (avg:   48973) ops/se[RUN #1 31%,  10 secs]  1 threads:      498597 ops,   57812 (avg:   49857) ops/se[RUN #1 34%,  11 secs]  1 threads:      556887 ops,   58283 (avg:   50623) ops/se[RUN #1 38%,  12 secs]  1 threads:      609431 ops,   52536 (avg:   50783) ops/se[RUN #1 41%,  13 secs]  1 threads:      662432 ops,   52994 (avg:   50953) ops/se[RUN #1 44%,  14 secs]  1 threads:      715623 ops,   53184 (avg:   51112) ops/se[RUN #1 47%,  15 secs]  1 threads:      768211 ops,   52582 (avg:   51210) ops/se[RUN #1 50%,  16 secs]  1 threads:      819712 ops,   51495 (avg:   51228) ops/se[RUN #1 53%,  17 secs]  1 threads:      877023 ops,   57303 (avg:   51585) ops/se[RUN #1 56%,  18 secs]  1 threads:      933840 ops,   56810 (avg:   51876) ops/se[RUN #1 59%,  19 secs]  1 threads:      991836 ops,   57989 (avg:   52197) ops/se[RUN #1 63%,  20 secs]  1 threads:     1050277 ops,   58433 (avg:   52509) ops/se[RUN #1 66%,  21 secs]  1 threads:     1107956 ops,   57672 (avg:   52755) ops/se[RUN #1 69%,  22 secs]  1 threads:     1165804 ops,   57840 (avg:   52986) ops/se[RUN #1 72%,  23 secs]  1 threads:     1223665 ops,   57853 (avg:   53198) ops/se[RUN #1 75%,  24 secs]  1 threads:     1280834 ops,   57162 (avg:   53363) ops/se[RUN #1 78%,  25 secs]  1 threads:     1338939 ops,   58098 (avg:   53552) ops/se[RUN #1 81%,  26 secs]  1 threads:     1395892 ops,   56946 (avg:   53683) ops/se[RUN #1 84%,  27 secs]  1 threads:     1453741 ops,   57842 (avg:   53837) ops/se[RUN #1 88%,  28 secs]  1 threads:     1510564 ops,   56816 (avg:   53943) ops/se[RUN #1 91%,  29 secs]  1 threads:     1567909 ops,   57338 (avg:   54060) ops/se[RUN #1 94%,  30 secs]  1 threads:     1625425 ops,   57505 (avg:   54175) ops/se[RUN #1 97%,  31 secs]  1 threads:     1683754 ops,   58321 (avg:   54309) ops/se[RUN #1 100%,  32 secs]  1 threads:     1740348 ops,   56649 (avg:   54382) ops/s[RUN #1 100%,  32 secs]  0 threads:     1740358 ops,   56649 (avg:   54382) ops/sec, 2.35MB/sec (avg: 2.25MB/sec),  0.56 (avg:  0.59) msec latency

1         Threads
32        Connections per thread
32        Seconds


ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets         4944.28          ---          ---         0.59293         0.57500         1.16700         3.59900       380.88
Gets        49438.12        55.56     49382.56         0.58786         0.56700         1.15900         3.61500      1927.59
Waits           0.00          ---          ---             ---             ---             ---             ---          ---
Totals      54382.40        55.56     49382.56         0.58832         0.56700         1.15900         3.61500      2308.47
```