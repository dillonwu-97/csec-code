# args:
# 1765227561 and 1830628817
# useful link: https://cit.dixie.edu/cs/2810/arm64-assembly.html
# multiple ways of solving this: can create the code and run it or can try to trace it manually
# presumably arg 2 gets pushed onto the stack before arg 1 so sp + 12 is arg 2 which is 1830628817 = 0x6D1D2DD1

	.arch armv8-a
	.file	"chall.c"
	.text
	.align	2
	.global	func1
	.type	func1, %function
func1:
	sub	sp, sp, #16
	str	w0, [sp, 12]
	str	w1, [sp, 8]
	ldr	w1, [sp, 12]
	ldr	w0, [sp, 8]
	cmp	w1, w0
	bls	.L2
	ldr	w0, [sp, 12]
	b	.L3
.L2:
	ldr	w0, [sp, 8]
.L3:
	add	sp, sp, 16
	ret
	.size	func1, .-func1
	.section	.rodata
	.align	3
.LC0:
	.string	"Result: %ld\n"
	.text
	.align	2
	.global	main
	.type	main, %function
main:

	stp	x29, x30, [sp, -48]! # store pair of registers
	add	x29, sp, 0
	str	x19, [sp, 16] # [sp + 16] = x19
	str	w0, [x29, 44] # [x29 + 44] = w0
	str	x1, [x29, 32] # [x29 + 32] = x1
	ldr	x0, [x29, 32] # x0 = [x29 + 32] # x0 = arg2?
	add	x0, x0, 8
	ldr	x0, [x0]
	bl	atoi
	mov	w19, w0
	ldr	x0, [x29, 32]
	add	x0, x0, 16
	ldr	x0, [x0]
	bl	atoi
	mov	w1, w0
	mov	w0, w19
	bl	func1
	mov	w1, w0
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	bl	printf
	mov	w0, 0
	ldr	x19, [sp, 16]
	ldp	x29, x30, [sp], 48
	ret
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
