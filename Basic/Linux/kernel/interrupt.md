## Interrupt

static const __initconst struct idt_data apic_idts[] = {...}

struct x86_init_ops x86_init __initdata = {
    ...
    .irqs = {
        ...
        .intr_init = native_init_IRQ,
        ...
    },
    ...
}


x86_init.irqs.intr_init = native_init_IRQ

> APIC: Advanced Programmable Interrupt Controller, for each Hyperthread

start_kernel -> init_IRQ() -> native_init_IRQ() -> idt_setup_apic_and_irq_gates -> idt_setup_from_table


INTG(RESCHEDULE_VECTOR,			asm_sysvec_reschedule_ipi), 中所引用的符号 `asm_sysvec_reschedule_ipi` 是通过宏实现的，包括C与汇编的宏，其中汇编宏定义在 entry_64.S / entry_32.S 中， 包括 `idtentry_irq` 和 `idtentry_sysvec` 等，而 C 宏包含在 `arch/x86/include/asm/idtentry.h` 中，包括 `DEFINE_IDTENTRY_IRQ` 和`DECLARE_IDTENTRY_SYSVEC` 等，C声明了入口点，真正代码由汇编生成

`arch/x86/` 中许多位置都用到此宏， 


[linux_irq](https://zhuanlan.zhihu.com/p/649008200)