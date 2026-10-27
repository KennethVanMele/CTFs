---
tags: [concept, forensics]
---

# Disk and Memory Forensics

## What it is

Disk forensics works on a raw disk/filesystem image (a `.dd` or similar byte-for-byte copy of a storage device); memory forensics works on a snapshot of a running process's or system's RAM (a heap/core dump). In both cases, you're looking at raw, mostly-unstructured bytes that happen to contain structured data (files, strings, objects) somewhere inside  -  the forensic task is finding it without needing to fully parse the underlying filesystem or memory layout.

## Why `strings` is the first tool reached for

`strings` scans a binary blob for runs of printable characters above some minimum length and prints them, with no understanding of the file's actual structure. This works because text data  -  passwords, flags, file paths, log messages  -  is stored as literal printable bytes, so it survives being embedded in an otherwise-unparsed disk image or memory dump. It's a blunt, structure-agnostic tool, which is exactly why it's so broadly useful: it doesn't need to know *anything* about filesystems or heap layout to find human-readable content buried inside them. Piping to `grep <known-prefix>` (like a flag format) narrows thousands of lines of noise to the handful actually relevant.

## Why heap/memory dumps leak sensitive data

Applications often hold sensitive data (credentials, tokens, internal file contents) in memory far longer than they're "supposed to," and debugging/diagnostic features (like a Java heap dump endpoint) can expose a full snapshot of that memory to anyone who can trigger it. Nothing in a raw memory dump is access-controlled the way the running application's own API might be  -  once you have the bytes, all of the application's working data, including things never meant to be displayed back to a user, is visible to the same blunt `strings`/`grep` approach used on disk images.

## Why integrity verification (checksums) matters in a forensic workflow

`sha256sum` (or similar) produces a fixed-size fingerprint of a file's exact contents  -  any change to the file, even one bit, produces a completely different hash. In an investigative context, matching a file's computed hash against a known-good or known-target hash **proves which specific file** (out of many candidates) is the one of interest, without needing to read or understand its contents first  -  useful when a task hands you a folder of many similar-looking files and a list of target checksums to search for.

## The underlying lesson

Raw-data forensics techniques are deliberately format-agnostic: `strings`, hashing, and brute-force scanning work *because* they don't depend on correctly parsing a specific file format or memory layout  -  making them resilient first steps even against formats you don't have a specialized parser for.
