---
tags: [concept, web, tooling]
---
## What It Is

Burp Suite (and tools like it) sits as an intercepting proxy between your browser and the target web application. Every request leaving the browser, and every response coming back, passes through it first, where it can be inspected, paused, and edited before being forwarded. This is fundamentally different from just using browser dev tools, because it lets you intercept and rewrite requests **before the server ever sees the original version** - not just observe traffic after the fact.

## Why "Repeater" Is the Core Manual-Testing Workflow
Sending a captured request to Repeater lets you resend the *same* request over and over with small, deliberate edits, without needing to re-trigger the original action from the browser's UI each time. This is exactly how a server-side logic flaw gets tested: capture a legitimate request once. Then systematically remove or alter one field at a time and resend it, to see whether the server actually re-validates that the field is present and correct, or whether it was only ever checked client-side / optionally. If the server accepts the request without a field the application flow normally insists on, that's a strong sign the check isn't properly enforced server-side.

## Why Intercepting *Responses*, Not Just Requests, Matters
Some logic only reveals itself by altering what the server sends *back* before it reaches the browser. For example: intercepting a response and changing a field's value before the JavaScript that reads it ever runs, to test how the client-side code reacts to a value the server was never actually supposed to send. This is a step beyond simply editing requests, and is why Burp's "intercept response" option exists as a distinct toggle.

## The Underlying Lesson
A browser's own network tab is read-mostly - great for observation, poor for systematic request tampering. An intercepting proxy turns "what does this request look like" into "what happens if I change exactly this one thing and nothing else," which is the actual scientific method applied to web testing. Isolate one variable, observe the server's real behavior, repeat.
