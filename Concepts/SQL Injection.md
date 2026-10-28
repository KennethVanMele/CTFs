---
tags: [concept, web, injection]
---
## What It Is
SQL injection happens when user-supplied input is concatenated directly into a SQL query string rather than passed as a separate, properly escaped parameter. The database can't distinguish "data the application meant literally" from "a fragment of SQL syntax the attacker snuck in" - it just executes whatever text ends up in the final query.

## Why a Single Quote Is the Classic First Test
Most login queries look conceptually like: `SELECT * FROM users WHERE username='<input>' AND password='<input>'`. If user input is inserted into that string without escaping, typing a single quote (`'`) as part of the input closes the string literal early - everything after it is now interpreted as SQL *code*, not data. A payload like `' OR 1=1 -- ` closes the username string, adds a condition that's always true (`OR 1=1`), and then comments out (`--`) the rest of the original query (including the password check) so it never executes. This is why the query ends up matching *every* row rather than a specific user, logging the attacker in as whichever row the application picks first (often the first/admin user).

## Why It Crashes the App Before It Bypasses It
An unescaped quote with no valid matching logic often breaks the SQL syntax outright (a dangling, unclosed string), causing a database error - a 500 Internal Server Error, or a query error reflected back to the page. This crash is itself diagnostic: it confirms the input is reaching the SQL query unescaped, *before* you've figured out a payload that actually succeeds rather than merely breaking syntax.

## Why Naive Filtering ("WAF") Is Bypassable
A filter that just blocks the literal string `' OR 1=1` (or similar known-bad patterns) is pattern-matching against specific *payloads*, not against the underlying vulnerability. Endless equivalent payloads exist (`' OR 'a'='a`, `admin'--`, different comment styles, different boolean tricks) that a naive blocklist won't catch, because the actual bug (unescaped input reaching the query) is still present. Comment syntax (`-- `, note the trailing space/characters required by some SQL dialects) is specifically useful because it lets you *truncate* the rest of a query you don't control. Rather than needing to construct syntactically valid SQL for everything that follows your injection point.

## Why Obfuscation on Top of Injection (E.g. a ROT13'd Query) Doesn't Change the Core Exploit
If an error or debug output shows the query the app builds, but that text has been transformed first, your injection payload must go through the same transformation to match what the database actually receives. The underlying vulnerability (unescaped concatenation) and the exploitation logic (break out of the string, inject a boolean/comment trick) are unchanged; only the surface-level text needs translating to match.

## The Real Fix
**Parameterized queries / prepared statements.** The query structure (`SELECT * FROM users WHERE username=? AND password=?`) is sent to the database separately from the actual input values. So the database engine itself enforces that input can never be interpreted as SQL syntax. No amount of creative escaping in the input can change the query's structure, because the structure was already fixed before the values were ever substituted in.
