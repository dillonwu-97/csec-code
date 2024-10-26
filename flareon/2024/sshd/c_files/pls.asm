; Filename: pls.asm
; Assembler: NASM
; Syntax: NASM

section .text
    global _start

_start:
    ; Function Prologue
    push rbp
    mov rbp, rsp
    sub rsp, 0x50            ; Allocate 80 bytes on the stack
    lea rbp, [rel data_bytes]

    ; Define offsets for clarity
    %define COUNTER 0x00
    %define KEYSTORE_3_OFFSET    0x08
    %define KEYSTORE_18H_VAL_OFFSET 0x0C
    %define KEYSTORE_38H_VAL_OFFSET 0x10
    %define VAR_68_OFFSET        0x14

    ; Original Code with Corrections
    mov     eax, dword [rbp + 0x18]                  ; eax = [rbp + 0x18]
    mov     r13d, dword [rbp + 0x00]                 ; r13d = [rbp + 0x00]
    mov     byte [rsp + 0x30 + COUNTER], 0x0A  ; [rsp + 0x30 + 0x00] = 0x0A
    mov     esi, dword [rbp + 0x10]                  ; esi = [rbp + 0x10]
    mov     ecx, dword [rbp + 0x30]                  ; ecx = [rbp + 0x30]
    mov     qword [rsp + 0x30 + KEYSTORE_3_OFFSET], rbp     ; [rsp + 0x38] = rbp
    mov     r9d, dword [rbp + 0x20]                  ; r9d = [rbp + 0x20]
    mov     r10d, dword [rbp + 0x04]                 ; r10d = [rbp + 0x04]
    mov     dword [rsp + 0x30 + KEYSTORE_18H_VAL_OFFSET], eax ; [rsp + 0x3C] = eax
    mov     eax, dword [rbp + 0x38]                  ; eax = [rbp + 0x38]
    mov     r11d, dword [rbp + 0x14]                 ; r11d = [rbp + 0x14]
    mov     edx, dword [rbp + 0x34]                  ; edx = [rbp + 0x34]
    mov     r8d, dword [rbp + 0x24]                  ; r8d = [rbp + 0x24]
    mov     ebx, dword [rbp + 0x08]                  ; ebx = [rbp + 0x08]
    mov     r12d, dword [rbp + 0x28]                 ; r12d = [rbp + 0x28]
    mov     dword [rsp + 0x30 + KEYSTORE_38H_VAL_OFFSET], eax ; [rsp + 0x40] = eax
    mov     eax, dword [rbp + 0x2C]                  ; eax = [rbp + 0x2C]
    mov     edi, dword [rbp + 0x0C]                  ; edi = [rbp + 0x0C]
    mov     r15d, dword [rbp + 0x1C]                 ; r15d = [rbp + 0x1C]
    mov     r14d, dword [rbp + 0x3C]                 ; r14d = [rbp + 0x3C]
    mov     dword [rsp + 0x30 + VAR_68_OFFSET], eax        ; [rsp + 0x44] = eax
    mov     eax, dword [rsp + 0x30 + KEYSTORE_38H_VAL_OFFSET] ; eax = [rsp + 0x40]
    nop                                             ; Replace invalid NOP with a single NOP

_loop:
    add     r10d, r11d
    add     r13d, esi
    xor     edx, r10d
    xor     ecx, r13d
    rol     edx, 0x10          ; Rotate left edx by 16 bits
    rol     ecx, 0x10          ; Rotate left ecx by 16 bits
    add     r8d, edx
    add     r9d, ecx
    xor     r11d, r8d
    xor     esi, r9d
    rol     r11d, 0xC           ; Rotate left r11d by 12 bits
    rol     esi, 0xC            ; Rotate left esi by 12 bits
    add     r10d, r11d
    add     r13d, esi
    xor     edx, r10d
    xor     ecx, r13d
    rol     edx, 8              ; Rotate left edx by 8 bits
    rol     ecx, 8              ; Rotate left ecx by 8 bits
    lea     rbx, [r8 + rdx]     ; Load effective address into rbx (64-bit)
    mov     r8d, dword [rsp + 0x30 + KEYSTORE_18H_VAL_OFFSET]
    add     r9d, ecx
    xor     esi, r9d
    xor     r11d, ebx           ; XOR r11d with lower 32 bits of rbx
    rol     esi, 7              ; Rotate left esi by 7 bits
    add     ebx, r8d
    rol     r11d, 7             ; Rotate left r11d by 7 bits
    xor     eax, ebx
    mov     dword [rsp + 0x30 + KEYSTORE_38H_VAL_OFFSET], esi
    rol     eax, 0x10           ; Rotate left eax by 16 bits
    add     r12d, eax
    xor     r8d, r12d
    mov     esi, r8d
    mov     r8d, dword [rsp + 0x30 + VAR_68_OFFSET]
    rol     esi, 0xC            ; Rotate left esi by 12 bits
    add     ebx, esi
    xor     eax, ebx
    rol     eax, 8              ; Rotate left eax by 8 bits
    add     r12d, eax
    add     edi, r15d
    add     r13d, r11d
    xor     r14d, edi
    xor     esi, r12d
    rol     r14d, 0x10          ; Rotate left r14d by 16 bits
    rol     esi, 7              ; Rotate left esi by 7 bits
    add     r8d, r14d
    add     r10d, esi
    xor     r15d, r8d
    xor     ecx, r10d
    rol     r15d, 0xC           ; Rotate left r15d by 12 bits
    rol     ecx, 0x10           ; Rotate left ecx by 16 bits
    add     edi, r15d
    xor     r14d, edi
    rol     r14d, 8             ; Rotate left r14d by 8 bits
    add     r8d, r14d
    xor     r14d, r13d
    rol     r14d, 0x10          ; Rotate left r14d by 16 bits
    xor     r15d, r8d
    add     r8d, ecx
    add     r12d, r14d
    xor     esi, r8d
    rol     r15d, 7             ; Rotate left r15d by 7 bits
    xor     r11d, r12d
    rol     r11d, 0xC           ; Rotate left r11d by 12 bits
    add     r13d, r11d
    xor     r14d, r13d
    rol     r14d, 8             ; Rotate left r14d by 8 bits
    add     r12d, r14d
    xor     r11d, r12d
    rol     r11d, 7             ; Rotate left r11d by 7 bits
    rol     esi, 0xC            ; Rotate left esi by 12 bits
    add     ebx, r15d
    add     r10d, esi
    xor     edx, ebx
    xor     ecx, r10d
    rol     edx, 0x10           ; Rotate left edx by 16 bits
    rol     ecx, 8              ; Rotate left ecx by 8 bits
    add     r9d, edx
    add     r8d, ecx
    xor     r15d, r9d
    xor     esi, r8d
    mov     dword [rsp + 0x30 + VAR_68_OFFSET], r8d
    rol     r15d, 0xC           ; Rotate left r15d by 12 bits
    mov     r8d, esi
    mov     esi, dword [rsp + 0x30 + KEYSTORE_38H_VAL_OFFSET]
    add     ebx, r15d
    rol     r8d, 7              ; Rotate left r8d by 7 bits
    xor     edx, ebx
    add     edi, esi
    mov     dword [rsp + 0x30 + KEYSTORE_18H_VAL_OFFSET], r8d
    rol     edx, 8              ; Rotate left edx by 8 bits
    xor     eax, edi
    add     r9d, edx
    rol     eax, 0x10           ; Rotate left eax by 16 bits
    xor     r15d, r9d
    lea     r8, [rbp + rax]     ; Load effective address into r8 (64-bit)
    rol     r15d, 7             ; Rotate left r15d by 7 bits
    xor     esi, r8d
    rol     esi, 0xC            ; Rotate left esi by 12 bits
    add     edi, esi
    xor     eax, edi
    rol     eax, 8              ; Rotate left eax by 8 bits
    add     r8d, eax
    xor     esi, r8d
    rol     esi, 7              ; Rotate left esi by 7 bits
    sub     dword [rsp + 0x30 + COUNTER], 1  ; Decrement counter by 1
    jnz _loop

; Store the data after modifying it 

; Filename: corrected_code.asm
; Assembler: NASM
; Architecture: x86-64

; Define memory offsets
%define COUNTER_EQ_10_OFFSET      0x00
%define KEYSTORE_3_OFFSET         0x08
%define KEYSTORE_38H_VAL_OFFSET   0x10
%define KEYSTORE_18H_VAL_OFFSET   0x0C
%define KEYSTORE_64_OFFSET_2      0x20
%define VAR_68_OFFSET             0x14
%define SOME_STACK_VAL_OFFSET     0x18

section .text
    global _start

_start:
    ; Function Prologue
    push rbp
    mov rbp, rsp
    sub rsp, 0x50                ; Allocate 80 bytes on the stack

    ; Corrected Instructions

    ; rbp = [rsp + 0x30 + KEYSTORE_3_OFFSET]
    mov     rbp, qword [rsp + 0x30 + KEYSTORE_3_OFFSET]       ; rbp = [rsp + 0x38]

    ; [rsp + 0x30 + KEYSTORE_38H_VAL_OFFSET] = eax
    mov     dword [rsp + 0x30 + KEYSTORE_38H_VAL_OFFSET], eax ; [rsp + 0x40] = eax

    ; eax = [rsp + 0x30 + KEYSTORE_18H_VAL_OFFSET]
    mov     eax, dword [rsp + 0x30 + KEYSTORE_18H_VAL_OFFSET] ; eax = [rsp + 0x3C]

    ; [rbp + 0x34] = edx
    mov     dword [rbp + 0x34], edx                          ; [rbp + 0x34] = edx

    ; rdx = [rsp + 0x30 + KEYSTORE_64_OFFSET_2]
    mov     rdx, qword [rsp + 0x30 + KEYSTORE_64_OFFSET_2]  ; rdx = [rsp + 0x50]

    ; [rbp + 0x18] = eax
    mov     dword [rbp + 0x18], eax                          ; [rbp + 0x18] = eax

    ; eax = [rsp + 0x30 + KEYSTORE_38H_VAL_OFFSET]
    mov     eax, dword [rsp + 0x30 + KEYSTORE_38H_VAL_OFFSET] ; eax = [rsp + 0x40]

    ; [rbp + 0x00] = r13d
    mov     dword [rbp + 0x00], r13d                         ; [rbp + 0x00] = r13d

    ; [rbp + 0x38] = eax
    mov     dword [rbp + 0x38], eax                          ; [rbp + 0x38] = eax

    ; eax = [rsp + 0x30 + VAR_68_OFFSET]
    mov     eax, dword [rsp + 0x30 + VAR_68_OFFSET]          ; eax = [rsp + 0x44]

    ; [rbp + 0x10] = esi
    mov     dword [rbp + 0x10], esi                          ; [rbp + 0x10] = esi

    ; [rbp + 0x2C] = eax
    mov     dword [rbp + 0x2C], eax                          ; [rbp + 0x2C] = eax

    ; rax = [rsp + 0x30 + SOME_STACK_VAL_OFFSET]
    mov     rax, qword [rsp + 0x30 + SOME_STACK_VAL_OFFSET] ; rax = [rsp + 0x48]

    ; [rbp + 0x30] = ecx
    mov     dword [rbp + 0x30], ecx                          ; [rbp + 0x30] = ecx

    ; [rbp + 0x20] = r9d
    mov     dword [rbp + 0x20], r9d                          ; [rbp + 0x20] = r9d

    ; [rbp + 0x04] = r10d
    mov     dword [rbp + 0x04], r10d                         ; [rbp + 0x04] = r10d

    ; [rbp + 0x14] = r11d
    mov     dword [rbp + 0x14], r11d                         ; [rbp + 0x14] = r11d

    ; [rbp + 0x24] = r8d
    mov     dword [rbp + 0x24], r8d                          ; [rbp + 0x24] = r8d

    ; [rbp + 0x08] = ebx
    mov     dword [rbp + 0x08], ebx                          ; [rbp + 0x08] = ebx

    ; [rbp + 0x28] = r12d
    mov     dword [rbp + 0x28], r12d                         ; [rbp + 0x28] = r12d

    ; [rbp + 0x0C] = edi
    mov     dword [rbp + 0x0C], edi                          ; [rbp + 0x0C] = edi

    ; [rbp + 0x1C] = r15d
    mov     dword [rbp + 0x1C], r15d                         ; [rbp + 0x1C] = r15d

    ; [rbp + 0x3C] = r14d
    mov     dword [rbp + 0x3C], r14d                         ; [rbp + 0x3C] = r14d

    ; [rsp + 0x30 + COUNTER_EQ_10_OFFSET] = 1
    mov     dword [rsp + 0x30 + COUNTER_EQ_10_OFFSET], 1     ; [rsp + 0x30 + 0x00] = 1

    ; Decrement [rsp + 0x30 + COUNTER_EQ_10_OFFSET] by 1
    sub     dword [rsp + 0x30 + COUNTER_EQ_10_OFFSET], 1     ; [rsp + 0x30 + 0x00] -= 1

    ; Function Epilogue (Example: Exit syscall)
    mov     rax, 60         ; syscall: exit
    xor     rdi, rdi        ; exit code 0
    syscall

    ; Function Epilogue
    mov     rax, 60         ; syscall: exit
    xor     rdi, rdi        ; exit code 0
    syscall


    ; Function Epilogue
    mov     rax, 60         ; syscall: exit
    xor     rdi, rdi        ; exit code 0
    syscall
section .data
    data_bytes: 
        times 0x3f db 0x41 
        times 0x40 db 0x42


