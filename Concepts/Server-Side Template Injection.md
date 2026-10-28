---
tags: [concept, web, injection]
---
## What It Is
Web frameworks often use templating engines (Jinja2 for Python/Flask, Twig for PHP, Freemarker for Java, …) to generate dynamic HTML by embedding expressions like `{{ variable }}` in a template, which the engine evaluates and substitutes at render time. SSTI happens when **user input is inserted into the template string itself** before it's rendered, rather than only ever being passed in as a *variable value* to a fixed, trusted template.

## Why `{{7*7}}` Is the Universal Test Payload
If user input ends up being treated as template *syntax* rather than plain *data*, a template engine will actually evaluate `7*7` as an arithmetic expression and render `49` in the output. Seeing `49` rather than the literal text `{{7*7}}` echoed back is unambiguous proof that the input is being parsed and executed as template code - the same signal-before-exploit pattern as the single-quote test in [[SQL Injection|SQL injection]].

## Why This Escalates All the Way to Remote Code Execution
Templating engines are, under the hood, powerful enough to access arbitrary Python (or the host language's) objects and attributes - because templates are meant to display live application data, the engine needs a way to reach into real objects. Jinja2's object model exposes `__init__`, `__globals__`, and similar introspection attributes on virtually any object reachable from the template context. Which is exactly how a chain like reaching a built-in object → its `__globals__` dict → the imported `os` module → `os.popen(...)` lets an attacker walk from "the templating sandbox" all the way out to **arbitrary OS command execution**. Despite no obvious "run a shell command" feature ever being intentionally exposed. This is possible precisely because the engine wasn't designed to run genuinely hostile, attacker-authored template code - it assumes templates are written by developers, not submitted by users.

## The Underlying Lesson
Never build a template string by concatenating user input into it before rendering. If user content needs to appear in output, it must be passed in as a **context variable** (rendered as data, never as template syntax). This is the same data/code separation principle that underlies the fix for SQL injection and format string bugs.
