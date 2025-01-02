section .text
global main
main:
    xor rdx,rdx
    push rdx
    mov rdi, 0x68732F6E69622F
    push rdi
    push rsp
    pop rdi
    mov rax,59
    xor rsi,rsi
    syscall
    
    mov rax, 60
    xor rdi,rdi

