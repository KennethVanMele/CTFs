---
tags: [concept, forensics, metadata]
---

# File Metadata Analysis

## What it is

Most file formats carry metadata - structured information *about* the file - separately from the main visible content. Images (JPEG, PNG, TIFF) commonly carry EXIF data (camera model, GPS coordinates, timestamps, software used, and often arbitrary custom text fields); documents carry author/editing-history metadata; many formats allow essentially free-form comment fields that aren't rendered by normal viewers.

## Why it works as an attack/analysis vector

Metadata is **not validated or sanitized by most casual viewing software** - an image viewer just shows the pixels, so nothing stops a comment field from containing an entire hidden message, a flag, or a clue, invisible unless you specifically ask to see the metadata. `exiftool` is the standard tool for extracting this: it reads and prints every metadata field a format defines, including custom/non-standard ones that a casual viewer or even a basic hex dump might not immediately draw attention to.

## Why metadata alone is sometimes a red herring

Finding *something* in metadata (like a poem, in one of this vault's challenges) doesn't mean the task is solved - it might be a decoy, a hint pointing toward a different technique (steganography, appended data) rather than the answer itself. Treat metadata as one checklist item among several (see [[Steganography]]), not a guaranteed final answer.

## The underlying lesson

Always check metadata early in file-analysis workflows - it's a near-zero-cost check (`exiftool file`) that occasionally hands you the answer directly, and even when it doesn't, it can tell you what *kind* of hiding technique to look for next (e.g. the software field naming a stego tool).
