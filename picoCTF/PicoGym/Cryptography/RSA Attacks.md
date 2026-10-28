---
tags: [picoctf, cryptography, rsa]
platform: picoCTF
category: Cryptography
---
Covers: rsa-pop-quiz, miniRSA, b00tl3gRSA2, Even RSA can be broken.

## Rsa-pop-quiz
A set of short conceptual RSA questions that walk through the core relationships end to end:

1. `n = p * q`
2. `q = n / p`
3. Factoring a ~2048-bit `n` directly is not feasible.
4. `phi(n) = (p - 1)(q - 1)`
5. `c = m^e mod n`, in Python: `pow(m, e, n)`
6. You cannot decrypt knowing only `n` and `e`, you need `p` and `q` to derive `d`.
7. Solved via `get-d.py`.
8. Solved via `decypherRSA.py`.

## miniRSA (Small Exponent, No Padding)
Normally `c = m^e mod n`, but if `e` is very small and `m` is small enough, `m^e` never actually exceeds `n`, so the modulo operation has nothing to reduce and `c = m^e` exactly, over the integers. Use `gmpy2` for arbitrary-precision math and take the real `e`-th root of `c` to recover `m` directly.

## b00tl3gRSA2 (Wiener's Attack)
The challenge description hints `e > d`, which points directly to Wiener's attack. Used the `owiener` tool to recover the private key. Wiener's attack recovers a small private exponent `d` via continued-fraction expansion of `e/n`, without ever factoring `n`.

## Even RSA Can Be Broken (Weak Prime)
The exponent `k` used to derive `p` and `q` is suspiciously small, and `n` always comes out even. Try assuming one of the prime factors is simply `2`. Since 2 is the only even prime, if `n` itself is even, one of its two factors must be exactly 2, so dividing `n` by 2 instantly recovers both primes.

## Why
See [[RSA and Public-Key Cryptography Attacks]] for the full algorithm and why real-world RSA breaks almost always come from a parameter-generation mistake rather than solving the underlying factoring problem directly.
