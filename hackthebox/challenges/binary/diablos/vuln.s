Dump of assembler code for function vuln:
   0x08049272 <+0>:     push   ebp
   0x08049273 <+1>:     mov    ebp,esp
   0x08049275 <+3>:     push   ebx
   0x08049276 <+4>:     sub    esp,0xb4
   0x0804927c <+10>:    call   0x8049120 <__x86.get_pc_thunk.bx>
   0x08049281 <+15>:    add    ebx,0x2d7f
   0x08049287 <+21>:    sub    esp,0xc
   0x0804928a <+24>:    lea    eax,[ebp-0xb8]
   0x08049290 <+30>:    push   eax
   0x08049291 <+31>:    call   0x8049040 <gets@plt>
   0x08049296 <+36>:    add    esp,0x10
   0x08049299 <+39>:    sub    esp,0xc
   0x0804929c <+42>:    lea    eax,[ebp-0xb8]
   0x080492a2 <+48>:    push   eax
   0x080492a3 <+49>:    call   0x8049070 <puts@plt>
   0x080492a8 <+54>:    add    esp,0x10
   0x080492ab <+57>:    nop
   0x080492ac <+58>:    mov    ebx,DWORD PTR [ebp-0x4]
   0x080492af <+61>:    leave  
   0x080492b0 <+62>:    ret    
End of assembler dump.
