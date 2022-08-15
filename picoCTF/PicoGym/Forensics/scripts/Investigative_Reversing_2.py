f = bytearray(open("encoded.bmp", "rb").read())

print(
    ''.join(
        [chr(y + 5) for y in b''.fromhex(
            hex(
                int(
                    ''.join(
                        [chr(0x30 + (x & 1)) for x in f[2000:2000 + 50 * 8]])[::-1], 2))[2:])])[::-1])
