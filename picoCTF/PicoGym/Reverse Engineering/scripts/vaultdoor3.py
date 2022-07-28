buffer = bytearray(32)
s = bytearray("jU5t_a_sna_3lpm18g947_u_4_m9r54f", encoding='utf8')
password = bytearray(x for x in range(32))

for i in range(0, 8):
    buffer[i] = password[i]
for i in range(8, 16):
    buffer[i] = password[23 - i]

for i in range(16, 32, 2):
    buffer[i] = password[46 - i]
for i in range(31, 17, -2):
    buffer[i] = password[i]

print(str(buffer.hex()))

p = bytearray(32)

for i, idx in enumerate(buffer):
    p[i] = s[idx]

print(p)
