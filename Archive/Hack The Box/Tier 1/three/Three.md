---
tags: [archive, hackthebox, s3, php, webshell]
platform: Hack The Box
tier: "1"
status: archived
---

# Three

- `nmap -sC -sV -sT 10.129.183.242` to count open TCP ports.
- Domain in the site's Contact section email address: `thetoppers.htb`
- Linux file used to resolve hostnames without a DNS server: `/etc/hosts`
- Sub-domain found via further enumeration:
  ```
  gobuster vhost -w /usr/share/wordlists/subdomains-top1million-5000.txt -u thetoppers.htb --append-domain
  ```
- Service running on that sub-domain: Amazon S3 (self-hosted)
- CLI utility to interact with it: `awscli`
- Command to set up the AWS CLI: `aws configure`
- List all S3 buckets: `aws --endpoint-url=http://s3.thetoppers.htb s3 ls`
- Scripting language the server runs: `aws --endpoint=http://s3.thetoppers.htb s3 ls s3://thetoppers.htb` -> PHP files present.

## Getting the flag

Since the bucket serves executable PHP, uploading a minimal PHP "web shell" (a short script that takes a URL parameter and passes it into a PHP command-execution function) and then uploading it into the bucket via the AWS CLI lets you run commands on the server through that URL parameter. The exact one-liner is intentionally omitted here, since it is a well-known, directly runnable payload that antivirus and security scanners flag on sight; it is easy to find fresh when actually needed. From there, a standard reverse shell one-liner (also omitted for the same reason) run through the web shell's command-execution parameter gives an interactive shell back to a listener on the attacker's machine, which is then used to read the flag.

## Why

See [[File Upload Vulnerabilities and Privilege Escalation]]: this server executes uploaded PHP directly, so the exploit is the same "upload a web shell, then use it to run commands" pattern as the picoCTF n0s4n1ty 1 challenge, just reaching the upload target through S3's API instead of a web form.
