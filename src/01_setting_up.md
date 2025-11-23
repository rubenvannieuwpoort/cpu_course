{
	"title": "Setting up the project"
}

This lesson starts at commit [b9d3256d69143ecab22c8b939a4d09dfe6218f72](https://github.com/rubenvannieuwpoort/course_cpu/commit/b9d3256d69143ecab22c8b939a4d09dfe6218f72).

# 1. Setting up the project

In this first session, we'll start from [this template](https://github.com/rubenvannieuwpoort/mimasa7_template), which is nothing but a Vivado project with a single design file, a testbench, and a Makefile to make programming the Mimas A7 a bit easier.

We roughly know what the structure of our processor is going to look like. As discussed before, we will build a 5-stage pipeline with fetch, decode, execute, memory, and register writeback stages. We'll make different modules for these, and to keep things structured nicely we'll create a `core` folder for all the source files that are used in the core.

Let's start with the first stage, which is the fetch stage. First, we duplicate the `top_level` module from our template, rename it to `fetch`, place it in the `core` folder, clean up the logic and input/output ports, and rename the entity to `fetch`.

!! 8ccc3ceb0fa4de89dc6853f0ffe4e722f2ba4bc5

In the core, the output of one stage will be used as the input to the next stage. To keep this a bit more manageable, we'll group the in- and outputs in *records*, which are defined in `core/types.vhd`.

!! c5cbdc2cc67d638c1fc6b460b0928063255b6fc5

It will also turn out to be useful to create constants for the "default" output of a stage. We'll define this (and possibly other constants that are used in the core) in `core/constants.vhd`. We'll use the convention of using all-caps for constants.

!! 991bd633d9116559e5ed9690a944f87bd3536015

We'll now add a placeholder for the next stage, the *decode* stage. It will be very similar to the placeholder for the fetch stage, so we just copy-paste that for now.

!! 170418100754b05531b5c2b134fdbd87e3ab61fe

The only difference is that the decode stage is not the first stage, so it takes the input from the previous stage, the fetch stage, as input.

!! 2eb69e7faf38986b4cbc614ee9ea6b65dccdc3fc

The placeholders for the register read, execute, and memory stages are similar to the one for the decode stage, so we copy-paste and rename the types, constants, and modules.

!! 43efea0c186e2f44727766987723cab687c9fec8

The register write stage is similar again, but since it is the last stage it does not have output.

!! fb1029feaa645a590e47c9b8419869257486f48e

Now, we're ready to make a module for our core. For now, it just takes the output from modules and passes it to the next module.

!! 882da985ac05896843073ebaabed4bf419058e3d

Now, we create a simple testbench for the core module.

!! 8f570f52fb6484f6628ffbc0fe02c9b594610b42

When we add all the files in Vivado and try to simulate the core, we get a wonderful error message about how empty records are not supported... *Sigh*. OK. Let's add some placeholders then.

!! ccfdd72186bba03efe5542478976e8a3f64d2808

Now, when we try to simulate `core_tb` again, it works. Of course, it does nothing, but *it works*, and we're ready to start working on the first CPU stage.
