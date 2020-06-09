#include <stdio.h>
#include <stdlib.h>

long next_dest (long seed) {
	long ret;
	asm (
		"MOV RDX, %1;"
		"MOV RAX, 0x5deece66d;"
		"IMUL RAX, RDX;"
		"LEA RCX, [RAX + 0xb];"
		"MOV EDX, 0x10001;"
		"MOV RAX, RCX;"
		"MUL RDX;"
		"MOV RAX, RCX;"
		"SUB RAX, RDX;"
		"SHR RAX, 1;"
		"ADD RAX, RDX;"
		"SHR RAX, 0x2f;"
		"MOV RDX, RAX;"
		"SHL RDX, 0x30;"
		"SUB RDX, RAX;"
		"MOV RAX, RCX;"
		"SUB RAX, RDX;"
		"MOV %0, RAX;"
		:"=r"(ret)
		:"r"(seed)
	);


	return ret;
	

}

int main(int argc, char* argv[]) {
	long in;
 	in = atol (argv[1]);
	for (int i = 0; i < 10; i++) {
		printf("%ld\n", in);
		in = next_dest(in);
	}
	return 0;
}


