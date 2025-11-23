# CPU course

## Lessons

{%TOC%}


## FAQ

### What is this?

It's a course for making your own [CPU](https://en.wikipedia.org/wiki/Central_processing_unit) (or, more accurately, [SOC](https://en.wikipedia.org/wiki/System_on_a_chip)) on an [FPGA](https://en.wikipedia.org/wiki/Field-programmable_gate_array).


### Why?

For fun.


### What are the prerequisites?

I will use:
- [VHDL](https://en.wikipedia.org/wiki/VHDL), which is a somewhat popular choice for high-level synthesis languages (the other popular choice being [Verilog](https://en.wikipedia.org/wiki/Verilog))
- The [Mimas A7 development board](https://numato.com/product/mimas-a7-artix-7-fpga-development-board/).


### Can I still follow the course if I don't know VHDL?

Yes. There will be a introductory section on VHDL at the start of this course. However, hardware design requires a specific way of thinking, and if you have no experience in VHDL or hardware design, you might have to spend some time studying before it "clicks".


### Can I still follow the course if I don't have the Mimas A7 dev board?

Yes. Whenever I use hardware primitives that are specific for this board/FPGA/vendor, I will note this explicitly.

Note, however, that when the difference in hardware is bigger, the trickier it might be to "port" the CPU to your hardware. This course is intended to teach the *ideas* behind CPU design, not to let you copy and paste my code. However, hardware design can be challenging, especially when you start out, and it can be helpful to have a "known good" version of the code that you can fall back on.

In general, I'd recommend to stay closer to my choices when you have little experience. That is, I'd recommend the Mimas A7 board over another one. If you (have to) pick another one, I'd recommend a dev board with an AMD Artix 7.
