from struct import pack, unpack


# assembly prolog: ignore
# asm3:
# 	<+0>:	push   ebp
# 	<+1>:	mov    ebp,esp


def dd(v):
    # <I = litle endian
    return pack("<I", v)


def readword(d):
    return unpack("<H", d)[0]


# dd(0) = return address and ebp on stack
stack = bytearray(dd(0) + dd(0) + dd(0xd73346ed) + dd(0xd48672ae) + dd(0xd3c8b139))

# 16b                8b 8b
# eax --> ....ax --> ah al so it's all the same register
# 	<+3>:	xor    eax,eax
# 	<+5>:	mov    ah,BYTE PTR [ebp+0xa]
ax = stack[0xa] << 8  # shift by 8 because it's the first 8 bits

# 	<+8>:	shl    ax,0x10 --> shift left: is a bit weird as it 0's the register
ax = ((ax & 0xffff) << 0x10) & 0xffff  # & 0xffff = grab last 16-bites

# 	<+12>:	sub    al,BYTE PTR [ebp+0xc]
al = ((ax & 0xff) - stack[0xc]) & 0xff  # & 0xff = grab last 8-bites
ax = (ax & 0xff00) | al  # put al in ax

# 	<+15>:	add    ah,BYTE PTR [ebp+0xd]
ah = ((ax >> 8) & 0xff) + stack[0xd]
ax = (ax & 0x00ff) | (ah << 8)

# 	<+18>:	xor    ax,WORD PTR [ebp+0x10]
ax ^= readword(stack[0x10:0x12])

print("0x%.4x" % ax)
# assembly epilog ignore
# 	<+22>:	nop
# 	<+23>:	pop    ebp
# 	<+24>:	ret
