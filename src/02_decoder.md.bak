{
	"title": "Decoder"
}

# Decoder

Now that we have a fetch unit, we are ready to do some real work on the *decoder*.
But first, we add placeholders for the decode module and testbench.

!! 65706caf23e17572f82390811912de21a2fbea98

The decoder turns machine instructions (or *opcodes*) into *control signals*. I find it hard to give a definition for "control signals", but they basically contain the same information as an opcode, but are in a form that is more convenient.

For example, consider the `addi x2, x1, 1` instruction, which basically means "add 1 to `x1`, store the result in `x2`". The opcode for this instruction is `0x13811000`. The decode stage will turn this into separate signals, for example:
- A register that holds (a number that represents) the register that the result should be written to, `x2`
- A register that holds (a number that represents) the first operand `x1`
- A register that holds (a number that represents) the second operand, the number `1`
- A register that holds some constant that tells the ALU that it should add the operands

For our implementation, we will now assume that we have 2 operands. Both can be either "immediates" (constants extracted from the opcode) or registers, and we need two one-bit signals to indicate what type should be used. We also want to indicate the operation that the ALU should perform.

So we get the following outputs:
```
alu_function: std_logic_vector(4 downto 0);

writeback_register: std_logic_vector(4 downto 0);

operand_1_type: std_logic;
operand_1_immediate: std_logic_vector(31 downto 0);
operand_1_register: std_logic_vector(4 downto 0);

operand_2_type: std_logic;
operand_2_immediate: std_logic_vector(31 downto 0);
operand_2_register: std_logic_vector(4 downto 0);
```

We will want to output all of these to the next stage. It will be cumbersome to define and connect all these outputs separately, let's group them in a record:
```
type decode_output_type is record
	alu_function: std_logic_vector(4 downto 0);

	writeback_register: std_logic_vector(4 downto 0);

	operand_1_type: std_logic;
	operand_1_immediate: std_logic_vector(31 downto 0);
	operand_1_register: std_logic_vector(4 downto 0);

	operand_2_type: std_logic;
	operand_2_immediate: std_logic_vector(31 downto 0);
	operand_2_register: std_logic_vector(4 downto 0);
end record decode_output_type;
```

We want to use this record both in the decoder and in the read stage, which is the next stage and will process the output of the decode stage further. So, the record definition needs to be in a *package*, so that it can be shared between the modules.

We'll also add constants for the operand type.

!! c77b545edb155526463e192d932dde3fb8975af6

However, every cycle, the decoder will output the decoded signals from the opcode output by the fetch unit in the *previous* cycle. So the first cycle, the decoder will not have something valid to output, and we somehow need to signal that for this cycle the output of the decoder should be ignored. We'll also want to indicate when the opcode could not be decoded, i.e. the opcode is invalid.

We can combine both problems and add a `type` field to the output.

However, looking at the waveforms in the simulator, there is another, simpler problem: The output of the decoder is undefined for the first cycle. We'll simply fix this by setting some default values.
