---
tags: [concept, pwn, logic-bugs]
---
## What It Is
Computers store integers in a fixed number of bits. When an arithmetic operation produces a result too large (or too negative) to fit in that fixed width, it **wraps around** rather than erroring.Adding 1 to the maximum representable value doesn't give "max + 1," it wraps back around to the minimum representable value (0, for unsigned types, or a large negative number, for signed types using two's complement).

## Why It Works as an Exploitable Bug
Business logic that assumes numbers only ever grow in the "normal" direction breaks completely once you can push a value past its storage limit and have it wrap around. A classic pattern: if a price or balance is stored in a fixed-width integer and the application doesn't check for overflow before or after an operation. Deliberately causing a value to wrap can produce results like an artificially enormous "balance". Enough, in a shop-style challenge, to divide that huge number by an item's price and discover you can "afford" a quantity that should have been impossible, because the true constraint was silently bypassed by overflow rather than actually satisfied.

## Why This Matters Beyond CTFs
Integer overflow bugs have caused real-world incidents ranging from game economy exploits to safety-critical failures (e.g. the Ariane 5 rocket's loss, caused by an unrelated but conceptually similar integer conversion overflow). The fix is always the same in principle: validate that arithmetic results stay within the expected, safe range *before* trusting them for a security- or safety-relevant decision. Or use arbitrary-precision/checked-arithmetic types that raise an error instead of silently wrapping.
