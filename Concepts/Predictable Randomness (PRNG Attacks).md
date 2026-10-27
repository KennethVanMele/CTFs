---
tags: [concept, pwn, crypto]
---

# Predictable Randomness (PRNG Attacks)

## What it is

A Pseudo-Random Number Generator (PRNG) produces a sequence of numbers that *looks* random but is entirely determined by its starting value, the **seed**. Given the same seed, a PRNG always produces exactly the same sequence. This is a feature for reproducibility (simulations, tests) but a serious vulnerability when that "randomness" is being used for anything security-relevant  -  session tokens, password-reset codes, or (as in this vault's example) a game or challenge that expects you to "guess" a supposedly random number.

## Why it works

Many programs seed their PRNG with something that looks varied but is actually easy to reconstruct  -  most commonly `time(0)`, the current Unix timestamp in seconds. An attacker who connects to the service and reads/writes to it at roughly the same wall-clock time can seed their *own* identical PRNG (e.g. Python's `random.seed(int(time.time()))`, matching the target's `C` `srand(time(0))` if the algorithms match, or re-implementing the same generator) and reproduce the exact same "random" output locally  -  defeating the illusion of unpredictability entirely.

Because the window of uncertainty is just clock skew between attacker and target (usually a second or two), it's practical to just try a small range of nearby timestamps if an exact match fails, or to seed and immediately pipe the result to the target over netcat in the same command so the timestamps are seconds apart at most.

## The underlying lesson

**Never use a general-purpose PRNG seeded from a predictable value (time, PID, counter) for anything security-sensitive.** Use a cryptographically secure random number generator (`/dev/urandom`, `os.urandom`, `secrets` module in Python) which is designed to be unpredictable even if an attacker knows roughly when it was invoked.
