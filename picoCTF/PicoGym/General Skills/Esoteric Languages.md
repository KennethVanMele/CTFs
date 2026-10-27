---
tags: [picoctf, general-skills, esoteric-languages]
platform: picoCTF
category: General Skills
---

# Esoteric Languages

Covers: mus1c, 1_wanna_b3_a_r0ck5tar.

## mus1c

1. The source is written in Rockstar, an esoteric language: https://codewithrockstar.com/online
2. Run it, then convert the numeric output to characters: `''.join([chr(int(x)) for x in a.split("\n") if x])`

## 1_wanna_b3_a_r0ck5tar

1. `pip install rockstar-py`
2. `rockstar lyrics.txt` to transpile/run it.
3. Same decode: `''.join([chr(int(x)) for x in a.split("\n") if x])`

## Why

See [[Esoteric Languages and Transpilation]]: Rockstar is designed to read like song lyrics, deliberately obfuscating ordinary logic rather than introducing any new technique. Running the program through its actual interpreter (rather than trying to read it by eye) and capturing its real output sidesteps needing to deeply understand the esoteric syntax, since the remaining problem (a list of integers that are character codes) is a familiar pattern.
