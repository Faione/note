# 超标量-IPL极限

- issue数量与commit数量相同


- 直接相联 写入时无法并行，写入性能弱于读
  - 写分为两个步骤，匹配Tag -> 写入Word
- 猜测执行的结果一定要buffer，并判断buffer换入换出的时机