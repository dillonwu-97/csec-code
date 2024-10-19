
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
