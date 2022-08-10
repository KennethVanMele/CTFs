c = bytearray(open("D:\\OneDrive - Xylos NV\\Documenten\\repos\CTFs\\picoCTF\PicoGym\\Reverse Engineering\\reverse_cipher\\rev_this", "rb").read())


for i in range(8,23):
    if i % 2 == 0:
        c[i] -= 5
    else:
        c[i] += 2

print(c)
