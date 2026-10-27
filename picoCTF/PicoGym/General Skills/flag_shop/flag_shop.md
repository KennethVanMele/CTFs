---
tags: [picoctf, general-skills, integer-overflow]
platform: picoCTF
category: General Skills
---

# flag_shop

## Steps

Integer overflow: `0x80010000 // 900` gives the quantity of "knock-off flags" to buy that wraps the balance into a negative amount, which the shop interprets as being able to "pay" a negative sum rather than refusing the purchase.

## Why

See [[Integer Overflow]]: a fixed-width balance/price calculation that doesn't check for wraparound can be pushed past its storage limit, flipping the result (here, effectively granting unlimited funds) instead of erroring out. This is the same class of bug behind real-world game-economy exploits and several historical safety-critical failures.
