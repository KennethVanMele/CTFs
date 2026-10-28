---
tags: [concept, web, client-side]
---
## What It Is
Any validation, access check, or secret that lives in code or data sent *to the browser* is something the user's own browser executes, and therefore something the user fully controls. The browser's developer tools (Elements, Sources, Network, Console) let anyone read, modify, and re-run that code at will.

## Why It Never Actually Enforces Anything
The fundamental rule: **anything that happens on the client cannot be trusted by the server**, because the client is, by definition, under the end user's control. Concretely:
- A JavaScript check like comparing substrings of a password client-side is fully readable in the page source - reading the comparison values directly in Sources/the Network tab gives you the answer without ever needing to "guess."
- A `robots.txt` file is a *request* to well-behaved search engine crawlers not to index certain paths. It's advisory, not an access control, and it often inadvertently reveals the existence of hidden/unlinked pages by listing their paths explicitly, pointing an attacker exactly to a page that was "hidden" only by not being linked anywhere.
- Hiding admin functionality from a page's visible UI (CSS/JS) doesn't prevent the underlying [[Using Microsoft Foundry endpoints|API]]/page from existing or being reachable. If the restriction is purely visual, navigating directly to the URL or re-enabling a hidden element in dev tools accesses the same functionality.
- Device/viewport checks are read from client-reported, user-controllable values like the `User-Agent` string or screen dimensions - the browser's device emulation/custom device tools let you simply tell the server whatever device identity you want it to believe.
- Minified or obfuscated JavaScript (`_0x4b5b('0x3')`-style variable names, scrambled logic) isn't a security control at all - it's a transformation that keeps the exact same logic, just harder for a human to read at a glance. Browser dev tools' "pretty-print" (`{}`) un-minifies formatting for readability, and the actual logic can always be traced function-by-function (or simply run directly in the console) regardless of how unreadable the variable names are.

## Why This Translates Directly to Real-World Web Security
This is precisely the OWASP principle of **never trusting client input**. Every one of these patterns appears regularly in real applications, and the fix is always the same: re-implement every security-relevant check *on the server*, where the attacker cannot directly read or modify the enforcement logic.
