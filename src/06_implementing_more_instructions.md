{
	"title": "Implementing more instructions"
}

This lesson starts at commit [52ad976f12300a37998296b9861bfa7bccabac4a](https://github.com/rubenvannieuwpoort/course_cpu/commit/52ad976f12300a37998296b9861bfa7bccabac4a).

# 6. Implementing more instructions

After the hopefully fun diversion in the last lesson, we are back to work. There are 40-ish instructions in the RISC-V base instruction set, and we have only implemented two so far. Let's bang out some more instructions!

Let's grab the RV32/64G Instruction Set Listings of the RISC-V docs.

First, let's just add variables for all the bit fields we don't have yet.

!! 93ca42239a415e1d90289bff162d472226357e77

Now, let's just add the structure for recognizing opcodes. I won't actually handle the instructions yet. I'll follow the order in the RV32/64G Instruction Set Listings.

First, we do `LUI`, `AUIPC`, `JAL`, and `JALR`.

!! acd53719230a0e7a97c1aa1f1fc97350ce6b9bbd

