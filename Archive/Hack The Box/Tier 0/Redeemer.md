---
tags: [archive, hackthebox, redis]
platform: Hack The Box
tier: "0"
status: archived
---

# Redeemer

- `nmap 10.129.184.2 -p T:1000-9000` -> port `6379` open
- Redis, an in-memory database
- `redis-cli -h <ip>`
- `info` -> version `5.0.7`
- `select 4`
- `keys *`
- `get flag`
