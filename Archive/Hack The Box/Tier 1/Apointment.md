---
tags: [archive, hackthebox, sqli]
platform: Hack The Box
tier: "1"
status: archived
---

# Apointment

Quiz answers:

- SQL stands for Structured Query Language
- One of the most common SQL vulnerability types: SQL Injection
- PII stands for Personally Identifiable Information
- OWASP Top 10 classification for this vulnerability: A03:2021-Injection
- Service/version on port 80: `nmap -p 80 10.129.206.30 -sV` -> Apache httpd 2.4.38 (Debian)
- Standard HTTPS port: 443
- A luck-based method of exploiting login pages: brute-forcing
- A folder is called a "directory" in web-application terminology
- Response code for "Not Found": 404
- Gobuster switch to discover directories (not subdomains): `dir`
- Comment-out symbol: `#`

## To get the key

```
gobuster dir --url 10.129.206.30 --wordlist ./directory-list-2.3-medium.txt
```
Found nothing useful. Visit the site through Kali's browser so the VPN connection is used. Try a basic SQL injection test (`'-`, note the trailing space).
