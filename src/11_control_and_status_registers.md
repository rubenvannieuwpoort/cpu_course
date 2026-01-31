{
	"title": "Control and status registers"
}

# 11. Control and status registers

Control and status registers are registers that are not part of the general-purpose registers `x0`-`x31`, but instead have "special" functions. That is, they control something or return the status of something. To read or write them, there are special instructions defined by the "Zicsr" extension.

The RISC-V specification is a bit awkward in the sense that it's a bit arbitrarily split into "unprivileged" and "privileged" volumes. Since we're implementing a very simple processor, we only have a single privilege level. But this doesn't mean that we don't have to consider the privileged architecture!

It's probably best explained in the RISC-V unprivileged architecture:
> Unprivileged instructions are those that are generally usable in all privilege modes in all privileged architectures, though behavior might vary depending on privilege mode and privilege architecture.

Another confusing aspect is that for any hardware implementation, the "Zicsr" extension for control and status registers is *mandatory*. So, the Zicsr extension, which describes the instructions to access CSRs, is described in the unprivileged part of the manuals, while the CSRs themselves are described in the privileged part of the manuals.

The "Zicsr" extension defines 6 instructions:
- `CSRRW rd, csr, rs` (read/write CSR) puts the value of the CSR `csr` into the general-purpose register `rd`, and the value of the general-purpose register `rs` into `csr`. `CSRRWI` is similar but uses an immediate instead of `rs`.
- `CSRRS rd, csr, rs` (read and set bits in CSR) puts the value of the CSR `csr` into the general-purpose register `rd`, and sets the high bits of the general-purpose register `rs` in `csr`. `CSRRS` is similar but uses an immediate instead of `rs`.
- `CSRRC rd, csr, rs` (read and clear bits in CSR) puts the value of the CSR `csr` into the general-purpose register `rd`, and clears the high bits of the general-purpose register `rs` in `csr`. `CSRRS` is similar but uses an immediate instead of `rs`.

The RISC-V assembly programmer's manual defines various pseudoinstructions:
- `CSRR rs, csr` is an alias for `CSRRS rd, csr, x0` and can be used to read a CSR.
- `CSRW csr, rs` is an alias for `CSRRW x0, csr, rs` and can be used to write a CSR. Similarly, `CSRWI csr, imm` is an alias for `CSRRWI x0, csr, imm`.
- `CSRS csr, rs` is an alias for `CSRRS x0, csr, rs` and can be used to set bits in a CSR. Similarly, `CSRSI csr, imm` is an alias for `CSRRSI x0, csr, imm`.
- `CSRC csr, rs` is an alias for `CSRRC x0, csr, rs` and can be used to clear bits in a CSR. Similarly, `CSRCI csr, imm` is an alias for `CSRRCI x0, csr, imm`.

There are two kinds of CSRs: **read-only** CSRs, and **read-write** CSRs. Obviously, read-only CSRs can only be read. Read-only CSRs have an address with their most significant bits (bits 10 and 11) set to 1.

Trying to write to them will result in an "illegal instruction" exception.

The manual defines three types of fields within read-write CSRs:
- Writes preserve, reads ignore values (WPRI): these fields are reserved for future use and software should ignore the values from these fields. Writes should preserve the value of these fields. For forward compatibility, implementations that do not furnish these fields must make them read-only zero.
- Write legal, read legal values (WLRL): fields of this type should only be written with legal values (what is a legal value should be specified per CSR). Implementations are permitted but not required to raise an illegal-instruction exception if an instruction attempts to write a non-supported value to a WLRL field. Implementations can return arbitrary bit patterns on the read of a WLRL field when the last write was of an illegal value, but the value returned should deterministically depend on the illegal written value and the value of the field prior to the write.
- Write any, read legal values (WARL): Fields of this type allow any value to be written to them, but will always return a legal value when read.

Fields in read-write CSRs can also be read-only, which simply means writes to these fields are ignored (no exception happens). For some reason this doesn't get a fancy acronym (maybe read-only CSRs are considered a special case of WARL CSRs?).

For fields of the last type (WARL), the manual notes the following:
> Assuming that writing the CSR has no other side effects, the range of supported values can be determined by attempting to write a desired setting then reading to see if the value was retained.

We need to read the manuals carefully to see which CSRs we need to implement for our minimal implementation. The easiest way to do this is to read chapter 3 of the privileged part of the RISC-V manual. I've gone ahead and did the research for you:
- `mvendorid`
- `marchid`
- `mimpid`
- `mhartid`
- `mconfigptr`
- `mstatus`
- `misa`
- `mtvec`
- `mstatush`
- `mscratch`
- `mepc`
- `mcause`
- `mtval`
- `mip`
- `mcycle`
- `minstret`
- `mhpmcounter3`..`mhpmcounter31`
- `mcycleh`
- `minstreth`
- `mhpmcounter3h`..`mhpmcounter31h`
- `mhpmevent3`..`mhpmevent31`
- `mhpmevent3h`..`mhpmevent31h`

(I give this list as a reference, to find relevant information it's still necessary to search what the manual says about the CSRs.)

So, let's get going. First we add some placeholders in the decoder.

!!Add placeholders for CSR instructions in decoder

In the decoder we'll set the operation to one of `OP_CSRRW`, `OP_CSRRS`, `OP_CSRRC`. We'll put the value of `rs1` (or the immediate value, for the `I`-variants of the instructions) in the first operand and the address of the CSR register into the second operand.

!!Decode CSR instructions

We'll also add constants for the mandatory CSRs.

!!Add constants for mandatory CSRs

To reduce the amount of duplicated code (and opportunity for bugs) a bit, I chose an implementation where the final value of a CSR is determined as
```
csr_new_value := (csr_value or set_bits) and clear_bits;
-- somehow make csr_new_value a legal value
csr_value <= csr_new_value
```

So the `1` bits in `set_bits` are set, and the `0` bits in `clear_bits` are cleared.

`CSRRW` can now be implemented by setting
```
set_bits := value;
clear_bits := value;
```

`CSRRS` as
```
set_bits := value;
clear_bits := (others => '0');
```

and `CSRRC` as
```
set_bits := (others => '0');
clear_bits := not value;
```

!!Implement some infrastructure for CSR operations

Now, we are *almost* ready to start implementing CSRs. But first, a question: What does the RISC-V specification consider a write? The answer is:
- Any `CSRRW` operations
- `CSRRS` and `CSRRC` operations with `rs` set to `x0`
- `CSRRSI` and `CSRRCI` operations with the immediate value set to 0

This means that `CSRRS` and `CSRRC` operations with a non-`x0` register holding 0 are still considered writes, even though they don't change the value of the CSR. Annoyingly, this means we need to determine in the decode stage if the operation is a "read-only" operation. In the execute stage, we only have the value, and we need to know *where the value came from* in order to know if a write is performed (in case we might need to raise an exception).

!!Set csr_read_only signal in decode stage and pass it to execute stage

The `mvendorid`, `marchid`, `mimpid`, `mhartid`, and `mconfigptr` CSRs can legally be set to zero. However, I do want to have the ability to easily fill them later, so I will define some constants for them and simply return those.

!!Implement mvendorid, marchid, mimpid, mhartid, and mconfigptr

Now, on to `mstatus`. This is a complicated CSR, but for a minimal implementation we only need the `mie` and `mpie` bits as read-write; most other bits/fields can be read-only zero. The only exception is `mpp`, which holds the previous privilige mode. Since our implementation only has the "machine" privilege mode, which corresponds to `11`, so we hardcode `mpp` to `11`.

!!Implement mstatus

On to `misa`. This CSR indicates what the bit width of the ISA is (32 or 64), and which extensions are active. It is a WARL CSR, meaning writes are allowed, but only legal values are returned on reading. The idea behind is that you can enable extensions by writing a one to the bit in `misa` that corresponds to that extension. If the bit stays zero, this means the implementation does not support the extension.

We are not implementing any extensions. For the `RV32I` subset, we return `x40000100` (the encoding is explained in the manual in the section for the `misa` CSR). I load this value from a constant so that we can easily change it if we do implement more extensions later.

!!Implement misa

The `mie` CSR contains "interrupt enable" bits for all the interrupts. There are 16 interrupts mandated by RISC-V, spanning the lower 16 bits of `mie`. The rest of them are custom and for now I make them read-only zeros.

(Note that we don't implement the functionality of any CSRs yet, just the reading and writing of them.)

!!Implement mie

The `mtvec` CSR has to do with the address of the interrupts handler. The lower two bits define a "mode"; only `00` and `01` are allowed.

!!Implement mtvec

For our implementation, the `mstatush` register can be read-only zero.

!!Implement mstatush

The `mscratch` CSR is a read-write scratch CSR that can be used for anything.

!!Implement mscratch

The `mepc` CSR holds the address of an instruction that was being executed when a trap (exception or interrupt) occurred. Again, we don't implement that functionality now, only the reading and writing.

!!Implement mepc

The `mcause` CSR is written when a trap happens and holds a code indicating the cause of the trap. The MSB holds a bit that indicates if the trap was an interrupt. Codes up to 64 are defined, so I just use 6 bits for the code.

!!Implement mcause

The `mtval` CSR is written when a trap happens and contains extra information about the trap, when applicable. What exactly is in `mtval` is dependent on the trap. For example, for illegal memory accesses, `mtval` holds the address of the memory for which an access was attempted.

!!Implement mtval

The `mip` CSR is a lot like `mie`, but holds pending bits to indicate that interrupts are pending.

!!Implement mip

The `mcycle` CSR holds the number of cycles that the processor went through. The RISC-V specification implies you can also write to it (although it does a really poor job of actually specifying what should happen).

!!Implement mcycle

The `minstret` CSR is very similar but counts retired instructions.

!!Implement minstret

There are 29 counters, `mhpmcounter3` up to `mhpmcounter31`, which are mandatory to implement, but it's legal to implement them as read-only zero.

!!Implement mhpmcounter

The `mcycleh` and `minstreth` CSRs are like the `mcycle` and `minstret` CSRs but hold the upper 32 bits.

!!Implement mcycleh and minstreth

The `mphmcounter`s also have variants that hold the higher bits.

!!Implement mhpmcounterh

Finally, we have `mhpmevent` and `mhpmeventh` counters, which can be read-only zero.

!!Implement mhpmevent and mhpmeventh

Now, we have defined most CSRs that need to exist. Most of them are either read-only registers, or have to do with interrupts, and we'll look at them later. Exceptions are `mcycle` (and `mcycleh`) and `minstret` (and `minstreth`). These are incrementing counters, but we need to overwrite them when writing to them. This is most easily implemented by using variables.

!!Actually count cycles in mcycle

For `minstret` and `minstreth` the approach is similar, but we need to know when an instruction retires. I implement this by connecting the `pipeline_ready` signal from the writeback stage to the execute stage, and only incrementing the retired instruction count when this signal is high.

!!Count retired instructions in minstret
