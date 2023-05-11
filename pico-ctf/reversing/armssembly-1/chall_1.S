	.arch armv8-a
	.text
	.align	2
	.global	func
func:
	sub	sp, sp, #32
	str	w0, [sp, 12] # -32 + 12 = -20, [sp,12] = w0
	mov	w0, 85 # w0 = 85
	str	w0, [sp, 16] # [sp + 16] = 85
	mov	w0, 6 # w0 = 6
	str	w0, [sp, 20] # [sp + 20] = 6
	mov	w0, 3 # w0 = 3
	str	w0, [sp, 24] # [sp + 24] = 3
	ldr	w0, [sp, 20] 
	ldr	w1, [sp, 16]
	lsl	w0, w1, w0 # w0 = w1 << w0, 85 << 6
	str	w0, [sp, 28] # [sp + 28] = 5440
	ldr	w1, [sp, 28] # w1 = 5440
	ldr	w0, [sp, 24] # w0 = 3
	sdiv	w0, w1, w0 # 5440 / 3 = 1813
	str	w0, [sp, 28] # [sp + 28] = 1813
	ldr	w1, [sp, 28] # w1 = 1813
	ldr	w0, [sp, 12] # w0 = arg1?
	sub	w0, w1, w0 # w0 = 1813 - arg1
	str	w0, [sp, 28] # 
	ldr	w0, [sp, 28]
	add	sp, sp, 32
	ret
	.size	func, .-func
	.section	.rodata
	.align	3
.LC0:
	.string	"You win!"
	.align	3
.LC1:
	.string	"You Lose :("
	.text
	.align	2
	.global	main
	.type	main, %function
main:
	# what is the input to main?
	# stp = store pair of pointers 
	# x29 = frame pointer
	# x30 = link register, stores return address of the function call 
	# ! 
	stp	x29, x30, [sp, -48]!

	add	x29, sp, 0
	str	w0, [x29, 28] # [x29 + 28] = w0
	str	x1, [x29, 16] # [x29 + 16] = x1
	# [x29, 16] = 6

	ldr	x0, [x29, 16] # x0 = x1
	# x0 = 6

	add	x0, x0, 8 # x0 = x0 + 8
	# 6 + 8 = 14
	# i feel like this doesn't make that much sense though

	ldr	x0, [x0] # x0 = value at address x0? 
	bl	atoi # branch link ( character -> int )
	str	w0, [x29, 44] # [x29 + 44] = w0
	ldr	w0, [x29, 44] # w0 = w0?
	bl	func 
	cmp	w0, 0

	# w0 = 0 is needed, otherwise branch to .L4 and print fail
	bne	.L4
	# this is used to print out "you win" basically 
	adrp	x0, .LC0 # load page of .LC0 target symbol?
	add	x0, x0, :lo12:.LC0 # add lower 12 bits of .LC0 to x0
	bl	puts
	b	.L6
.L4:
	adrp	x0, .LC1
	add	x0, x0, :lo12:.LC1
	bl	puts
.L6:
	nop
	ldp	x29, x30, [sp], 48
	ret
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits

# picoCTF{00000715}