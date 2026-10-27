---
tags: [archive, hackthebox, mysql]
platform: Hack The Box
tier: "1"
status: archived
---

# Sequel

- Structured Query Language
- Default MySQL/MariaDB port: 3306
- `nmap -sVC 10.129.154.95 -p 3306` -> MariaDB
- `-u` (user flag), `root`, `*` (wildcard), `;` (statement terminator)
- ```
  mysql -u root -h 10.129.154.95
  SHOW DATABASES;
  USE htb;
  SHOW TABLES;
  SELECT * FROM config;
  ```
