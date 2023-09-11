# Global Allocator

栈上内存的分配由编译器以及相关的规则决定，而堆上的内存分配依赖特定的分配器来实现，rust标准库中定义了`GlobalAlloc`,任何对于此trait的实现都可以作为堆内存分配器， 而默认情况下rust使用 `jemalloc`

用户可以通过实现 `GlobalAlloc`, 以及 `#[global_allocator]` 属性宏来堆全局堆分配器进行自定义


## STD Allocator

rust中默认使用的分配器为 `std::alloc::System`, 其中对于 `GlobalAlloc` trait 的实现在标准库 `src/sys` 下的不同操作系统文件夹中，以linux为例，其实现在 `src/sys/unix/alloc.rs` 中，依赖libc malloc

## Simple Allocator

> 注意不要在 alloc 过程中使用 print，因为 print 的过程中会申请buffer用于数据传递，会导致 alloc 的递归调用以至于进入死循环 [^1]

[^1]: [avoid_print_in_alloc](https://stackoverflow.com/questions/57314776/does-the-println-macro-allocate-heap-memory)


最简单 Allocator 只需要实现 `alloc` 与 `dealloc`，即可，layout 中提供了所需内存的 size 和 align, 前者是要分配的大小，后者则要求返回的地址需要按照 align 进行对齐(可能导致最终分配的大小比 size 更大)

```rust
unsafe fn alloc(&self, layout: Layout) -> *mut u8 {}

unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {}
```

可以使用一个简单的数组作为堆，随后进行分配即可，保存在`.data`段的 SimpleAllocator 将作为默认的堆内存分配器来为Vec，String等存在堆上内存需要的对象进行服务

```rust
#[global_allocator]
static ALLOCATOR: SimpleAllocator<ARENA_SIZE> = SimpleAllocator {
    arena: UnsafeCell::new([0; ARENA_SIZE]),
    remaining: AtomicUsize::new(ARENA_SIZE),
};
```