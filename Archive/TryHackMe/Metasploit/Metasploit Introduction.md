---
tags: [archive, tryhackme, metasploit]
platform: TryHackMe
room: Metasploit
status: archived
---

# Metasploit Introduction

Core terminology from the room:

- **Exploit**: a piece of code that uses a vulnerability present on the target system.
- **Vulnerability**: a design, coding, or logic flaw affecting the target system. Exploiting one can disclose confidential information or let an attacker execute code on the target.
- **Payload**: the code that actually runs on the target system once an exploit succeeds, since the exploit alone just gets you a foothold.
- **Auxiliary**: supporting modules, scanners, crawlers, fuzzers.
- **Encoders**: encode the exploit/payload, hoping a signature-based antivirus solution misses them.
- **Evasion**: distinct from encoders, not a direct attempt to evade antivirus, but related tooling.
- **Exploits**: neatly organized by target system in the framework.
- **NOPs (No OPeration)**: literally do nothing; on Intel x86 represented as `0x90`, the CPU does nothing for one cycle. Often used as padding/buffer space in exploit payloads.
