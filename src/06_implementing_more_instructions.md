{
	"title": "Implementing more instructions"
}

This lesson starts at commit [52ad976f12300a37998296b9861bfa7bccabac4a](https://github.com/rubenvannieuwpoort/course_cpu/commit/52ad976f12300a37998296b9861bfa7bccabac4a).

# 6. Implementing more instructions

After the hopefully fun diversion in the last lesson, we are back to work. There are 40-ish instructions in the RISC-V base instruction set, and we have only implemented two so far. Let's bang out some more instructions!

Let's grab the RV32/64G Instruction Set Listings of the RISC-V docs.

First, let's just add variables for all the bit fields we don't have yet.

!! 5231a0df2b71c5f0d5b0b9d4e8ef7f0864a47899

Now, let's remove the decoding logic we currently have and just start implementing the instructions from the RV32/64G Instruction Set Listings.

!! 1e65a73437d77ff3fa6e657e353515a608a1e6f8

So we start with `LUI` and `AUIPC`. In Chapter 2 (RV32I Base Integer Instruction Set) of the RISC-V unprivileged architecture document, we find this:

![Descriptions and bits for LUI and AUIPC instructions](06_implementing_more_instructions/LUI_AUIPC.png)

In chapter 35, we see that the `opcode` field is `0110111` for `LUI` and `0010111` for `AUIPC`.

!! 8d94acb5977a7fb08d1852c598bdb1ac8c21e5ef

So, we start with `LUI`. We need to place the immediate value in the `rd` register. This is easy enough with the existing infrastructure.

!! 0a1beb133bc9c4040c45b4655504adade5ee8c4e

`AUIPC` is similar, but the it adds the immediate to the address of the instruction. This address is in the `pc` register in the `fetch` stage, but not yet available in the `decode` stage, so we need to pass it in the output of the `fetch` stage.

!! ca9cbf89e23782732f908ec4e52bc4262e0fa3ab

Now, we can implement `AUIPC` similar to `LUI` in the decode stage.

!! 2722f188a2657cd3d530b0e4cb1a846aba6d32c4

Now, `JAL` and `JALR` are control flow instructions, which mean we'll have to somehow change the value of the `pc` register in the fetch stage. This requires changes in at least 3 modules as well as some testing. This is a bit too much work for this lesson; we'll just work on the "low-hanging fruit" now, and will return to the instructions that require more work later.

!! e5078e1a60b6560b4c1cbf238a52aba8f1d2f6d1

Now, `BEQ`, `BNE`, `BLT`, `BGE`, `BLTU`, and `BGEU` are control flow instructions as well, so we skip them too. 

!! 0069be8452e86194a2a47391afb190dd15c85493

We'll also skip `LB`, `LH`, `LW`, `LBU`, `LHU`, `SB`, `SH`, `SW` because these are memory operations and we haven't implemented memory yet. So far, this is going *excellent*.

!! 1463068ccc2768d147c634ee0d1b646627762116

Now, we arrive at a bunch of instructions that have the same opcode (but a different value for the `funct3` field): `ADDI`, `SLTI`, `SLTIU`, `XORI`, `ORI`, `ANDI`.

First, we want to recognize these instructions.

!! 27247da4d5321cef6234ba9f23f8507c430aa506

We have implemented `ADDI` before, so we can just add that code back.

!! 70809faa232cf60e5da171b61ccd7c9acb10a8f9

The other instructions are very similar, but the exact operation that is executed in the execute stage is slightly different. So we can structure the code a bit differently to take advantage of the similarity.

!! fb7b05e5bdc63088d49a2870856ef63fa33d17df

Now we add a couple of operations so that we can decode `SLTI`, `SLTIU`, `XORI`, `ORI`, `ANDI`.

!! 6cabd53362edeca2f060fc00aff8f5db33f2b364

Now we still have to implement these operations in the execute module.

`OP_SLT` compares two operands as signed numbers, and sets 1 when the first operand is less than the second.

!! 6fb6c533c984be03e4884fa6ff76d0e058fa8919

`OP_SLTU` is similar but works on unsigned operands.

!! c36a61dd43b2265d915b6bd3cad47239fffa31c7

`OP_XOR`, `OP_OR`, and `OP_AND` are similar and simple to implement.

!! a00df3fb7447849314075dd71d8d475efda96ba9

Now, `SLLI`, `SRLI`, and `SRAI` are similar to eachother but different from the instructions we just implemented, but for some reason all share the same opcode. I'll put these three instructions above the ones we just implemented, so that we can use slightly less logic.

!! 309e0232dc6ff577edad9b19772440f621c7d39d

Again, we add operations to implement the decoding of these instructions.

!! 5f1c5c1cf8ea91538fe3d1e712551960579f10ce

Then we implement the operations themselves. The shift instructions are a bit weird. The manual mentions
> The operand to be shifted is in *rs1*, and the shift amount is encoded in the lower 5 bits of the I-immediate field.

This means that you can shift by at most 31 bits. Janky as hell in my opinion, but we're just implementing the spec, not making it.

A nice way of implementing shifts by a variable number of bits, say `n`, is two do the shift as a sequence of shifts of powers of two. If `n` is 5-bits, and the most significant bit of `n` is set, we shift by 16 bits. If the next bit is set, we shift by 8 bits, etc., etc. At the end, we'll have shifted by `n` bits.

!! cb4d714ddd0e7c0a8f9468e0110dd5c55ac77c6e

This is a big change, but it's (almost) the same verbose code. In fact, we can merge the implementations of the two right shifts (`SRL` and `SRA`).

!! 76d19f23a41e97f3f976036061b8a909e27d6a43

Moving on; almost all of the instructions with opcode `0110011` are register-register versions of instructions we already implemented. The `SUB` instruction is the only exception.

As usual I'll add placeholders first.

!! 6e9e2d12189ac0cdd1798e313796a984726d4597

Now we'll add the implementation.

!! de994d38dd8ac978a2402ae53e25b1667a5cd952

Now, we just have to implement `OP_SUB` in the decoder.

!! 48e308001a90db65362cff78734dd6fce31de853

OK, phew. Just a couple of oddball instructions left. `FENCE` is used for memory ordering. We don't even have memory yet, so for now we'll make this a NOP.

!! a6846637e4a8e667aca01dec7c1f8d776e311109

Now, `FENCE.TSO` and `PAUSE` are special cases of `FENCE`, which we already handle. So we can skip them; We'll look if we can do something better later.

`ECALL` and `EBREAK` are traps, which we have not implemented yet. So I'll add the logic to be able to easily decode them later, but otherwise ignore them.

!! 2a0b69e454f9394b2892d0b96a8e54f794853b41

Now that we're done, let's add back our custom "LED" and "HANG" instructions.

!! 6304d615b3559db9ac9908467a134b971d5b82c0

Phew, we added a lot of instructions! We added the decoding for all instructions and actually implemented about half of all the instructions in the basic RV32 ISA. Not bad for a single lesson.

Did we forget anything? Testing, you say?
