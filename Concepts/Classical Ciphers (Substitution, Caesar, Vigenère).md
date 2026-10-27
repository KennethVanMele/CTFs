---
tags: [concept, crypto, classical-ciphers]
---

# Classical Ciphers (Substitution, Caesar, Vigenère)

## What they are

These are pre-computer encryption schemes that all share one weakness: a fixed, small key space and a transformation that preserves statistical patterns in the underlying language (letter frequency, repeated structures), making them breakable by analysis rather than brute computational force.

## Caesar / ROT-N

Each letter is shifted by a fixed number of positions in the alphabet (ROT13 shifts by 13, so it's its own inverse - applying it twice returns the original text). Because there are only 25 possible non-trivial shifts for the Latin alphabet, a Caesar cipher can simply be brute-forced: try all 25 shifts and see which one produces readable text. Tools like rot13.com (or any Caesar "solver") just automate this trial - some even score candidate shifts against English letter-frequency tables to auto-pick the most plausible one.

## Substitution ciphers

A general substitution cipher maps each letter of the alphabet to a different letter, not necessarily by a fixed shift (so the mapping is an arbitrary permutation of 26 letters). This is a much bigger key space (26! possibilities) than Caesar, but it's still breakable because **letter frequency is preserved**: in English, `E` is the most common letter, `T` and `A` follow, certain two- and three-letter combinations (`TH`, `THE`, `ING`) recur constantly. A substitution-cipher solver matches the frequency distribution and common patterns of the ciphertext against known English statistics and iteratively refines a guessed mapping - this is exactly what automated "substitution cipher breaker" tools do.

## Vigenère cipher

This is a Caesar cipher whose shift amount changes letter-by-letter according to a repeating keyword (e.g. key `SOLVECRYPTO` repeating over the whole message) - look up the plaintext letter's row and the matching key letter's column in a Vigenère square (tabula recta) to find the ciphertext letter, and reverse the lookup to decrypt once the key is known. Historically this resisted simple frequency analysis because the same plaintext letter can map to different ciphertext letters depending on its position. It's broken by first guessing the key length (via repeated-pattern/Kasiski analysis or frequency correlation at different offsets) and then treating each of the resulting interleaved subsequences as its own independent Caesar cipher, solvable by frequency analysis.

## Morse code and other encodings disguised as "ciphers"

Not every obfuscation is a cipher in the cryptographic sense - Morse code is just a different *encoding* of letters as dots/dashes (or in CTF challenges, as tapping/audio patterns), with no key at all. It "looks" cryptic but is fully public and reversible by anyone who knows the mapping, same as Base64 (see [[Encoding vs Encryption]]).

## The underlying lesson

Any cipher whose output preserves statistical structure from the input, or which has a small enough key space to enumerate, is broken by analysis or brute force rather than by finding a flaw in the "algorithm" itself. This is why modern cryptography is built around primitives specifically designed to destroy statistical patterns (confusion/diffusion) and have astronomically large key spaces.
