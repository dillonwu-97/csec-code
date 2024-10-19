
mov     rsi, rax
mov     rax, 0x5d1745d1745d1746
mov     rdi, rdx
imul    rbx
sar     rdx, 0x2
lea     r8, [rdx+rdx*4]
lea     rdx, [rdx+r8*2]
mov     rax, rbx
sub     rax, rdx
movzx   edx, byte [rbx+rdi]
cmp     rax, 0xb
jb      0x4a77ea


rcx = length of the input


rax = const # rax
    rdi = 0 # rdi 
    rbx = 0 # rbx, counter 

    """ (high is in rdx, low is in rax) """
    rax = rbx * rax
    rdx = rax >> 64
    rax = rax % (1 << 64)
    rdx = rdx >> 2
    r8 = rdx + rdx * 4
    rdx = rdx + r8 * 2
    rax = rbx 
    rax -= rdx 
    ???
    if (rax < 0xb):
        r9d = xor_str[rax]
        rdx = rdx ^ r9d
        rbx += 1
        rax = rsi 
        rdx = rdi 



