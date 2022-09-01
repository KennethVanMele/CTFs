#include <stdio.h>
#include <stdlib.h>

int asm4(char* in) {
	int val;

	asm(
			"push   ebx;"
			"sub    esp, 0x10;"
			"mov    DWORD PTR[ebp - 0x10], 0x246;"
			"mov    DWORD PTR[ebp - 0xc], 0x0;"
			"jmp    _asm_27;"
		"_asm_23:"
			"add    DWORD PTR[ebp - 0xc], 0x1;"
		"_asm_27 :"
			"mov    edx, DWORD PTR[ebp - 0xc];"
			"mov    eax, DWORD PTR[ebp + 0x8];"
			"add    eax, edx;"
			"movzx  eax, BYTE PTR[eax];"
			"test   al, al;"
			"jne    _asm_23;"
			"mov    DWORD PTR[ebp - 0x8], 0x1;"
			"jmp    _asm_138;"
		"_asm_51:"
			"mov    edx, DWORD PTR[ebp - 0x8];"
			"mov    eax, DWORD PTR[ebp + 0x8];"
			"add    eax, edx;"
			"movzx  eax, BYTE PTR[eax];"
			"movsx  edx, al;"
			"mov    eax, DWORD PTR[ebp - 0x8];"
			"lea    ecx, [eax - 0x1];"
			"mov    eax, DWORD PTR[ebp + 0x8];"
			"add    eax, ecx;"
			"movzx  eax, BYTE PTR[eax];"
			"movsx  eax, al;"
			"sub    edx, eax;"
			"mov    eax, edx;"
			"mov    edx, eax;"
			"mov    eax, DWORD PTR[ebp - 0x10];"
			"lea    ebx, [edx + eax * 1];"
			"mov    eax, DWORD PTR[ebp - 0x8];"
			"lea    edx, [eax + 0x1];"
			"mov    eax, DWORD PTR[ebp + 0x8];"
			"add    eax, edx;"
			"movzx  eax, BYTE PTR[eax];"
			"movsx  edx, al;"
			"mov    ecx, DWORD PTR[ebp - 0x8];"
			"mov    eax, DWORD PTR[ebp + 0x8];"
			"add    eax, ecx;"
			"movzx  eax, BYTE PTR[eax];"
			"movsx  eax, al;"
			"sub    edx, eax;"
			"mov    eax, edx;"
			"add    eax, ebx;"
			"mov    DWORD PTR[ebp - 0x10], eax;"
			"add    DWORD PTR[ebp - 0x8], 0x1;"
		"_asm_138:"
			"mov    eax, DWORD PTR[ebp - 0xc];"
			"sub    eax, 0x1;"
			"cmp    DWORD PTR[ebp - 0x8], eax;"
			"jl     _asm_51;"
			"mov    eax, DWORD PTR[ebp - 0x10];"
			"add    esp, 0x10;"
			"pop    ebx;"
			:"=r"(val)
			:[pInput] "m"(in)
	);

	return(val);
}

int main(int argc, char** argv)
{
	printf("0x%x\n", asm4("picoCTF_a3112"));
	return 0;
}
