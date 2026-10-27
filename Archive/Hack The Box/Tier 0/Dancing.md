---
tags: [archive, hackthebox, smb]
platform: Hack The Box
tier: "0"
status: archived
---

# Dancing

- Server Message Block (SMB)
- Port 445
- `-L` (list shares), `-4` (force IPv4)
- Share found: `WorkShares`
- `get` to download files
- ```
  smbclient \\\\10.129.171.113\\WorkShares
  ```
