---
tags: [picoctf, cryptography, classical-cipher, encoding]
platform: picoCTF
category: Cryptography
---
Covers: Mod26, 13, Easy1, caesar, Tapping, la cifra de, waves over lambda, flags, interencdec.

## Mod26 / 13 (ROT13)
Both resolve to ROT13, decoded at https://rot13.com/. ROT13 shifts every letter 13 places, exactly half of the 26-letter alphabet, which makes it its own inverse: applying it twice returns the original text. "Mod26" is a direct hint at this, since the shift wraps around modulo 26.

## Caesar
Same tool, different shift: ROT4 instead of ROT13. A Caesar cipher only has 25 possible non-trivial shifts, so trying each one (or using a tool that scores candidates against English letter frequency) always finds the right shift quickly.

## Easy1 (Vigenere, Known Key)
- Cipher: `UFJKXQZQUNB`, Key: `SOLVECRYPTO`
- Using a Vigenere square: row `S`, column `U`, read off the plaintext letter, repeat per character.

With the key already known, decoding is a direct table lookup, no cryptanalysis required.

## La Cifra De (Vigenere, Unknown Key)
Solved with https://www.guballa.de/vigenere-solver. Without a known key, a Vigenere cipher is broken by automated key-length detection (frequency correlation / Kasiski-style analysis) followed by per-position Caesar-style frequency analysis.

## Waves over Lambda (General Substitution)
Solved by searching for a substitution cipher breaker. A general substitution cipher has a much larger key space than Caesar (26! possible mappings), but still preserves English letter-frequency statistics, so automated solvers that match frequency distributions against the ciphertext can recover the mapping without brute-forcing all permutations.

## Tapping (Morse Code)
Decoded at https://morsecode.world/international/translator.html. Not a cipher at all, just a public, keyless encoding of letters as dots and dashes, so there's no secret to recover, only a known mapping to reverse.

## Flags
Resolved by searching for the image/reference directly. Not every "cryptography" challenge is actually about breaking a cipher; some test whether you recognize a well-known reference (e.g. a signal flag chart) and know to search for it rather than trying to compute anything.

## Interencdec (Chained Base64 + Caesar)
1. Base64-decode the given string.
2. The result is another Base64 string, but Python's `repr()`-style output adds extra quote/`b'…'` wrapping that needs stripping before the next decode.
3. Decoding again (Base64 once more) reveals a Caesar-ciphered string.
4. CyberChef finds the right shift automatically: ROT19.

## Why
Chained encodings aren't multiple layers of security, they're the same reversible transformation applied repeatedly, and each layer is recognizable by its character set (see [[Encoding vs Encryption]]). The actual obstacle at the bottom of interencdec's [[Three challenge|three]] encoding layers is a Caesar cipher, a 25-option brute-forceable scheme, same as every other entry here (see [[Classical Ciphers (Substitution, Caesar, Vigenère)]]). The underlying theme across this whole set: these schemes are broken by frequency analysis or exhaustive search of a small key space, not by any flaw specific to the "algorithm."
