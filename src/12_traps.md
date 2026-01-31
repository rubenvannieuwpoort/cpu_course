{
	"title": "Traps"
}

# 12. Traps

In RISC-V terminology, a *trap* is the mechanism that handles interrupts and exceptions. The difference between an exception and an interrupt is that an exception is synchronous: For example, it can be by an invalid instruction executed by the core. On the other hand, an interrupt is caused by an external event. For example, an interrupt can be activated by a timer.

Upon a trap, the following things happen:
- The reason for the trap is stored in the `mcause` CSR
- The address of the instruction that was interrupted by the trap is stored in the `mepc` CSR
- If there is extra information for the specific trap, it is stored in `mtval`, else it is set to `0`
- The `MPIE` field of `mstatus` is set to `MIE`
- The `MIE` field of `mstatus` is set to `0`
- The `pc` is set to `mtvec` (in direct mode or for exceptions) or to `mtvec + 4 * cause` if the mode is vectored and the cause is an interrupt

The privileged part of the RISC-V docs also define some instructions. One of them is `MRET`, which return from a trap handler and does the following:
- It resets `mstatus.MIE` to `mstatus.MPIE`
- It sets `mstatus.MPIE` to `1`
- It sets `pc` to `mepc`

The other instruction that is defined in the privileged part of the ISA is the `WFI` (wait for interrupt). It should halt the processor until an interrupt occurs. However, this instruction is only meant to save power; a legal implemention is a `NOP`.

Let's do the easy work first and implement `WFI` as a `NOP` for now.

!!Implement WFI as NOP

Now let's implement `MRET`, which is also quite easy.

!!Implement MRET

Now we'll consider exceptions. The following exceptions are defined:
0. Instruction address misaligned: generated on a *taken* branch or unconditional jump when the target address is not aligned
1. Instruction access fault: generated when the instruction fetch tries to fetch from a memory region that is not accessible
2. Illegal instruction: when decoding an instruction fails
3. Breakpoint: TODO
4. Load address misaligned
5. Load access fault
6. Store address misaligned
7. Store access fault
...
11. Environment call from M-mode

There are a lot more exceptions defined, but they are not applicable. Regarding interrupts, there are 3 that are potentionally interesting:
- Machine system interrupt
- Machine timer interrupt
- Machine external interrupt

The machine system interrupt is caused by other cores. Since our implementation only has one core, it is not applicable. The machine external interrupt is caused by peripherals, but at this point we don't have them, so we can ignore this interrupt as well. So only the machine timer interrupt is left, and I will postpone the implementation of this to a later lesson.

First, I'll set up the basic structure of how traps work.

!!Improve tooling

...

!!wip

...

!!Implement mtime and mtimeh

...

!!Use constant for memory size

...

!!Implement mtimecmp and mtimecmph

...

!!Fix program script

...

!!Implement timer interrupts

...

!!Make execute stage more consistent
