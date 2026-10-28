---
tags: [concept, forensics, file-formats]
---
## The Structure

A PNG file is a strict sequence of **chunks**, each with the same layout: `[4-byte length][4-byte type name][data][4-byte CRC checksum]`. Every valid PNG begins with the fixed 8-byte signature `89 50 4E 47 0D 0A 1A 0A`, and the very first chunk is always `IHDR` (image header: width, height, bit depth, color type). This rigid, self-describing structure is exactly why PNGs are a popular target for "broken/corrupted file" forensics challenges: the format's rules are public and simple enough to manually verify and repair with a hex editor.

## Why Corruption Is Both Breakable and Detectable
- **Wrong signature bytes**: if the file doesn't open at all, the first thing to check is whether those first 8 bytes match the PNG spec exactly. A single altered byte there is enough to make most viewers refuse to open the file, even though the rest of the data is intact.
- **Wrong chunk length**: each chunk declares its own data length up front. If that length value is wrong, every parser downstream misreads where the chunk ends and the next one begins, cascading into garbage. But since `IHDR`'s length is always 13 by spec, a corrupted file with a different value here is an easy, deterministic fix.
- **Wrong CRC**: the checksum at the end of each chunk is computed from the chunk's type and data; tools like `pngcheck` validate it and report mismatches explicitly, telling you exactly which chunk is suspect. Recomputing the correct CRC (or, in a CTF, just patching in the value the checker says it expects) restores validity without needing to understand the checksum's internals.
- **A chunk's declared size not matching its actual content**: if a chunk's length field is wrong, everything after it is misaligned by that many bytes, corrupting the parse of every subsequent chunk. This is why fixing a PNG is often a cascading, in-order process: fix the first broken chunk, re-check, see what's broken *next*.

## Why the Flag Can Be Appended After the "End"
PNG defines an explicit end marker, the `IEND` chunk. A viewer stops there - but nothing in the file format prevents extra bytes from existing after `IEND`. Characters are appended after the image data, sometimes mangled by an earlier transformation that you have to reverse by hand. Normal image viewers won't show them. strings, a hex editor, or a script that reads past the end of the image data will.

## The Underlying Lesson
Binary file formats that are simple, well-documented, and chunk-based (PNG, ZIP, and many others) are approachable for manual forensic repair precisely *because* their spec is public - a validator like `pngcheck` turns "is this file corrupted?" into "which specific byte range disagrees with the spec?", converting a search problem into a known-location fix.
