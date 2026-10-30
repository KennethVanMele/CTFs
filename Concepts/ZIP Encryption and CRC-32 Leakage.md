---
tags: [concept, crypto, zip, crc32]
---
## What It Is
A password-protected zip entry using traditional PKZIP encryption (ZipCrypto) encrypts only the file's *contents*. The surrounding metadata - filename, uncompressed/compressed size, and the CRC-32 checksum of the plaintext - lives in the zip's central directory in the clear, unaffected by how strong the archive password is. Anyone can read `zipinfo -v archive.zip` and get the exact CRC-32 of a file they can't yet decrypt.

## Why It Works as an Attack Vector
A 32-bit CRC is not a cryptographic hash - it's a short, fast error-detection checksum with no preimage resistance. For a short file, the number of possible plaintexts of that exact length can be small enough to search directly: compute the CRC-32 of each candidate plaintext and compare it to the leaked value, with no need to touch the actual ciphertext or guess the password at all. A collision on a 32-bit CRC against a single genuine candidate is roughly 1-in-4-billion, so a match found this way is for all practical purposes certain to be correct. This is the same principle a known-plaintext attack like `bkcrack` formalizes for larger files (recovering ZipCrypto's internal key state from 12+ known plaintext bytes) - here the file is small enough to skip key recovery entirely and just search the plaintext space itself.

## Why Password-Cracking Tools Mislead You Here
Tools like John/hashcat verify a zip password guess against only the last 1-2 bytes of the 12-byte ZipCrypto encryption header (a deliberate shortcut for speed), not a full decrypt-and-verify. Against a tiny, uncompressed (stored) file there's no deflate-stream sanity check to fall back on either, so that shortcut's false-positive rate dominates: with a large enough wordlist, "cracked" results are frequently just header-check collisions that don't decrypt to anything meaningful. A "strong" archive password combined with a short stored file is a strong signal to stop attacking the password and start looking at what the format leaks instead.

## The Underlying Lesson
Encryption protects the confidentiality of *content*; it rarely protects the metadata a container format stores next to that content. When a challenge insists a password is computationally unbreakable, check what the format exposes regardless of that password (size, CRC, filenames, timestamps) before spending compute trying to break the cipher head-on.
