---
tags: [concept, web, privesc]
---
## What It Is

A web application that lets users upload files (avatars, documents, attachments) is safe only if it strictly controls *what* can be uploaded and *how* uploaded files can later be accessed/executed. An unrestricted upload vulnerability exists when a server accepts executable filetypes and stores them where the web server runs them instead of serving them as static files.

## Why Testing with a Harmless Payload First Matters
Uploading a trivial PHP file that just prints a fixed, harmless string and then requesting it directly is a controlled, minimal-impact test. If the server executes it (the output appears, rather than the raw PHP source being shown, or the upload being refused outright), that proves code execution is possible *before* you commit to a more invasive payload. This separates "confirming the vulnerability exists" from "exploiting it," which is good practice generally, minimal payloads first, escalate only once a precondition is proven.

## Why a One-Line "Web Shell" Turns an Upload Bug into a Full Shell
Once arbitrary PHP can run, a minimal script that passes one URL query parameter straight into a shell-command-execution function (PHP's `system()`/`exec()` family) exposes an arbitrary OS command execution primitive through that parameter. This effectively grants a remote command line, with the privileges of whatever user account the web server process runs as. This commonly would be `www-data` on many Linux web server configurations, a deliberately low-privileged account specifically so a compromised web app doesn't hand over full system control). This pattern is sometimes called a "web shell" the underlying idea (attacker-controlled input reaching a command-execution function) is the part worth remembering.

## Why Privilege Escalation Is Usually the next Step, Not an Afterthought
Landing a shell as a low-privileged service account is rarely the end goal - the interesting data (other users' files, root-only secrets) is usually inaccessible to that account by design. Checking `sudo -l` is a standard, low-cost first privilege-escalation check: a misconfiguration that allows passwordless `sudo` on *any* command (even something as innocuous-seeming as `ls`) hands over full root-equivalent file read access immediately, since `sudo <any command>` runs with root's [[Manage access and permissions in Microsoft 365|permissions]].

## The Underlying Lesson
Defending against this class of bug requires multiple independent layers
- Validate uploaded file types against an allowlist (not just a blocklist of known-bad extensions, which is easy to evade with alternate extensions/MIME types)
- Store uploads outside any directory the web server will execute code from
- Apply least-privilege so that even full compromise of the web process doesn't trivially escalate to root via an overly permissive `sudo` configuration.
