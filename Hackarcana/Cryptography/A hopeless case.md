Get the zip file with `wget` and extract the hashes: `zip2john mypassword.zip > zip.hashes`
Now use `john zip.hashes --wordlist=/usr/share/wordlists/rockyou.txt` to get the password. This gives us "-swtheart-1731-..\*7¡Vamos!". Even just ¡Vamos! doesn't work.
Let's try hashcat. Prepare the zip.hashes file: `cut -d':' -f2 zip.hashes > hashcat.ready`
Now use `hashcat -hh | grep -i "pkzip"` to find the appropriate rule. 
With `zipinfo mypassword.zip` we can see it's uncompressed so let's use 17210.
`hashcat -m 17210 -a 0 hashcat.ready /usr/share/wordlists/rockyou.txt`
Still no luck "Muffin" is also a false positive.
Now this is Gynvael. He probably did some fancier stuff. Let's check the CRC info: `zipinfo -v mypassword.zip | grep -i 'crc\|uncompressed'`
This gives us: CRC32: 0xfe3adc6a and a length of 15 for pass.txt
I tried cracking with rockyou.txt while verifying the CRC:
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
Ok what if pass.txt just contains the flag. "HexArcana{}" is 11 bytes. That leaves 4 bytes... What if we are guessing the CRC?! 4 chars is bruteforceable:
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

Spits out HexArcana{fire}: found the flag.