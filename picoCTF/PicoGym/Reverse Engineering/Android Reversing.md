---
tags: [picoctf, reverse-engineering, android, jadx]
platform: picoCTF
category: Reverse Engineering
---
Covers: droids0, droids1.

## Droids0
Open the APK directly in Android Studio, the flag is visible from there without needing a dedicated decompiler.

## Droids1
1. The app's Java code is stored in a `.dex` file, not readable directly by Android Studio.
2. Open it in `jadx` instead.
3. In `main`, find `buttonClick`, which calls `getFlag`, follow it to `FlagstaffHill`.
4. It uses `R.string.password`, but that's a resource ID, not the actual password.
5. Open `resources.arsc`, then `res/values/strings.xml` to find the real string value.
6. Enter that password in the app.

## Why
See [[Reverse Engineering and Disassembly Basics]]: Android `.dex` bytecode retains much more structural information than raw x86 machine code (method/field names, unless specifically obfuscated), so a decompiler like `jadx` can reconstruct source close to the original. This is why Android reversing tends to focus on following call chains through readable decompiled code rather than instruction-level analysis, and why resource indirection is a common extra step. The real value lives in a separate resource table, not inline in the code that references it.
