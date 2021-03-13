Dump of assembler code for function main:
   0x00000000000011e9 <+0>:     endbr64 
   0x00000000000011ed <+4>:     push   rbp
   0x00000000000011ee <+5>:     mov    rbp,rsp
   0x00000000000011f1 <+8>:     sub    rsp,0x40
   0x00000000000011f5 <+12>:    mov    DWORD PTR [rbp-0x4],0xdeadc0d3
   0x00000000000011fc <+19>:    lea    rdi,[rip+0xe05]        # 0x2008
   0x0000000000001203 <+26>:    mov    eax,0x0
   0x0000000000001208 <+31>:    call   0x10a0 <printf@plt>
   0x000000000000120d <+36>:    lea    rax,[rbp-0x40]
   0x0000000000001211 <+40>:    mov    rdi,rax
   0x0000000000001214 <+43>:    mov    eax,0x0
   0x0000000000001219 <+48>:    call   0x10d0 <gets@plt>
   0x000000000000121e <+53>:    lea    rax,[rbp-0x40]
   0x0000000000001222 <+57>:    mov    rsi,rax
   0x0000000000001225 <+60>:    lea    rdi,[rip+0xe04]        # 0x2030
   0x000000000000122c <+67>:    mov    eax,0x0
   0x0000000000001231 <+72>:    call   0x10a0 <printf@plt>
   0x0000000000001236 <+77>:    cmp    DWORD PTR [rbp-0x4],0x1337bab3
   0x000000000000123d <+84>:    jne    0x12a8 <main+191>
   0x000000000000123f <+86>:    mov    edi,0x100
   0x0000000000001244 <+91>:    call   0x10e0 <malloc@plt>
   0x0000000000001249 <+96>:    mov    QWORD PTR [rbp-0x10],rax
   0x000000000000124d <+100>:   mov    esi,0x0
   0x0000000000001252 <+105>:   lea    rdi,[rip+0xdfc]        # 0x2055
   0x0000000000001259 <+112>:   mov    eax,0x0
   0x000000000000125e <+117>:   call   0x10f0 <open@plt>
   0x0000000000001263 <+122>:   mov    DWORD PTR [rbp-0x14],eax
   0x0000000000001266 <+125>:   mov    rcx,QWORD PTR [rbp-0x10]
   0x000000000000126a <+129>:   mov    eax,DWORD PTR [rbp-0x14]
   0x000000000000126d <+132>:   mov    edx,0x100
   0x0000000000001272 <+137>:   mov    rsi,rcx
   0x0000000000001275 <+140>:   mov    edi,eax
   0x0000000000001277 <+142>:   mov    eax,0x0
   0x000000000000127c <+147>:   call   0x10c0 <read@plt>
   0x0000000000001281 <+152>:   mov    rax,QWORD PTR [rbp-0x10]
   0x0000000000001285 <+156>:   mov    rsi,rax
   0x0000000000001288 <+159>:   lea    rdi,[rip+0xdd1]        # 0x2060
   0x000000000000128f <+166>:   mov    eax,0x0
   0x0000000000001294 <+171>:   call   0x10a0 <printf@plt>
   0x0000000000001299 <+176>:   mov    eax,DWORD PTR [rbp-0x14]
   0x000000000000129c <+179>:   mov    edi,eax
   0x000000000000129e <+181>:   mov    eax,0x0
   0x00000000000012a3 <+186>:   call   0x10b0 <close@plt>
   0x00000000000012a8 <+191>:   mov    eax,0x0
   0x00000000000012ad <+196>:   leave  
   0x00000000000012ae <+197>:   ret  