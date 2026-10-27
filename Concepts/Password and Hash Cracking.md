---
tags: [concept, crypto, passwords]
---

# Password and Hash Cracking

## What a hash is, and why it can be "cracked" at all

A cryptographic hash function (MD5, SHA-1, SHA-256, NTLM, bcrypt, …) is a one-way function: it's computationally infeasible to reverse the hash to recover the original input directly. "Cracking" a hash doesn't reverse the math - it **guesses** candidate inputs, hashes each one with the same algorithm, and compares the result to the target hash. If a guess produces a matching hash, that guess *is* the original input (or at least a collision, which is rare for a well-chosen hash and a specific target).

This is why password hash cracking is really a brute-force/dictionary search problem, not a cryptographic break - and why it only works well against hashes of **low-entropy secrets** like human-chosen passwords, not against random 256-bit keys.

## Why identifying the hash algorithm matters first

Different algorithms produce different-length outputs and have wildly different cracking speeds: MD5 and SHA-1 are fast to compute (billions of guesses/sec on a GPU) and are common in older or lazy systems; bcrypt/scrypt/Argon2 are deliberately slow and memory-hard, specifically to make brute-forcing expensive even at scale. Tools identify the likely algorithm by output length and format (MD5: 32 hex chars; SHA-1: 40; SHA-256: 64) before an attacker commits to a cracking strategy - guessing wrong wastes enormous compute time trying the wrong comparison function entirely.

## Dictionary attacks and wordlists

Rather than trying every possible string (infeasible for anything beyond short, simple passwords), a dictionary attack hashes every entry in a wordlist of real, previously-breached, or commonly-chosen passwords (the canonical example being `rockyou.txt`, leaked from a real breach of millions of accounts) and checks each against the target hash. This works because **humans are bad at choosing unpredictable passwords** - `password123`, `letmein`, `qwerty098` are all exactly the kind of low-entropy, pattern-following choices that dictionary attacks are built to catch quickly, long before a brute-force search would ever reach them.

## Why sequences of hashes/puzzles reward not repeating mistakes

If a challenge gives you a sequence of hashes one at a time, identify the algorithm **every time** rather than assuming it's the same as the last one - mixing up MD5 and SHA-1/SHA-256 mode flags in a cracking tool wastes time without producing a match, since the comparison is byte-for-byte against the wrong digest length/algorithm entirely.

## The underlying lesson

The real defense against hash cracking isn't a "stronger" fast hash - it's (a) a slow, memory-hard algorithm designed to resist brute force at scale, and (b) a password with enough real entropy that it isn't in - or derivable from - any wordlist.
