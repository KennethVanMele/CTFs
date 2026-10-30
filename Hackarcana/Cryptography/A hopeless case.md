---
tags: [hackarcana, cryptography, zip, crc32, password-cracking]
platform: Hackarcana
category: Cryptography
---
Covers: [A Hopeless Case](https://hackarcana.com/public-exercises/gynvaels-collection/a_hopeless_case) (Gynvael's Collection). An encrypted zip (`mypassword.zip`) holds a single file, `pass.txt`, protected by a password its owner forgot.

## Steps

1. Get the zip file and extract the hash for offline cracking: `zip2john mypassword.zip > zip.hashes`
2. Try John first: `john zip.hashes --wordlist=/usr/share/wordlists/rockyou.txt`. This gives us `-swtheart-1731-..\*7¡Vamos!`. Even just `¡Vamos!` on its own doesn't work.
3. Let's try hashcat. Prepare the `zip.hashes` file: `cut -d':' -f2 zip.hashes > hashcat.ready`
4. Find the right mode: `hashcat -hh | grep -i "pkzip"`.
5. With `zipinfo mypassword.zip` we can see it's uncompressed, so let's use 17210.
6. `hashcat -m 17210 -a 0 hashcat.ready /usr/share/wordlists/rockyou.txt`
7. Still no luck, "Muffin" is also a false positive.

Both of these "cracks" are noise: John and hashcat verify a password guess against only the 1-2 check byte(s) in the ZipCrypto header, and against a 15-byte stored (uncompressed) file that check has a huge false-positive rate. Brute forcing the zip's own password this way was never going to land on something trustworthy - see [[ZIP Encryption and CRC-32 Leakage]].

8. Now this is Gynvael. He probably did some fancier stuff. Let's check the CRC info: `zipinfo -v mypassword.zip | grep -i 'crc\|uncompressed'`
9. This gives us: CRC32: `0xfe3adc6a` and a length of 15 for `pass.txt`.
10. I tried cracking with rockyou.txt while verifying the CRC:

```python
import zlib

target_crc = 0xfe3adc6a
target_len = 15

def try_candidate(raw: bytes):
    if len(raw) == target_len and zlib.crc32(raw) & 0xffffffff == target_crc:
        print("MATCH:", raw)

with open("rockyou.txt", "rb") as f:
    for line in f:
        w = line.rstrip(b"\r\n")
        try_candidate(w + b"\n")
        try_candidate(w + b"\r\n")
        try_candidate(w)
```

But no luck.

11. Ok, what if `pass.txt` just contains the flag. `HexArcana{}` is 11 bytes. That leaves 4 bytes... What if we are guessing the CRC?! 4 chars is bruteforceable:

```python
import zlib, itertools, string  
  
target_crc = 0xfe3adc6a  
prefix = b"HexArcana{"  
suffix = b"}"  
chars="abcdefghijklmnopqrstuvwxyz"  
for combo in itertools.product(chars, repeat=4):  
    inner = ''.join(combo).encode()  
    candidate = prefix + inner + suffix  
    if zlib.crc32(candidate) & 0xffffffff == target_crc:  
        print(candidate)
```

Spits out `HexArcana{fire}`: found the flag.

## Why
See [[ZIP Encryption and CRC-32 Leakage]] and [[Password and Hash Cracking]]. The title is the joke: the archive's own password really is "super strong" and brute forcing it directly is, as advertised, hopeless - and even trying feels productive at first, since weak-file-size password crackers happily hand back confident-looking garbage ("Muffin", John's nonsense string) that never actually decrypts anything.

The real exploit skips the password entirely. A zip's CRC-32 of the *plaintext* is stored unencrypted in the central directory no matter how strong the archive password is, because it's metadata about the file, not file contents. For a 15-byte file, that 32-bit checksum turns "find the password" into "find any 15-byte string with this checksum" - a search space small enough to brute force once you stop treating it as a password-guessing problem. The remaining twist was realizing the 15 bytes weren't a weak dictionary password to find in rockyou at all, but the flag itself: `HexArcana{` + `}` eats 11 of the 15 bytes, leaving a trivially small 4-character space to search directly against the CRC.

## The Underlying Lesson
When a crypto challenge's premise insists a password is "unbreakable," that's usually a signal to stop attacking the password and start looking at what the container format leaks regardless of it. A strong cipher protects confidentiality of the *content* ZipCrypto encrypts - it says nothing about the *metadata* (CRC-32, sizes, filenames) the format exposes next to that ciphertext.
