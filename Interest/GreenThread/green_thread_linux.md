```rust
#![feature(naked_functions)]

use std::{arch::asm, process::exit};

/// 2MB Default Stack Size
const DEFAULT_STACK_SIZE: usize = 1024 * 1024 * 2;
const MAX_THREADS: usize = 4;
static mut RUNTIME: usize = 0;

pub struct Runtime {
    threads: Vec<Thread>,
    current: usize,
}

#[derive(Debug, PartialEq, Eq)]
enum State {
    // 可用
    // 可以分配任务并运行
    Available,
    // 运行
    Running,
    // 就绪
    // 可以恢复暂停的任务
    Ready,
}

/// 保存线程数据
struct Thread {
    // 线程 id
    id: usize,
    // 线程栈
    stack: Vec<u8>,
    // 保存恢复运行所需要的与CPU相关的数据
    ctx: ThreadContext,
    // 线程状态
    state: State,
}

#[derive(Debug, Default)]
#[repr(C)]
struct ThreadContext {
    rsp: u64,
    r15: u64,
    r14: u64,
    r13: u64,
    r12: u64,
    rbx: u64,
    rbp: u64,
}

impl Thread {
    fn new(id: usize) -> Self {
        Thread {
            id,
            stack: vec![0_u8; DEFAULT_STACK_SIZE],
            ctx: ThreadContext::default(),
            state: State::Available,
        }
    }
}

impl Runtime {
    pub fn new() -> Self {
        // 基础线程
        let base_thread = Thread {
            id: 0,
            stack: vec![0_u8; DEFAULT_STACK_SIZE],
            ctx: ThreadContext::default(),
            state: State::Running,
        };

        // 初始化其他线程
        let mut threads = vec![base_thread];
        let mut available_threads: Vec<Thread> = (1..MAX_THREADS).map(|i| Thread::new(i)).collect();
        threads.append(&mut available_threads);

        Runtime {
            threads,
            current: 0,
        }
    }

    pub fn init(&self) {
        unsafe {
            let r_ptr: *const Runtime = self;
            RUNTIME = r_ptr as usize;
        }
    }

    pub fn run(&mut self) -> ! {
        while self.t_yield() {}
        std::process::exit(0);
    }

    fn t_return(&mut self) {
        if self.current != 0 {
            self.threads[self.current].state = State::Available;
            self.t_yield();
        }
    }

    #[inline(never)]
    fn t_yield(&mut self) -> bool {
        let mut pos = self.current;
        // 找到状态为 Ready 的线程
        while self.threads[pos].state != State::Ready {
            pos += 1;
            if pos == self.threads.len() {
                pos = 0;
            }
            if pos == self.current {
                return false;
            }
        }

        // 如果当前线程尚未退出，则修改状态为Ready
        if self.threads[self.current].state != State::Available {
            self.threads[self.current].state = State::Ready;
        }

        self.threads[pos].state = State::Running;

        let old_pos = self.current;
        self.current = pos;

        // 切换上下文
        unsafe {
            let old: *mut ThreadContext = &mut self.threads[old_pos].ctx;
            let new: *const ThreadContext = &self.threads[pos].ctx;

            asm!(
                "call switch",
                in("rdi") old,
                in("rsi") new,
                clobber_abi("C")
            );
        }

        self.threads.len() > 0
    }

    pub fn spawn(&mut self, f: fn()) {
        // 找到空闲的线程
        let available = self
            .threads
            .iter_mut()
            .find(|t| t.state == State::Available)
            .expect("no available thread.");

        let size = available.stack.len();
        unsafe {
            let s_ptr = available.stack.as_mut_ptr().offset(size as isize);
            let s_ptr = (s_ptr as usize & !15) as *mut u8;
            // 将 guard skip f 放入栈中
            std::ptr::write(s_ptr.offset(-16) as *mut u64, guard as u64);
            std::ptr::write(s_ptr.offset(-24) as *mut u64, skip as u64);
            std::ptr::write(s_ptr.offset(-32) as *mut u64, f as u64);
            available.ctx.rsp = s_ptr.offset(-32) as u64;
        }
        available.state = State::Ready;
    }
}

/// 退出当前任务
/// 设置线程状态为Available，并还执行权限
fn guard() {
    unsafe {
        let rt_ptr = RUNTIME as *mut Runtime;
        (*rt_ptr).t_return();
    }
}

/// 弹出栈上的数据，并进行跳转
/// 当前此方法上是 guard
#[naked]
unsafe extern "C" fn skip() {
    asm!("ret", options(noreturn))
}

pub fn yield_thread() {
    unsafe {
        let rt_ptr = RUNTIME as *mut Runtime;
        (*rt_ptr).t_yield();
    }
}

pub fn current_thread() -> usize {
    unsafe {
        let rt_ptr = RUNTIME as *mut Runtime;
        (*rt_ptr).current
    }
}

/// 替换 old 为 new  TaskContext
/// 替换了栈 与 调用者保存寄存器
/// ret 之后，由于栈已经替换，因此可以从栈上恢复调用者保存寄存器
#[naked]
#[no_mangle]
unsafe extern "C" fn switch() {
    asm!(
        "mov [rdi + 0x00], rsp",
        "mov [rdi + 0x08], r15",
        "mov [rdi + 0x10], r14",
        "mov [rdi + 0x18], r13",
        "mov [rdi + 0x20], r12",
        "mov [rdi + 0x28], rbx",
        "mov [rdi + 0x30], rbp",
        "mov rsp, [rsi + 0x00]",
        "mov r15, [rsi + 0x08]",
        "mov r14, [rsi + 0x10]",
        "mov r13, [rsi + 0x18]",
        "mov r12, [rsi + 0x20]",
        "mov rbx, [rsi + 0x28]",
        "mov rbp, [rsi + 0x30]",
        "ret",
        options(noreturn)
    )
}

fn main() {
    let mut runtime = Runtime::new();
    runtime.init();

    for _ in 0..2 {
        runtime.spawn(|| {
            let thread_id = current_thread();
            println!("Thread {} Starting", thread_id);

            for i in 0..10 {
                println!("thread: {} counter: {}", thread_id, i);
                yield_thread();
            }
            println!("Thread {} Finished", thread_id);
        });
    }

    runtime.run();
}

```