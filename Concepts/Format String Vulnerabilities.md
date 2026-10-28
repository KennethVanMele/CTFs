---
tags: [concept, pwn, memory-corruption]
---
## What It Is
Functions like `printf(fmt, ...)` in C interpret `fmt` as a template containing conversion specifiers (`%d`, `%s`, `%x`, `%n`, …) and then pull that many extra arguments off the stack to fill them in. A format string vulnerability happens when attacker-controlled data is passed *as the format string itself* - e.g. `printf(user_input)` instead of `printf("%s", user_input)`.

## Why It Works
`printf` doesn't know how many arguments were actually passed; it just trusts the format string and keeps reading from the next slots on the stack (or in registers, per the calling convention) for every specifier it sees. If the attacker supplies the format string, they can supply as many `%x`/`%p`/`%s` specifiers as they like, and `printf` will dutifully read and print whatever happens to be sitting in memory at those argument slots. Regardless of whether a real matching argument exists. This turns into:

- **Information leaks**: `%x` or `%p` repeated many times dumps raw stack contents, which can reveal canaries, addresses, or other secrets.
- **Arbitrary reads**: `%s` on a leaked pointer reads memory at that address as a string.
- **Arbitrary writes**: `%n` writes the number of bytes printed so far to the address of the corresponding argument, which can be used to overwrite values (including return addresses) if the attacker controls that address too.

A simpler, more immediate failure mode is just a crash or garbled output. Feeding something like `%114d` asks `printf` to pad an argument to 114 characters, but if that "argument" doesn't actually exist, it reads garbage off the stack and the output becomes unpredictable. A visible symptom that the input is being interpreted as a format string rather than treated as plain data.

## The Fix
Never pass user input directly as a format string. Always use `printf("%s", user_input)` so the format string is a fixed, trusted literal and user input is just a value.
