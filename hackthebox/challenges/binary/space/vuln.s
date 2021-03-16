Dump of assembler code for function vuln:
   0x080491a4 <+0>:     push   ebp # ebp points to start of MAIN stack
   0x080491a5 <+1>:     mov    ebp,esp # ebp now points to start of vuln
   0x080491a7 <+3>:     push   ebx
   0x080491a8 <+4>:     sub    esp,0x14
   0x080491ab <+7>:     call   0x8049243 <__x86.get_pc_thunk.ax>
   0x080491b0 <+12>:    add    eax,0x2114
   0x080491b5 <+17>:    sub    esp,0x8
   0x080491b8 <+20>:    push   DWORD PTR [ebp+0x8] # pushing eax; since that is currently at ebp + 8; it also contains the location of the main buffer
   0x080491bb <+23>:    lea    edx,[ebp-0xe] # 0xe = 14, -4 bytes(ebx) = 10; so do a strcpy into 10 bytes
   0x080491be <+26>:    push   edx
   0x080491bf <+27>:    mov    ebx,eax
   0x080491c1 <+29>:    call   0x8049060 <strcpy@plt>
   0x080491c6 <+34>:    add    esp,0x10
   0x080491c9 <+37>:    nop
   0x080491ca <+38>:    mov    ebx,DWORD PTR [ebp-0x4]
   0x080491cd <+41>:    leave  # leave ret means void function; also leave moves the base pointer into the stack pointer and then pops ebp.
   0x080491ce <+42>:    ret    
End of assembler dump.
