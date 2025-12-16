{
	"title": "Setting up a toolchain"
}

# 10. Setting up a toolchain

**This lesson will assume you're on Linux. I think it will work on MacOS, but I'm not sure. You will need WSL if you're on Windows.**

Until now, we have made our programs by hand-writing RISC-V assembly, or even raw machine code. That changes in this lesson, where we'll set up a *toolchain* for our processor. A toolchain is just a collection of tools that can be used together to write programs for a system. It often consists of a compiler, assembler, linker, and other related tools.

If you're creating binaries from one system for another system that has a different architecture, you'll probably need a *cross compiler* (although some compilers can compile for other architectures out-of-the-box, this is the exception, not the rule).

Low-level or embedded systems are usually programmed with C, and the most popular "brand" of toolchain is the GNU toolchain, containing GCC, probably the most popular C compiler. In this lesson, we'll see how to build binutils (a collection of tools for handling binaries) and set up a GCC cross-compiler. Both are part of the GNU toolchain.

On our "host" system (the system where we want to compiler the programs for our "target" system), we need to download and extract 

The exact steps are outlined on the [OS development wiki](https://wiki.osdev.org/GCC_Cross-Compiler). I put them together in a small script:
```
export BINUTILS_VERSION="2.41"
export GCC_VERSION="13.2.0"

export PREFIX="$HOME/opt/cross"
export TARGET=riscv-elf
export PATH="$PREFIX/bin:$PATH"

export DOWNLOADS="$HOME/src"
export SOURCE="$HOME/src"

mkdir -p $SOURCE
mkdir -p $DOWNLOADS

cd $DOWNLOADS

wget https://ftp.gnu.org/gnu/binutils/binutils-${BINUTILS_VERSION}.tar.xz
wget https://ftp.gnu.org/gnu/gcc/gcc-${GCC_VERSION}/gcc-${GCC_VERSION}.tar.xz

tar -xf binutils-2.41.tar.xz
tar -xf gcc-13.2.0.tar.xz

cd $SOURCE
mkdir build-binutils
cd build-binutils
../binutils-${BINUTILS_VERSION}/configure --target=$TARGET --prefix="$PREFIX" --with-sysroot --disable-nls --disable-werror
make
make install

cd $SOURCE
mkdir build-gcc
cd build-gcc
../gcc-${GCC_VERSION}/configure --target=$TARGET --prefix="$PREFIX" --disable-nls --enable-languages=c,c++ --without-headers
make all-gcc
make all-target-libgcc
make install-gcc
make install-target-libgcc
```

This will download, extract, and compile GCC and binutils, and install them in `~/opt/cross/bin`. For me, the script took about 20 minutes to execute. After it has finished we can add `~/opt/cross/bin` to our `PATH` environment variable by adding something like this in our `.bashrc` (or similar file for whatever shell you use):
```
export PATH="$HOME/opt/cross/bin:$PATH"
```

Let's take the following test program:
```
#include <stdint.h>

uint32_t fib(uint32_t n) {
	if (n <= 1) return n;
	return fib(n - 2) + fib(n - 1);
}

int main(int argc, char *argv[]) {
	return fib(17);
}
```

Now, we can invoke the compiler as `riscv-elf-gcc`. However, we are compiling for a very bare-bones environment and need to take some precautions. For example, there is no C runtime on our CPU, which means we cannot use the C library. This means we have to tell the compiler to generate a "freestanding" binary (with the `-ffreestanding` flag), and not to include the C standard library (with the `-nostdlib` flag).

Execution of a C program starts at the `_start` function. We'll implement that in an assembly file, by just calling `main` and then hanging.

`start.s`:
```
.section .text
.global _start

_start:
call main
1: j 1b
```

Since our CPU just starts executing at address `0`, we need to make sure that the `_start` symbol is placed at address `0`. This can be done with a linker script.

`linker.ld`:
```
ENTRY(_start)
SECTIONS {
  . = 0x0;
  .text : {
    KEEP(*(.text._start))
    *(.text*)
  }
  .rodata : { *(.rodata*) }
  .data : { *(.data*) }
  .bss  : { *(.bss*)  }
}
```

We use the linker script with the `-T linker.ld` flag.

Further, we need to tell GCC what exact RISC-V architecture to target. We target RV32I, so we add the `-march=rv32i` flag. We also need to specify an ABI, because the default ABI (`ilp32d`) requires floating point registers from the D extension. So we set it to the `ilp32` ABI that does not need the D extension with the `-mabi=ilp32` flag.

All in all, we get
```
riscv-elf-gcc -march=rv32i -mabi=ilp32 -nostdlib -ffreestanding -O2 start.S main.c -T linker.ld -o prog.elf
```

This produces an output file `prog.elf`. This is an ELF file, a binary format commonly used on Linux. However, to execute an ELF file we need to "load" it: Parse the contents and put it in memory in the specified way. This is quite complicated and we want to just put the binary into memory. We can do this by extracting the binary with `objcopy`:
```
riscv-elf-objcopy -O binary prog.elf prog.bin
```

We now have a file containing the binary. The only thing that's left is to convert this binary to hexadecimal values which can be put in the VHDL source code. For this, I wrote a simple Python script.

`process.py`:
```
#!/usr/bin/env python

SIZE=4096
LINE=8
DEFAULTWORD = 'X"00000000"'

data=[]

inputdata = open('prog.bin','rb').read()
pad = (-len(inputdata)) % 4
inputdata += b'\x00' * pad
for i in range(0, len(inputdata), 4):
    w = inputdata[i:i+4]
    val = int.from_bytes(w, 'little')
    data.append(f'X"{val:08x}"')

oldsize = len(data)
for i in range(oldsize, SIZE):
    data.append(DEFAULTWORD)

i = 0
while i < SIZE:
    print(', '.join(data[i:i+LINE]) + ('' if i + LINE >= len(data) else ','))
    i += LINE
```

Now, we can compile a program as follows:
```
$ ls
compile.sh linker.ld main.c process.py start.s
$ ./compile.sh
```

This will dump a large amount of binary values to the screen; If we copy it and replace the contents of the RAM in `bram.vhd` with this, our program will be executed by our CPU.

!!Add toolchain
