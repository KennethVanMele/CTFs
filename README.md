---
tags: [index]
---
# CTFs

A collection of CTF challenges I've completed, mostly picoCTF, with notes on both *how* each one was solved and *why* the underlying technique works. Built as an Obsidian vault: open this repo's root folder directly as an Obsidian vault to get backlinks, the graph view, and tag search.

## Structure

- **`Concepts/`**, the "why" layer. Each file explains one underlying security/CS concept (buffer overflows, SQL injection, steganography, [[RSA Attacks|RSA attacks]], etc.) in depth, independent of any specific challenge. Every challenge note links back to the relevant concept page(s) with double-bracket wikilinks.
- **`picoCTF/PicoGym/<Category>/`**, challenge notes grouped by category (Binary Exploitation, Cryptography, Forensics, General [[All about .md, skills and MCP|Skills]], Reverse Engineering, Web exploitation). Within a category, notes combine challenges that share the same underlying technique into one file, rather than one file per challenge, so related solutions and their shared "why" sit next to each other.
- **`Hackarcana/`**, write-ups from Hackarcana challenges.
- **`Archive/`**, old TryHackMe and Hack The Box notes. Kept for reference but not actively maintained, lighter on explanation than the picoCTF/Concepts material.

## Tagging

Every note carries YAML frontmatter with `tags`. Conventions:
- `picoctf`, `hackarcana`, `archive`, `concept`, mark where a note lives.
- A technique tag per topic, e.g. `buffer-overflow`, `sql-injection`, `steganography`, `rsa`, `classical-cipher`.
- Use Obsidian's tag pane or search (`tag:#sql-injection`) to pull up everything on a technique across platforms, not just within one category folder.

## Concepts Index

- [[Buffer Overflows and Stack Smashing]]
- [[Format String Vulnerabilities]]
- [[Predictable Randomness (PRNG Attacks)]]
- [[Classical Ciphers (Substitution, Caesar, Vigenère)]]
- [[RSA and Public-Key Cryptography Attacks]]
- [[Encoding vs Encryption]]
- [[Password and Hash Cracking]]
- [[Steganography]]
- [[File Metadata Analysis]]
- [[PNG File Format Internals]]
- [[Packet Capture Analysis]]
- [[Disk and Memory Forensics]]
- [[Reverse Engineering and Disassembly Basics]]
- [[Git Forensics]]
- [[Integer Overflow]]
- [[Esoteric Languages and Transpilation]]
- [[Memory Safety in Rust]]
- [[Client-Side Security Controls]]
- [[Cookies, Sessions, and JWTs]]
- [[SQL Injection]]
- [[Server-Side Template Injection]]
- [[File Upload Vulnerabilities and Privilege Escalation]]
- [[Web Proxies and Manual Testing (Burp Suite)]]

## Using This as an Obsidian Vault

1. In Obsidian: **Open folder as vault** and pick this repository's root.
2. The **graph view** shows how challenges cluster around shared concepts, useful for spotting which techniques come up repeatedly.
3. The **backlinks** panel on any `Concepts/` page lists every challenge note that uses that technique, a reverse index for free.
4. Use the **tag pane** (or a search like `tag:#steganography`) to cut across folders by technique.
5. Community plugins worth adding: **Dataview**, if you want to query/list challenges by tag in a table, and the built-in **graph** and **backlinks** views are enough to get most of the value with zero extra setup.
