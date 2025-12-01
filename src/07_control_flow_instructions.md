{
	"title": "Control flow instructions"
}

This lesson starts at commit [6304d615b3559db9ac9908467a134b971d5b82c0](https://github.com/rubenvannieuwpoort/course_cpu/commit/6304d615b3559db9ac9908467a134b971d5b82c0).

# 7. Control flow instructions

Let's continue with the control flow instructions. These are instructions that perform a "jump" or "call" and need to change the `pc` register in the fetch module. To do this, we need to add some signals in the output of the execute module and let the fetch module use them as inputs. We'll add an indicator signal `jump` that indicates if the pc should be overwritten, and a `jump_address` vector to pass the new address of the `pc` register.

!!Add jump and jump_address signals

Now, we want to use them in the fetch module.

!!Use jump and jump_address signals in fetch module

We don't support fetching and jumping at the same time; I'll add an assertion to check this.

!!Add assertion to fail when jumping while fetching

Now, we want to implement the `JAL` and `JALR` instructions. The docs say this about them:

> The jump and link (JAL) instruction uses the J-type format, where the J-immediate encodes a signed offset in multiples of 2 bytes. The offset is sign-extended and added to the address of the jump instruction to form the jump target address. Jumps can therefore target a ±1 MiB range. JAL stores the address of the instruction following the jump ('pc'+4) into register rd.

> The indirect jump instruction JALR (jump and link register) uses the I-type encoding. The target address is obtained by adding the sign-extended 12-bit I-immediate to the register *rs1*, then setting the least-significant bit of the result to zero. The address of the instruction following the jump (pc+4) is written to register rd.

Note that for the JALR instruction we'll actually need three operands:
1. The immediate
2. The value of the rs1 register
3. The value that will be stored in the destination register

So, we'll add an operand to the output of the decode stage, which we'll use to pass the value that should be stored in the destination register.

!!Add third operand to decode output

Now we're ready to decode the `JAL` and `JALR` instructions.

!!Decode JAL and JALR instructions

We just need to implement `OP_JAL`, which should set `result` to `pc + 4`, add operand 1 and 2, set the LSB of the result to zero, and jump to that.

!!Implement OP_JAL

Now, let's decode `BEQ`, `BNE`, `BLT`, `BGE`, `BLTU`, `BGEU`.

!!Decode BEQ, BNE, BLT, BGE, BLTU, BGEU

And implement `OP_BEQ`, `OP_BNE`, `OP_BLT`, `OP_BGE`, `OP_BLTU`, `OP_BGEU`.

!!Implement OP_BEQ, OP_BNE, OP_BLT, OP_BGE, OP_BLTU, OP_BGEU

Now that we have a jump instruction, we don't need our custom `HANG` instruction anymore. Instead, we can just do
```
hang:
j hang
```

This is a "pseudoinstruction" that you can think of as syntactic sugar for a `JAL` instruction with immediate `0`. So, the instruction jumps to itself, effectively hanging the CPU.

!!Remove custom HANG instruction

That's all the work on the CPU for this lesson.

As a sanity check, I wrote this cute little program in RISC-V assembly to calculate Fibonacci numbers again.

```
# x3 stores the number of
# iterations we still have to do
li x3, 10

# init x1, x2 to F0, F-1
li x2, 1

loop:

# do two iterations
add x2, x1, x2
add x1, x1, x2

# decrease x3
addi x3, x3, -2

# loop if we're not done yet
bgt x3, x0, loop

# if the number of iterations is zero
beq x3, x0, end

# otherwise, x3 equals -1 and x1 has
# the next Fibonacci number, so we get
# the previous one which is stored in x2
mv x1, x2

end:
j end
```

We can assemble this with the [online RISC-V assembler](https://riscvasm.lucasteske.dev/) and put it into our instruction memory.

!!Add Fibonacci program in instruction memory

Now, we can test it and see that `x1` holds `0x37`, which is 55 in decimal, and indeed the tenth Fibonacci number equals 55.