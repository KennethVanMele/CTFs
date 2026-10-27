---
tags: [archive, hackthebox, ftp]
platform: Hack The Box
tier: "0"
status: archived
---

# Fawn

- File Transfer Protocol (FTP), port 21
- SFTP
- `ping` the target first
- `nmap -sV 10.129.154.8` -> vsftpd 3.0.3
- Unix
- `ftp -h`
- Login as `anonymous`
- Response code `230` (login successful)
- `get` to download files
