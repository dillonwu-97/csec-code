Dump of assembler code for function main:                                                                                                                                                     
   0x080491cf <+0>:     lea    ecx,[esp+0x4]                                                                                                                                                  
   0x080491d3 <+4>:     and    esp,0xfffffff0                                                                                                                                                 
   0x080491d6 <+7>:     push   DWORD PTR [ecx-0x4]                                                                                                                                            
   0x080491d9 <+10>:    push   ebp
   0x080491da <+11>:    mov    ebp,esp
   0x080491dc <+13>:    push   ebx
   0x080491dd <+14>:    push   ecx
   0x080491de <+15>:    sub    esp,0x20 # allocate 32 bytes
   0x080491e1 <+18>:    call   0x80490d0 <__x86.get_pc_thunk.bx>
   0x080491e6 <+23>:    add    ebx,0x20de
   0x080491ec <+29>:    sub    esp,0xc
   0x080491ef <+32>:    lea    eax,[ebx-0x12bc]
   0x080491f5 <+38>:    push   eax
   0x080491f6 <+39>:    call   0x8049040 <printf@plt>
   0x080491fb <+44>:    add    esp,0x10
   0x080491fe <+47>:    mov    eax,DWORD PTR [ebx-0x4]
   0x08049204 <+53>:    mov    eax,DWORD PTR [eax]
   0x08049206 <+55>:    sub    esp,0xc
   0x08049209 <+58>:    push   eax
   0x0804920a <+59>:    call   0x8049050 <fflush@plt>
   0x0804920f <+64>:    add    esp,0x10
   0x08049212 <+67>:    sub    esp,0x4
   0x08049215 <+70>:    push   0x1f
   0x08049217 <+72>:    lea    eax,[ebp-0x27] # <-- take the first 39 bytes (which is basically the allocated buffer above minus ecx and ebx)
   0x0804921a <+75>:    push   eax
   0x0804921b <+76>:    push   0x0
   0x0804921d <+78>:    call   0x8049030 <read@plt>
   0x08049222 <+83>:    add    esp,0x10
   0x08049225 <+86>:    sub    esp,0xc
   0x08049228 <+89>:    lea    eax,[ebp-0x27] # load effective address to be used as arg for vuln
   0x0804922b <+92>:    push   eax 
   0x0804922c <+93>:    call   0x80491a4 <vuln>
   0x08049231 <+98>:    add    esp,0x10
   0x08049234 <+101>:   mov    eax,0x0
   0x08049239 <+106>:   lea    esp,[ebp-0x8]
   0x0804923c <+109>:   pop    ecx
   0x0804923d <+110>:   pop    ebx
   0x0804923e <+111>:   pop    ebp
   0x0804923f <+112>:   lea    esp,[ecx-0x4]
   0x08049242 <+115>:   ret    
End of assembler dump.
