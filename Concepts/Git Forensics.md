---
tags: [concept, forensics, git]
---

# Git Forensics

## What it is

Git stores the *entire history* of a repository, not just its current state. Every commit, every previous version of every file, and every commit message ever written remains retrievable from the `.git` directory unless it's been explicitly and thoroughly purged (which most people never do) - `git log`, `git show`, and even just reading raw object files inside `.git/` can expose data the current working tree no longer shows.

## Why this is a real information-leakage risk

A commit message, by design, is meant to be permanent, human-readable documentation of a change - which makes it an easy, overlooked place to accidentally leave a secret (a flag, a password, a hardcoded key) that someone assumed would only be "temporary" or local. `.git/COMMIT_EDITMSG` specifically stores the message of the most recent commit in plain text on disk, readable without even running `git log` - a direct file read is enough.

## Why deleting a file doesn't delete its history

Removing a file in a new commit (`git rm`) only removes it from the *current* checkout; every prior commit that included that file is still fully intact in the repository's history, and `git log --all --full-history -- <path>` (or simply checking out an old commit) can recover it. This is why git repositories that were ever public, even briefly, should be treated as permanently compromised if a secret was ever committed - rotating the secret is the only real fix, not just removing it from the latest commit.

## The underlying lesson

Version control history is an append-only forensic record by default. Anything ever committed - even if later "removed" - should be assumed recoverable, which is why secrets belong in environment variables or secret managers, never in tracked files, from the very first commit.
