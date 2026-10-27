---
tags: [archive, hackthebox, ftp, enumeration]
platform: Hack The Box
tier: "1"
status: archived
---

# Crocodile

- Nmap default-scripts switch: `-sC`
- Service on port 21: `nmap 10.129.116.15 -sC` -> vsFTPd 3.0.3
- FTP code for "Anonymous FTP login allowed": 230
- Download files found on the server: `ftp 10.129.116.15` -> `help` -> `get`
- One of the higher-privilege-sounding usernames found: `dir` -> `get allowed.userlist` -> `exit` -> `vi allowed.userlist` -> `admin`
- Apache HTTP Server version: `nmap 10.129.116.15 -sC -sV`
- Handy web-analysis browser plugin: Wappalyzer
- Gobuster switch to specify filetypes: `-x`
- File found that gives a foothold: Wappalyzer identifies PHP, then
  ```
  gobuster dir --url 10.129.116.15 --wordlist ./wordlists/directory-list-2.3-medium.txt -x php
  ```
  finds `login.php`.
- Password found in `allowed.userlist.passwd` on the FTP server.
