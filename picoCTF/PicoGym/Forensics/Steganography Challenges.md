---
tags: [picoctf, forensics, steganography]
platform: picoCTF
category: Forensics
---
Covers: What Lies Within, m00nwalk, m00nwalk2, RED, Investigative Reversing 2, white pages.

## What Lies Within
LSB steganography, decoded at https://stylesuxx.github.io/steganography/. The flag is hidden in the least significant bits of the image's pixel data, imperceptible to the eye but extractable by reading the low bit of every pixel's color value in sequence.

## m00nwalk (SSTV)
The file is an SSTV (Slow-Scan Television) audio signal. Decoded with MMSSTV and VB-Cable:
1. Set VB-Cable as VLC's audio output.
2. Set VB-Cable as MMSSTV's audio input, and enable the sync indicator in its Sync tab.

SSTV encodes an image as audio tone frequencies, originally designed for ham radio. MMSSTV demodulates that audio back into the original image. VB-Cable is only needed here to route one application's audio output into another application's audio input on the same machine.

## m00nwalk2 (Steghide)
Only the first clue is needed:

```
steghide extract -sf message.wav -p hidden_stegosaurus
```

`steghide` embeds data using a known algorithm gated by a passphrase, so once you have (or guess) the passphrase, extraction is a direct, one-command operation.

## RED (Metadata Red Herring, then Zsteg)
1. `exiftool` reveals a poem in the metadata, interesting but not actually helpful.
2. The raw file shows no readable text in a hex editor, but a suspicious repeating pattern.
3. `zsteg` finds it: Base64-encoded data hidden via LSB.

The exiftool poem is a deliberate red herring; finding something in metadata doesn't mean the puzzle is solved. The real payload needed LSB-focused detection, which `zsteg` is specifically built to recognize for PNG/BMP-style bit-plane hiding.

## Investigative Reversing 2 (LSB with Reversed Bits and Byte Offset)
A script starts at the 2000th byte of a BMP and takes 50 characters' worth of data, 8 bits at a time:

1. Grab the least significant bit of each of the 400 bytes starting at offset 2000.
2. Convert the resulting binary string to decimal, then hex. The result, `0xd6`, isn't a valid printable-ASCII value, so try reversing the bit string.
3. Each resulting character is off by `-5`; add 5 back to each byte.
4. Reverse the whole string again to get the final flag.

This is raw LSB steganography with two deliberate extra twists: the bit order of the hidden stream is reversed, and each decoded byte value is shifted by a small constant. Neither twist changes the core extraction method, they're exactly the kind of cheap variation a challenge author adds to stop a naive, unmodified LSB extractor from working on the first try.

## White Pages
1. The file is UTF-8 text that visually looks like blank whitespace/blocks.
2. Replace "block" characters with `.` and spaces with `#` to reveal a visual binary pattern.
3. Shrink the viewer window to exactly 8 characters wide, so each row becomes one byte, confirming a `.`=0, `#`=1 mapping.
4. Decode each 8-character row: binary to hex to character.

Whitespace characters here encode binary data: visually indistinguishable blank-looking text that actually encodes 1s and 0s through subtle character choices. Forcing a fixed line width turns the visual layout itself into the byte boundary.

## Why
All of these rely on the same principle: changes imperceptible to casual viewing can carry arbitrary hidden data, because nothing about normal viewing/playback reads that channel. See [[Steganography]] for the full checklist (metadata, appended data, LSB, passphrase-protected tools) and why testing small variations (reversed bits, constant offsets) is worth trying when a direct decode produces garbage.
