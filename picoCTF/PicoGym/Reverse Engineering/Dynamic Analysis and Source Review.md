---
tags: [picoctf, reverse-engineering, gdb, source-review]
platform: picoCTF
category: Reverse Engineering
---

# Dynamic Analysis and Source Review

Covers: Need For Speed, Flag Hunters.

## Need For Speed

1. `main` leads to `print_flag`, gated by a key.
2. The function before `print_flag` is `get_key`, which uses `calculate_key`, a timer running much slower than the one set by `set_timer`.
3. Run it in GDB to skip the wait instead of actually waiting:
   ```
   gdb ./need-for-speed
   break set_timer   # set a breakpoint
   r                 # run the program
   return            # return empty, accept the prompt with y
   step               # continue
   ```

Observing and bypassing a slow timer check at runtime is far faster than statically computing when it would naturally complete.

## Flag Hunters

Given the source code, printing `song_lines` shows object 0 contains the flag, but the script normally starts execution at `[VERSE1]` (object 1), skipping past it. However, the code lets you sing along with unsanitized input:
```python
elif re.match(r"CROWD.*", line):
    crowd = input('Crowd: ')
    song_lines[lip] = 'Crowd: ' + crowd
    lip += 1
elif re.match(r"RETURN [0-9]+", line):
    lip = int(line.split()[1])
```
Since `;` is treated as a delimiter and `RETURN` jumps execution to a specific line index, entering `;RETURN 0` as crowd input jumps back to object 0, which holds the flag. No space between `;` and `RETURN`.

## Why

Need For Speed is a case for dynamic analysis over static analysis (see [[Reverse Engineering and Disassembly Basics]]): a timing-based check is far easier to skip at runtime in a debugger than to reason about by reading code alone. Flag Hunters is really an unsanitized-input bug: user-supplied text being parsed as part of the program's own control-flow syntax (a `RETURN` command), the same class of mistake as [[SQL Injection]] or [[Server-Side Template Injection]], just in a bespoke mini-language instead of SQL or a templating engine.
