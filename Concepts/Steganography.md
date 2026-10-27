---
tags: [concept, forensics, steganography]
---

# Steganography

## What it is

Steganography hides data *inside* other, innocuous-looking data (an image, audio file, etc.) rather than making it unreadable like encryption does. The host file still opens and looks/sounds normal; the hidden payload is invisible unless you know where and how to look for it. This is fundamentally different from encryption: steganography's goal is concealment of the *existence* of a message, not making a known message unreadable (and the two are often combined  -  a stego payload can itself be encrypted).

## Why it works  -  common techniques and why each is detectable

- **Least Significant Bit (LSB) steganography**: every pixel's color value (or every audio sample) has some bits that barely affect how it looks/sounds. Overwriting just the lowest 1-2 bits of each byte with hidden data changes the image/audio imperceptibly to the eye/ear, but those bits can be systematically extracted by reading every pixel's LSB in sequence and reassembling them into bytes. This is why "extract the least significant bit of every byte starting at some offset, then read 8 at a time to rebuild a byte" is a recurring pattern  -  and why a reversed bit-order or an off-by-some-constant shift (common obfuscation on top of raw LSB) is something to test for when a direct decode produces garbage: try reversing the bit string, or shifting each decoded byte value by a small constant, since these are cheap variations a challenge author can add on top of the base technique.
- **Appended/embedded data after the "end" of a file**: many file formats have a well-defined end-of-data marker; naive viewers stop reading there, but nothing stops extra bytes from being appended after it. `strings`, a hex editor, or `binwalk` (which recognizes known file-format signatures) will reveal content a normal viewer never shows you. This is also how a "polyglot" file works: it's a single byte sequence that satisfies two different file formats' requirements at once, so two different programs (e.g. an image viewer and a PDF reader) each see a complete, valid file in the overlapping bytes, interpreting the shared data differently depending on which parser reads it.
- **Audio-encoded images (SSTV)**: Slow-Scan Television encodes an image as an audio signal (specific tone frequencies map to brightness/color), originally designed for ham radio. Software like MMSSTV demodulates that audio back into an image  -  it's the audio equivalent of steganography hiding a visual payload in a different medium, though here the "hiding" is more about encoding-as-audio than concealment.
- **Dedicated stego tools (steghide, zsteg)**: many steganography tools embed data using a known algorithm and optional passphrase. `steghide extract -sf file -p passphrase` only works if you know (or can guess/crack) the passphrase; `zsteg` specifically targets PNG/BMP LSB-style hiding and will enumerate likely encodings automatically, which is why it's a good first tool to try on an image that doesn't yield anything to `strings` or `exiftool`.

## The underlying lesson

Steganography detection generally follows a layered checklist: check metadata (`exiftool`) → check for appended/trailing data (`strings`, `binwalk`, trailing bytes in a hex editor) → check for LSB-style hiding (`zsteg`, manual bit extraction) → check for passphrase-protected embedding (`steghide`) → consider format-specific or audio-encoded tricks. None of these require breaking cryptography  -  they require knowing where people *actually* hide data and checking each spot systematically.
