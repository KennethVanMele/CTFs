---
tags: [concept, crypto, rsa]
---

# RSA and Public-Key Cryptography Attacks

## The algorithm, briefly

RSA relies on the difficulty of factoring the product of two large primes. Key generation:
- Pick two large primes `p` and `q`, compute `n = p * q`.
- Compute `φ(n) = (p-1)(q-1)` (Euler's totient - counts integers below `n` coprime to it).
- Pick a public exponent `e` (often 65537) and compute the private exponent `d` such that `e*d ≡ 1 (mod φ(n))`.
- **Public key**: `(n, e)`. **Private key**: `d` (and implicitly `p, q`).
- Encryption: `c = m^e mod n`. Decryption: `m = c^d mod n`.

Breaking RSA, in practice, almost never means "solving the discrete-math problem directly" - it means finding an implementation mistake that creates a shortcut around needing to factor `n`.

## Why it's normally infeasible to break

If `n` is a product of two ~1024-bit primes, factoring it by trial division or any classical algorithm takes longer than the age of the universe with current computing power. `φ(n)` cannot be computed without knowing `p` and `q` individually - knowing `n` alone isn't enough. This is the entire basis of RSA's security.

## Common weaknesses exploited in practice

- **Small `e` with no padding (the miniRSA case)**: if the plaintext `m` is small enough and `e` is small (like 3), then `m^e` may be *smaller than `n` outright* - meaning the modulo operation never actually reduces anything. In that case `c = m^e` exactly (over the integers, no modular wraparound), and you can recover `m` by just taking the real `e`-th root of `c`. This requires arbitrary-precision integer math (e.g. Python's `gmpy2`) since `m^e` can be enormous.
- **Wiener's attack (small private exponent `d`)**: if `d` is too small relative to `n` (roughly `d < n^0.25`), the fraction `e/n` has a continued-fraction expansion that reveals `d` directly, without ever factoring `n`. Tools like `owiener` automate this continued-fraction search.
- **A weak or guessable prime factor**: if one of the "random" primes isn't actually random - e.g. generated from a small search space, or (as in the "Even RSA" example) literally `p = 2` - then `n` is trivially factorable. Any RSA modulus that's *even* is an immediate giveaway that one factor is 2, since 2 is the only even prime; dividing `n` by 2 hands you both factors instantly.
- **Reused/related moduli, common factors between multiple public keys**: if two users' `n` values share a common factor (bad random generation), computing `gcd(n1, n2)` recovers it.

## The underlying lesson

RSA's math is sound; nearly every real-world break is a **parameter-generation or padding mistake**, not a flaw in the number theory. This is why production RSA always uses proper padding schemes (OAEP), large random primes from a cryptographically secure source, and exponents chosen to avoid the small-`e`/small-`d` pitfalls above.
