Dump of assembler code for function flag:
   0x080491e2 <+0>:     push   ebp
   0x080491e3 <+1>:     mov    ebp,esp
   0x080491e5 <+3>:     push   ebx
   0x080491e6 <+4>:     sub    esp,0x54
   0x080491e9 <+7>:     call   0x8049120 <__x86.get_pc_thunk.bx>
   0x080491ee <+12>:    add    ebx,0x2e12
   0x080491f4 <+18>:    sub    esp,0x8
   0x080491f7 <+21>:    lea    eax,[ebx-0x1ff8]
   0x080491fd <+27>:    push   eax
   0x080491fe <+28>:    lea    eax,[ebx-0x1ff6]
   0x08049204 <+34>:    push   eax
   0x08049205 <+35>:    call   0x80490b0 <fopen@plt>
   0x0804920a <+40>:    add    esp,0x10
   0x0804920d <+43>:    mov    DWORD PTR [ebp-0xc],eax
   0x08049210 <+46>:    cmp    DWORD PTR [ebp-0xc],0x0
   0x08049214 <+50>:    jne    0x8049232 <flag+80>
   0x08049216 <+52>:    sub    esp,0xc
   0x08049219 <+55>:    lea    eax,[ebx-0x1fec]
   0x0804921f <+61>:    push   eax
   0x08049220 <+62>:    call   0x8049070 <puts@plt>
   0x08049225 <+67>:    add    esp,0x10
   0x08049228 <+70>:    sub    esp,0xc
   0x0804922b <+73>:    push   0x0
   0x0804922d <+75>:    call   0x8049080 <exit@plt>
   0x08049232 <+80>:    sub    esp,0x4
   0x08049235 <+83>:    push   DWORD PTR [ebp-0xc]
   0x08049238 <+86>:    push   0x40
   0x0804923a <+88>:    lea    eax,[ebp-0x4c]
   0x0804923d <+91>:    push   eax
   0x0804923e <+92>:    call   0x8049050 <fgets@plt>
   0x08049243 <+97>:    add    esp,0x10
   0x08049246 <+100>:   cmp    DWORD PTR [ebp+0x8],0xdeadbeef
   0x0804924d <+107>:   jne    0x8049269 <flag+135>
   0x0804924f <+109>:   cmp    DWORD PTR [ebp+0xc],0xc0ded00d
   0x08049256 <+116>:   jne    0x804926c <flag+138>
   0x08049258 <+118>:   sub    esp,0xc
   0x0804925b <+121>:   lea    eax,[ebp-0x4c]
   0x0804925e <+124>:   push   eax
   0x0804925f <+125>:   call   0x8049030 <printf@plt>
   0x08049264 <+130>:   add    esp,0x10
   0x08049267 <+133>:   jmp    0x804926d <flag+139>
   0x08049269 <+135>:   nop
   0x0804926a <+136>:   jmp    0x804926d <flag+139>
   0x0804926c <+138>:   nop
   0x0804926d <+139>:   mov    ebx,DWORD PTR [ebp-0x4]
   0x08049270 <+142>:   leave  
   0x08049271 <+143>:   ret 