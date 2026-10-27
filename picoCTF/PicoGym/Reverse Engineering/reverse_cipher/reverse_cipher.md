---
tags: [picoctf, reverse-engineering, png]
platform: picoCTF
category: Reverse Engineering
---

# reverse_cipher

## Steps

Same underlying challenge as Investigative Reversing 0 in the Forensics section: the flag sits past the end of a PNG, scrambled by a transformation that needs to be reversed.

## Why

See [[PNG and Polyglot File Repair]] for the worked solution, and [[PNG File Format Internals]] / [[Reverse Engineering and Disassembly Basics]] for why appended data plus a small reversible transformation is a recurring pattern across both the Forensics and Reverse Engineering categories.
