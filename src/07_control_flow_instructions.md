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
