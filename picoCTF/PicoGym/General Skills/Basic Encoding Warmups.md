---
tags: [picoctf, general-skills, encoding]
platform: picoCTF
category: General Skills
---

# Basic Encoding Warmups

Covers: Lets Warm up, Warmed Up, 2Warm, Bases, Based, Undo.

## Lets Warm up

`chr(0x70)` in Python, converting a hex code point straight to its character.

## Warmed Up

`hex(0x3d)` style conversion in Python.

## 2Warm

`bin(42)` in Python, converting a decimal number to its binary representation.

## Bases

```python
import base64
base64.b64decode("bDNhcm5fdGgzX3IwcDM1")
```

## Based

Three different base conversions in one challenge:
1. Binary to character: `''.join([chr(int(x,2)) for x in "01100011 ...".split(" ")])`
2. Octal to character: `''.join([chr(int(x,8)) for x in "164 141 ...".split(" ")])`
3. Hex to string: `bytes.fromhex('736f636b6574').decode('utf-8')`

## Undo

A chain of standard encoding/text transformations applied in sequence:
```
base64 -d
rev
tr '-' '_'
tr ['(',')'] ['{','}']
tr 'A-Za-z' 'N-ZA-Mn-za-m'
```
(the last line is ROT13 implemented via character transliteration)

## Why

All of these exploit the same fact: a character is just a number (its ASCII/Unicode code point), and that number can be written in binary, octal, decimal, or hex without changing its meaning. Decoding is just parsing the number in whatever base it's presented in, then interpreting the result as a character. See [[Encoding vs Encryption]] for why recognizing the character set (only `0`/`1` for binary, `0`-`7` for octal, `0`-`9a-f` for hex, the Base64 alphabet) tells you immediately which decode to apply, and why none of this requires any secret key.
