---
tags: [picoctf, reverse-engineering, source-review]
platform: picoCTF
category: Reverse Engineering
---

Covers: vault-door-training, vault-door-1, VaultDoor4, vaultdoor5, vaultdoor6.

## vault-door-training
Just open the file and find the flag at the bottom, a pure warmup with no actual logic to reverse.

## vault-door-1
The source checks the password one character at a time:
```javascript
password.charAt(0)  == 'd' &&
password.charAt(1)  == '3' &&
password.charAt(2)  == '5' &&
password.charAt(3)  == 'c' &&
password.charAt(4)  == 'r' &&
password.charAt(5)  == '4' &&
password.charAt(6)  == 'm' &&
password.charAt(7)  == 'b' &&
password.charAt(8)  == 'l' &&
password.charAt(9)  == '3' &&
password.charAt(10) == '_' &&
password.charAt(11) == 't' &&
password.charAt(12) == 'H' &&
password.charAt(13) == '3' &&
password.charAt(14) == '_' &&
password.charAt(15) == 'c' &&
password.charAt(16) == 'H' &&
password.charAt(17) == '4' &&
password.charAt(18) == 'r' &&
password.charAt(19) == '4' &&
password.charAt(20) == 'c' &&
password.charAt(21) == 'T' &&
password.charAt(22) == '3' &&
password.charAt(23) == 'r' &&
password.charAt(24) == '5' &&
password.charAt(25) == '_' &&
password.charAt(26) == '6' &&
password.charAt(27) == '3' &&
password.charAt(28) == 'e' &&
password.charAt(29) == 'f' &&
password.charAt(30) == '3' &&
password.charAt(31) == 'a';
```
Just read off each expected character in order to reconstruct the password directly from the comparisons.

## VaultDoor4
Python 2 can convert the encoded data to a bytearray directly, simplifying the decode compared to doing it manually.

## vaultdoor5
The encoded password is Base64, followed by a URL-safe transform.

## vaultdoor6
The check is:
```python
(passBytes[i] ^ 0x55) - myBytes[i]) != 0
```
Since `x - y != 0` is just another way of writing `x != y`, this simplifies to `(passBytes[i] ^ 0x55) != myBytes[i]`, meaning the real password is just `myBytes` XORed with `0x55`.

## Why
Most of these are source-level logic puzzles rather than binary reverse engineering. The "vulnerability" is that the comparison logic is handed to you directly, so solving it is a matter of reading the checks precisely and, for vaultdoor6, simplifying the boolean algebra to see what the check actually reduces to. See [[Reverse Engineering and Disassembly Basics]] for the broader principle that building a correct mental model of a check's logic (whatever form it's given in) is the actual [[All about .md, skills and MCP|skill]], independent of whether you're reading disassembly or plain source.
