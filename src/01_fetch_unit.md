{
	"title": "Fetch unit"
}

# Fetch unit

In the previous lessons we have created a template that I will use as a starting point. First, let's clean it up a bit by removing the example logic from it. I am not worried about removing too much, one benefit of using a version control system like `git` is that we can recover old code without too much effort.

!! be97cf34320e0962e24d922fa293bd166282b53f

With that out of the way, we are ready to start working. But where to start? We came up with this diagram in the last lesson.

![Overview of the system-on-chip architecture](01_fetch_unit/overview.svg)

For now we will focus on the most important component: the CPU itself. We are building a pipeline that starts with the "fetch" stage, so it is most natural to start there. We'll make a new module for the fetch unit now, and only integrate it in other modules when we're ready.

First, let's just create a placeholder module.

!! 72d1913b533ff75937f4fb504e0f796734646c3f

Now, the fetch unit is responsible for retrieving the instructions from memory. Since we don't have memory yet, we'll just create an array for instructions. For now we'll only use it to run tiny test programs, so I'll only make it big enough for 16 instructions. If should be straightforward to increase the size later if we want this for some reason.

!! 754e624f8ed4d71035b0162760e2eb39a0a28be9

For now I put all instructions as all-zeros, but maybe it might come in handy to number the first, say, five instructions so that we can easily identify them. I'll start counting with 1 to avoid misinterpreting any all-zeros vector as the first vector.

!! 30e567fa1625da89fd8318c9c851c99740d28fcc

Now, in RISC-V (and most other architectures), we have the concept of a *program counter*, which is nothing more than a register that contains the address of the current instruction.

For now we'll just initialize it to zero and increment it by four every clock cycle. Why increment by four instead of one? Well, the program counter is an address in bytes, and for the version of RISC-V we are implementing, every instruction is 32 bits, or four bytes.

!! 83784cf5e6e02f75fcc8c7199b3a1cf9fd315be6

Now, we want to actually output the instruction that the program counter points to. For now, I'll implement this with combinatorial logic, since it is convenient and makes sure the program counter and the opcode that is output are in sync.

!! f44a09f8f008f538374c8e51ed3de6df69985066

This implementation takes some shortcuts for the sake of keeping the momentum:
- The program counter is a 32-bit register, but we only use the lower 4 bits. This means it will wrap around after executing 16 instructions, which is incorrect.
- Implementing this with combinatorial logic is not ideal since it can lead to timing errors.

I am not concerned by either of these errors, since this is just an initial implementation that allows us to continue with the other pipeline stages. We'll rewrite this implementation in a correct and robust way later.
