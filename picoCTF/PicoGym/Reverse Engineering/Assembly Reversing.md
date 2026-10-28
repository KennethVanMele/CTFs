---
tags: [picoctf, reverse-engineering, assembly, disassembly]
platform: picoCTF
category: Reverse Engineering
---
Covers: asm1, asm2, asm4.

## asm1
Trace the comparisons and jumps by hand:
```python
ebp = 0x2e0
cmp(0x2e0, 0x3fb) -> jg false -> continue
cmp(0x2e0, 0x280) -> jne true -> jump to asm1+29
mov ebp to eax
sub(0x2e0, 0xa) -> hex(0x2e0 - 0xa)
```
Each instruction maps directly to a basic operation, so transliterating it into Python/pseudocode step by step reconstructs the original logic.

## asm2
Same approach, but translate the whole routine into Python-equivalent "meta code" rather than evaluating it instruction by instruction, since the logic is more involved.

## asm4
Too long to trace by hand efficiently, so translate the disassembly into C code instead and compile/run it directly:
```bash
gcc -masm=intel -m32 solution.c -o solution
```

## Why
See [[Reverse Engineering and Disassembly Basics]]. Assembly instructions map almost one to one onto basic operations so a faithful line by line translation into a higher-level language reconstructs the original algorithm without needing to mentally execute the whole thing. Picking manual tracing (asm1) vs. meta-code translation (asm2) vs. full compilation (asm4) is a judgment call based on how long and how unfamiliar the instruction sequence is.
