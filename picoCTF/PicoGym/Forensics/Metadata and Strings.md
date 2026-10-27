---
tags: [picoctf, forensics, metadata, strings]
platform: picoCTF
category: Forensics
---

# Metadata and Strings

Covers: Glory of the Garden, So Meta, DISKO1, unzip.

## Glory of the Garden

```
strings garden.jpg | grep pico
```
`strings` scans the raw file bytes for printable text runs regardless of the surrounding binary image data, so a flag embedded as plain text inside a JPEG is found without needing to understand the JPEG format at all.

## So Meta

```
exiftool pico_img.png
```
The flag was hidden in the image's metadata fields rather than its pixel data, invisible to any normal image viewer but read directly by a metadata-aware tool.

## DISKO1

```
strings disko-1.dd | grep pico
```
Same principle as Glory of the Garden, applied to a full disk image instead of a single image file. `strings` doesn't need to understand the filesystem structure at all to find a plain-text flag buried in the raw bytes.

## unzip

```
unzip flag.zip
```
No trick here, just basic archive extraction. Worth checking whether an archive is itself password-protected or nested in harder variants of this pattern.

## Why

`strings` and `exiftool` are both format-agnostic or near-format-agnostic tools, which is exactly why they're such cheap, high-value first checks on any file. See [[File Metadata Analysis]] and [[Disk and Memory Forensics]].
