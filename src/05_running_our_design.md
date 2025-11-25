{
	"title": "Running our design"
}

This lesson starts at commit [0fcfa0cdaf00a57a0f2da39b78b9c2c6cdfab014](https://github.com/rubenvannieuwpoort/course_cpu/commit/0fcfa0cdaf00a57a0f2da39b78b9c2c6cdfab014).

# 5. Running our design

Let's take a break from starting at simulation waveforms and try to run our design on the dev board.

It would be nice to somehow see the result of our computations, so let's add a custom instruction that displays the 8 least significant bits of a register on the LEDs of the Mimas A7.

Until now, we have only run our core in simulation. The "main" or "top level" module that will be used on the FPGA is `top_level.vhd`. It was already there in the template, we have just never used it. It already has outputs for the LEDs on the dev board. So, first, let's instantiate our core in the top level module.

!! fd8bd0e4809d702391864e5dcd2ed1fb882ad80f

To be able to set the LEDs we need to make an output for them in our core.

!! c01c79c56e152ec1587fcf21b86a3ed93695f6c3

We want to set it from the execute stage.

!! 98a1de631abe97dd3ebfa171245ea20c1703b9b7

Now, let's add an operation for setting the LED.

!! 19deb063b57b992c5ba75340e09a8e9c7c7881e7

Now, we can add our custom instruction. I'll use the `opcode` field and check if it's all ones.

!! 2bb26ad72ff3f4c33dc571516b88a4e3203dd10c

I also want to implement an instruction that makes our CPU hang. If we don't stop it, our CPU will keep executing the same 16 instructions over and over again, and it will be impossible to observe the LEDs when they keep changing thousands of times per second.

Currently, the fetch stage only fetches new instructions when an instruction is done, which is detected by observing the `is_active` flag. So, we can simply add an instruction that does not set `is_active`, and the fetch stage will stop, halting the entire pipeline.

!! b1b1acd0d86bb54bd072611e0f1e97fa96ebe71d

I've dubbed this custom instruction `HANG`.

Can we do anything interesting with 16 instructions? If we set `x2` to `1` with `ADDI x2, x2, 1`, and then alternatingly do `ADD x1, x1, x2` and `ADD x2, x1, x2`, we can calculate the Fibonacci numbers. The even-numbered Fibonacci numbers (F0, F1, F2, ...) end up in `x1`, while the odd-numbered Fibonacci numbers (F1, F3, F5, ...) end up in `x2`.

After doing `n` iterations of the `ADD` instruction, we have computed the (`n+1`)th Fibonacci number. So if we do a single `ADDI` instruction, 11 `ADD` instructions, the `LED x2` instruction, and the `HANG` instruction, we compute the `13`th Fibonacci number in 15 instructions.

Using the online assembler again, we find that `ADDI x2, x2, 1` assembles to `00110113`, `ADD x1, x1, x2` assembles to `002080b3`, and `ADD x2, x1, x2` assembles to `00208133`.

We have to assemble our custom instructions by hand. `LED x2` assembles to `0001007f`, and `HANG` assembles to `0000107f`.

Now, we put this into our instruction memory.

!! 52ad976f12300a37998296b9861bfa7bccabac4a

If we run this with
```
make bitstream
make program
```

and check the LEDs on our dev board, we can see they display the binary pattern `11101001`. This is the binary representation of the number 233, which is indeed the 13th Fibonacci number. Success!
