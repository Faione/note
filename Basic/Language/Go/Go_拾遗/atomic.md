# Atomic

`atomic` 提供了一系列原子操作函数，这些函数保证执行的原子性(利用cpu提供的相关指令)
- `Add*(addr, delta) new` : 将 delta 与 addr 对应内存中的值相加，返回相加后的结果
- `Swap*(addr, new) old` : 将 addr 对应内存中的值修改为 new，返回修改前的值
- `CompareAndSwap*(addr, old, new) swapped` : 比较 addr 对应内存中的值是否与 old 相等，如果相等则将 addr 对应内存中的值修改为 new, 返回 true, 否则返回false
- `Load*(addr)val`: 读取 addr 对应内存中的值
- `Store*（addr, val）`: 将 val 存储到 addr 对应的内存中

`atomic` 中主要对 `Int32`, `Int64`, `Uint32`, `Uint64`, `Uintptr`, `Pointer` 进行了如上原子操作的实现, 用户可以构造自旋锁来对其他类型的变量进行原子操作


```go
// 使用 math 库中的 `Float64frombits` 与 `Float64bits` 可以实现 uint64 与 float64 之间的相互转化
func (g *gauge) AddFloat64(addr *float64, delta float64) (new float64){
	for {
        // 原子读
		oldBits := atomic.LoadUint64(addr)
		newBits := math.Float64bits(math.Float64frombits(oldBits) + delta)
        // 如果当前值与旧值相同，则进行交换，反之则继续自旋
		if atomic.CompareAndSwapUint64(addr, oldBits, newBits) {
			return
		}
	}
}
```