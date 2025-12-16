{
	"title": "Reading instructions from main memory"
}

This lesson starts at commit [c2c6ad9e07ff149a1de3863f1d10db636e966997](https://github.com/rubenvannieuwpoort/course_cpu/commit/c2c6ad9e07ff149a1de3863f1d10db636e966997).

# 9. Reading instructions from main memory

In the last lesson we made sure we can write to and read from the main memory. However, the instructions are still fetched from a hardcoded array of instructions. We'll change that in this lesson, so that instructions are fetched from the "real" memory.

For this, we'll need to enable the second port on the block RAM, which I commented out before.

!!Uncomment second port in block RAM

We'll need to make the variable for the RAM shared again. The instruction fetch will only need to read (not write), so we can remove some logic.

!!Clean up block RAM module

Now, we'll need update the component definition in `mem_subsys.vhd`, and hook up the new inputs and output.

!!Update memory subsystem for extra port in block RAM

Now we want to add another port to the memory subsystem that the instruction fetch can use.

!!Add a read port to the memory subsystem

Now we also need to add that read port to the core, so that the instruction fetch can access it. We're almost done with the plumbing for this one, I promise.

!!Add read port to core

Now we add a read port to the fetch stage and hook it up to the read port of the core.

!!Add mem read port to fetch stage

Now we actually want to use the memory port.

!!Drive memory port from fetch stage

If we simulate now, we just get zeros from the memory. Which makes sense, because we initialized it like that. So, erm, let's initialize it the same way as we did for the hardcoded array that we used for instruction memory until now.

!!Initialize memory contents

Let's remove those generics from the block RAM module while we're at it, we won't be using them.

!!Remove generics from block RAM

In simulation, we see now that when the `active` flag in the fetch output is set, the instruction matches what the memory returns. So we can just replace the instruction in the fetch output by the memory contents.

!!Use memory response instead of instruction memory

If we simulate this, we see it has some problems with setting the `instr` field in the fetch output. This is due to the default value, and easily fixed by setting the default value of the `instr` field to `'Z'` (high impedence).

!!Fix problem with instr field in fetch output

Now, our CPU fetches instructions from the main memory, yay!
