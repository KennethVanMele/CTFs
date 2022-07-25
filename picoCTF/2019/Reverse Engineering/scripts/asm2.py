#each part of stack is 4-bits
#                          v ebp
#[  a ][  b ][  c ][   d ][OEBP][RET ][ARG1][ARG2]
#asm2:
#	<+0>:	push   ebp
#	<+1>:	mov    ebp,esp
def asm2(arg1, arg2):
	#	<+3>:	sub    esp,0x10
	#	<+6>:	mov    eax,DWORD PTR [ebp+0xc]
	#ebp + 12 = arg2
	#	<+9>:	mov    DWORD PTR [ebp-0x4],eax
	#ebp-4 = d
	d = arg2
	#	<+12>:	mov    eax,DWORD PTR [ebp+0x8]
	#ebp + 8 is arg1
	#	<+15>:	mov    DWORD PTR [ebp-0x8],eax
	#ebp-8 = c
	c = arg1
	#	<+18>:	jmp    0x50c <asm2+31>; goto +31

	#	<+20>:	add    DWORD PTR [ebp-0x4],0x1
	#	<+24>:	add    DWORD PTR [ebp-0x8],0xd1
	#d += 1
	#c += 0xd1

	#this is an if
	#	<+31>:	cmp    DWORD PTR [ebp-0x8],0x5fa1
	#	<+38>:	jle    0x501 <asm2+20>; jle=jump less or equal
	#if c <= 0x5fa1:
	#	goto +20
	#line21-30 = while loop
	while c<=0x5fa1:
		d += 1
		c += 0xd1

	#	<+40>:	mov    eax,DWORD PTR [ebp-0x4]
	#	<+43>:	leave
	#	<+44>:	ret
	return d

print(hex(asm2(0x4,0x2d)))
