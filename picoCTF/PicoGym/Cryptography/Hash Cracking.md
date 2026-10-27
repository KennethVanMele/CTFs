---
tags: [picoctf, cryptography, hashing, password-cracking, hashcat]
platform: picoCTF
category: Cryptography
---

# Hash Cracking

Covers: Hashcrack.

## Steps

1. Run `hashcat` with just the hash, no mode specified. It suggests MD5 as the likely algorithm (common, and matches the hash's length/format).
2. Crack as a dictionary attack: `hashcat -m 0 -a 0 <hash> /path/to/rockyou.txt` (`-m 0` = MD5, `-a 0` = dictionary attack). Recovers `password123`, but no flag yet, just another hash.
3. Mistake: reused the same command assuming the same algorithm. Went back to identifying the new hash first.
4. It's SHA1 this time (`-m 100`). Cracked: `letmein`. Still more hashes follow.
5. Lesson learned, identify each new hash before cracking. Next one is SHA256 (`-m 1400`). Cracked: `qwerty098`.

## Why

See [[Password and Hash Cracking]]: hash cracking is a guess-and-compare search, not a mathematical reversal, which is exactly why a dictionary of real breached passwords (`rockyou.txt`) succeeds quickly against common, low-entropy human-chosen passwords. The repeated mistake here (assuming the algorithm without re-checking) shows why identifying the hash type is a required first step every time, since a different digest length/algorithm needs a different `-m` flag, and guessing wrong just wastes time comparing against the wrong hash function.
