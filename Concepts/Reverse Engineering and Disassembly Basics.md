---
tags: [concept, reverse-engineering]
---
## What It Is

Reverse engineering a compiled binary means reconstructing what the program does without (or in addition to) its source code. You can do this by reading disassembled machine code (`objdump`, Ghidra, IDA), stepping through execution in a debugger (`gdb`), or decompiling bytecode back to a higher-level language (e.g. Android `.dex` via `jadx`).

## Why Static Analysis (Disassembly) Works
A compiled program is a direct, deterministic translation of source code into CPU instructions - nothing is hidden by the act of compiling, just made less immediately readable to a human. Disassemblers map raw machine bytes back to their mnemonic instructions (`mov`, `cmp`, `jg`, `jne`, `sub`, …), and tools like Ghidra go further, attempting to reconstruct higher-level control flow (loops, if-statements) and even approximate C-like pseudocode. Reading a sequence like "compare value to X, jump-if-greater past the next check, compare to Y, jump-if-not-equal to a different branch" is literally reconstructing the original `if`/`else` logic the source code had, instruction by instruction.

## Why Manual Translation (Asm → Python/C) Is a Valid Technique
When disassembly is long or uses unfamiliar instructions, it's often faster to **transliterate** each assembly operation into equivalent higher-level code than to mentally execute it. This works because assembly instructions map almost one-to-one onto basic operations (`sub` → subtraction, `cmp`+conditional jump → an `if`), so a faithful line-by-line translation reconstructs the original algorithm's logic even without understanding the full program at a glance.

## Why Dynamic Analysis (a Debugger) Complements Static Analysis
Some behavior is far easier to observe at runtime than to compute by reading code or validating a guess about what a function computes by just watching its actual return value. `gdb` lets you set breakpoints (pause execution at a specific function), step through instructions, and directly modify control flow turning "statically prove this check eventually passes" into "just skip past it and confirm the rest of the program behaves as expected."

## Why PIE/ASLR Change the Reverse-Engineering Workflow
When a binary's load address is randomized (PIE) or isn't fixed at compile time, addresses recorded during one run (or read directly off a disassembly) won't be valid on a different run or on the live target. But offsets *between* functions compiled into the same binary don't change - only where the whole binary is loaded does. So the practical technique is: compute the fixed offset between two functions using a disassembler or by observing it hold across several runs. Then at exploit time, leak or observe the address of one known function at runtime and add the fixed offset to find the other.

## Why Decompiling Managed/Bytecode Languages (E.g. Android) Is Different

Java/Android `.dex` bytecode retains much more structural information than raw x86 machine code (type information, method/field names unless specifically obfuscated), so decompilers like `jadx` can often reconstruct source that's close to the original, rather than just disassembly-level pseudocode. This is why Android reverse engineering tends to focus on *following call chains through readable decompiled code* rather than instruction-level analysis - the abstraction level available to you depends heavily on how much the original compilation step preserved.

## The Underlying Lesson
Reverse engineering is fundamentally about building a mental (or literal, in code) model of a program's logic from whichever representation is available - bytes, disassembly, or decompiled pseudocode. There's no single "right" tool: picking static vs dynamic analysis, and disassembly vs manual translation vs decompilation, is a judgment call based on what's fastest to reason about for the specific check you're trying to understand or bypass.
