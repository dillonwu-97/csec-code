	.arch armv8-a
	.file	"chall_2.c"
	.text
	.align	2
	.global	func1
	.type	func1, %function

# argument: 3848786505
# is it multiply by 3 or is it first time we hit an underflow???
# 2b03776db = 3848786505 *3, then 32 bits is just b03776db
# flag: picoCTF{b03776db}
func1:
	sub	sp, sp, #32 # get stack space 
	str	w0, [sp, 12] # store value at [sp +12] = w0 <-- is this the arg
	str	wzr, [sp, 24] # [sp + 24] = wzr
	str	wzr, [sp, 28] # [sp + 28] = wzr, wzr is a zero register
	b	.L2
.L3:
	ldr	w0, [sp, 24] 
	add	w0, w0, 3 # w0+=3
	str	w0, [sp, 24] # [sp + 24] = w3; sequence: (3,)
	ldr	w0, [sp, 28] # 
	add	w0, w0, 1 # w0+= 1
	str	w0, [sp, 28] # [sp + 28] = w0; sequence: (1,)

.L2:
	ldr	w1, [sp, 28] # w1 = 0
	ldr	w0, [sp, 12] # w0 = [sp + 12] = arg?
	cmp	w1, w0 # w1 - w0; if positive, then w1 > w0
	bcc	.L3 # branch if carry clear meaning that we jump to .L3 if w1 < w0
	# if (w1 < w0): goto .L3

	ldr	w0, [sp, 24] # w0 = 0
	add	sp, sp, 32 # clear stack
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
	stp	x29, x30, [sp, -48]! # store a pair of registers: x29, x30 at location sp-48
	add	x29, sp, 0 # x29 = sp 
	str	w0, [x29, 28] # [x29 + 28] = w0
	str	x1, [x29, 16] # [x29 + 16] = x1
	ldr	x0, [x29, 16] # x0 = w0, equals 0?
	add	x0, x0, 8 # x0 += 8
	ldr	x0, [x0] # x0 = [value at x0]?
	bl	atoi

	# call func1 with the value 3848786505
	bl	func1
	str	w0, [x29, 44] # [x29 + 44] = w0

	# the next two instructions are used to load the address of LC0
	# This is just to print the result
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	ldr	w1, [x29, 44]
	bl	printf
	nop
	ldp	x29, x30, [sp], 48
	ret
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
