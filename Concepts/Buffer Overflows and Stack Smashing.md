---
tags: [concept, pwn, memory-corruption]
---
## What It Is
A buffer overflow happens when a program writes more data into a fixed-size buffer than that buffer can hold. In C/C++, nothing stops this automatically - functions like `gets()`, `strcpy()`, or an unchecked `read()` will happily keep writing past the end of an array. On the stack, that overflow doesn't just corrupt the buffer itself. It overwrites whatever memory comes after it, which includes other local variables, saved registers, and critically, the **saved return address** - the address the CPU jumps back to when the current function returns.

## Why It Works
The stack is just a region of memory the CPU uses as a scratchpad, growing downward. A typical stack frame looks like (from low to high addresses): local variables → saved base pointer (`rbp`/`ebp`) → saved return address → arguments. If a local buffer sits below the return address in memory and the program writes past the buffer's bounds without checking, the attacker's input keeps going and eventually lands on - and overwrites - that return address. When the function hits `ret`, the CPU doesn't know the address changed; it just pops whatever 4 or 8 bytes are sitting there and jumps to it. If the attacker controls those bytes, they control where execution goes next.

This is why overflow exploits are usually built in two phases:
1. **Find the offset** - fill the buffer with a known, unique pattern (e.g. a long run of `A`s, or `AAAA...BBBBCCCCDDDD...`) and see how much data it takes before the program crashes or behaves differently. The exact byte offset to the return address is found by noticing which 4/8-byte chunk ends up in a register like `EIP`/`RIP` at the crash.
2. **Control the jump target**: once the offset is known, replace those bytes with a real address. Either the address of a `win()`/`flag()` function already in the binary (a "ret2win"), or, for more advanced exploits, shellcode placed in the buffer itself that the return address is redirected into.

Endianness matters here: x86/x86-64 is little-endian, so an address like `0x080485e6` must be written into memory as the byte sequence `e6 85 04 08`, reversed from how a human would read it.

## Why Mitigations Change the Attack
- **Stack canaries**: a random value placed just before the return address; if it's been overwritten when the function returns, the program aborts. Defeated by leaking the canary value first, or avoiding overwriting it.
- **NX / DEP (No-eXecute)**: marks the stack non-executable, so you can't just jump to injected shellcode on the stack anymore - you have to reuse existing executable code (ROP, ret2libc, or ret2win).
- **PIE (Position-Independent Executable)**: randomizes the base address the whole binary is loaded at on each run, so hardcoded addresses from a previous run won't work. The trick is that *relative* offsets between functions inside the same binary stay constant even when the base address changes. So if you can leak any one address at runtime, you can compute the address of any other function by adding the fixed offset between them that you measured statically (with a disassembler) or across repeated runs.
- **ASLR**: randomizes addresses of the stack, heap, and shared libraries, for the same reason as PIE, making it harder to guess where injected code or useful functions will land.

## Where This Shows up in This Vault
See the Binary Exploitation [[Basic Penetration Testing|notes]] (`handy-shellcode`, `OverFlow 0`, `OverFlow 1`, `PIE Time`, `heap 0`) for worked examples of offset-finding, endianness handling, and defeating PIE by leaking a relative address.
