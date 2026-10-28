---
tags: [concept, pwn, crypto]
---
## What It Is
A Pseudo-Random Number Generator (PRNG) produces a sequence of numbers that *looks* random but is entirely determined by its starting value, the **seed**. Given the same seed, a PRNG always produces exactly the same sequence. This is a feature for reproducibility (simulations, tests) but a serious vulnerability when that "randomness" is being used for anything security-relevant.
- Session [[Tokenization|tokens]]
- Password-reset codes 
- A game or challenge that expects you to "guess" a supposedly random number.

## Why It Works
Many programs seed their PRNG with something that looks varied but is actually easy to reconstruct - most commonly `time(0)`, the current Unix timestamp in seconds. An attacker who connects to the service and reads/writes to it at roughly the same wall-clock time can seed their *own* identical PRNG if the algorithms match and reproduce the exact same "random" output locally. This defeats the illusion of unpredictability entirely.

Because the timing window is just a few seconds of clock skew, an exact timestamp match isn't critical. You can easily try nearby timestamps if it fails, or pipe the result straight to the target over netcat so the two are only seconds apart.

## The Underlying Lesson
**Never use a general-purpose PRNG seeded from a predictable value (time, PID, counter) for anything security-sensitive.** Use a cryptographically secure random number generator (`/dev/urandom`, `os.urandom`, `secrets` module in Python) which is designed to be unpredictable even if an attacker knows roughly when it was invoked.
