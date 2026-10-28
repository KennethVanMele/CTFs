---
tags: [picoctf, forensics, png, file-formats, polyglot]
platform: picoCTF
category: Forensics
---
Covers: extensions, c0rrupt, Secret of the Polyglot, Investigative Reversing 0, Investigative Reversing 1.

## Extensions
The file's extension is misleading, checking its actual magic bytes/signature shows it's really a PNG. A file's extension is just a filename hint for the OS to pick a default handler; it carries no guarantee about the file's real format, which is determined by its content (magic-byte signature).

## c0rrupt
1. It's a PNG, run `pngcheck mystery.png`.
2. The first 8 bytes must exactly match the PNG signature: `137 80 78 71 13 10 26 10`.
3. The first chunk is always `IHDR`.
4. `pngcheck` reports the `pHYs` chunk's CRC is wrong. A chunk is `[length][name][data][crc]`; the correct length should be `9`, and the correct CRC is `38d82c82`, patch it in with a hex editor.
5. Next problem: the following `IDAT` chunk is reported as too large. Fix by zeroing out 2 bytes that were throwing off the declared size.

Because PNG's chunk structure and checksums are fully public and simple, a validator like `pngcheck` turns "this file won't open" into a precise list of exactly which byte ranges disagree with spec.

## Secret of the Polyglot
Opening the file directly shows the end of the flag and hints it's actually a PNG. Running `file` on `flag2of2-final.pdf` confirms the PDF is also a valid PNG. A polyglot file is crafted so that two different file formats' structural requirements are simultaneously satisfied by the exact same byte sequence, each parser finding what it needs starting from a different anchor point in the shared bytes.

## Investigative Reversing 0
The flag sits at the end of the PNG, but some characters are mismatched because they were run through a scrambling function called "mystery."

1. Open the binary in Ghidra.
2. `main` just prints decoy error-looking strings.
3. A function called `at_insert` performs the actual character transformation.
4. Reverse those calculations manually (hex editor) or with a short script.

Combines appended data past a file's defined end with basic static reverse engineering to recover the transformation function's logic well enough to invert it.

## Investigative Reversing 1
Starting template: `picoCTF{aaaaaaaaaaaaaaaaaaaa}`, each `a` needs replacing with a character found hidden across several PNGs, at specific positions contributed by different images (`png1`, `png2`, `png3`). A multi-source reconstruction puzzle that forces checking all the provided files rather than assuming one contains the whole answer.

## Why
See [[PNG File Format Internals]] for the chunk structure, signature, and CRC mechanics that make PNG forensics both breakable and detectable, and [[Steganography]] for why appended/polyglot data sits outside what any normal viewer reads.
