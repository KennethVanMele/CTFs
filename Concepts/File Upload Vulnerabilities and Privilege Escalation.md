---
tags: [concept, web, privesc]
---

# File Upload Vulnerabilities and Privilege Escalation

## What it is

A web application that lets users upload files (avatars, documents, attachments) is safe only if it strictly controls *what* can be uploaded and *how* uploaded files can later be accessed/executed. An unrestricted upload vulnerability exists when the server accepts a file whose type lets it be executed as code (e.g. a `.php` file on a PHP-powered server) and then serves uploaded files from a location the web server will actually execute, rather than just display as a static file.

## Why testing with a harmless payload first matters

Uploading a trivial PHP file that just prints a fixed, harmless string and then requesting it directly is a controlled, minimal-impact test: if the server executes it (the output appears, rather than the raw PHP source being shown, or the upload being refused outright), that proves code execution is possible *before* you commit to a more invasive payload. This separates "confirming the vulnerability exists" from "exploiting it," which is good practice generally, minimal payloads first, escalate only once a precondition is proven.

## Why a one-line "web shell" turns an upload bug into a full shell

Once arbitrary PHP can run, a minimal script that passes one URL query parameter straight into a shell-command-execution function (PHP's `system()`/`exec()` family) exposes an arbitrary OS command execution primitive through that parameter, effectively granting a remote command line, with the privileges of whatever user account the web server process runs as (commonly `www-data` on many Linux web server configurations, a deliberately low-privileged account specifically so a compromised web app doesn't hand over full system control). This pattern is sometimes called a "web shell"; the exact one-liner is omitted here deliberately, since it's a well-known, directly runnable payload that security scanners and antivirus tools flag on sight, the underlying idea (attacker-controlled input reaching a command-execution function) is the part worth remembering.

## Why privilege escalation is usually the next step, not an afterthought

Landing a shell as a low-privileged service account is rarely the end goal - the interesting data (other users' files, root-only secrets) is usually inaccessible to that account by design. Checking `sudo -l` (what commands, if any, this account can run as another user, especially root, without a password) is a standard, low-cost first privilege-escalation check: a misconfiguration that allows passwordless `sudo` on *any* command (even something as innocuous-seeming as `ls`) hands over full root-equivalent file read access immediately, since `sudo <any command>` runs with root's permissions.

## The underlying lesson

Defending against this class of bug requires multiple independent layers: validate uploaded file types against an allowlist (not just a blocklist of known-bad extensions, which is easy to evade with alternate extensions/MIME types), store uploads outside any directory the web server will execute code from, and apply least-privilege so that even full compromise of the web process doesn't trivially escalate to root via an overly permissive `sudo` configuration.
