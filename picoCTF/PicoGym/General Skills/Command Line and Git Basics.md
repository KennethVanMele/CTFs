---
tags: [picoctf, general-skills, command-line, git]
platform: picoCTF
category: General Skills
---
Covers: First Grep, Resources, strings it, what is a netcat?, First grep part II, plumbing, where-is-the-file, Binary Search, Time Machine, Super SSH.

## First Grep

```bash
cat file | grep pico
```

## Resources
Just follow the given link.

## Strings it

```bash
strings strings | grep pico
```

## What is a Netcat?

```bash
nc 2019shell1.picoctf.com 21865
```

Netcat (`nc`) opens a raw TCP connection to a host/port, the basic tool for talking to any network service directly.

## First Grep Part II

```bash
grep -r pico
```

Recursive grep searches every file under the current directory, useful when you don't know which file holds the flag.

## Plumbing

```bash
nc 2019shell1.picoctf.com 21957 | grep pico
```

Piping `nc`'s output into `grep` filters a live network response the same way you'd filter a file.

## Where-is-the-file

```bash
ls -la
cat .cant_see_me
```

`ls -la` shows hidden files (dotfiles), which a plain `ls` skips by default, they're hidden from casual listing, not access-restricted.

## Binary Search
A binary search searches from the middle: start with 500, go to 250 or 750 depending on whether the target is lower or higher, and so on. Use `low + (high - low) // 2` to compute the midpoint without overflow risk in languages where that matters.

## Time Machine
In the `.git` folder, `COMMIT_EDITMSG` holds the flag directly. See [[Git Forensics]] for why a commit message is an easy and overlooked place to accidentally leave a secret, and why git keeps that message on disk in plain text regardless of what the current working tree shows.

## Super SSH

```bash
ssh titan.picoctf.net -p 52633 -l ctf-player
```

Basic SSH connection syntax: specify a non-default port with `-p` and a login user with `-l`.

## Why
Most of these are deliberately trivial: they build fluency with the exact tools (`grep`, `nc`, `ls -la`, `ssh`) that every later, harder challenge assumes you already know cold. [[Git Forensics]] and the midpoint-search logic in Binary Search are the two entries here with a real underlying concept worth remembering past this specific challenge.
