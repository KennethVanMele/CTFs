---
tags: [picoctf, forensics, hashing, ssh]
platform: picoCTF
category: Forensics
---
Covers: Verify, Scan surprise.
## Verify
1. Connect over SSH as instructed.
2. `ls` to find `checksum.txt`, `decrypt.sh`, and a `files/` folder.
3. `cat checksum.txt` to get the target checksum.
4. Find the matching file: `sha256sum ./files/* | grep <checksum>`
5. `./decrypt.sh ./files/<matched file>`

A cryptographic hash uniquely fingerprints a file's exact contents, so matching a target checksum against a folder of candidates identifies which specific file is the right one, without needing to inspect each file's contents individually first.

## Scan Surprise
The zip file contains an image. Connect to the provided SSH session to scan a QR code rendered by the remote environment.

A QR code is just another visual encoding of data, like Base64 is a textual one, nothing cryptographic about it, just a 2D barcode format designed to be read by a camera rather than by eye.

## Why
See [[Disk and Memory Forensics]] for why integrity checks like SHA-256 are a standard forensic identification tool, and [[Encoding vs Encryption]] for why an unusual-looking representation (a QR code, a hash) isn't automatically "encrypted."
