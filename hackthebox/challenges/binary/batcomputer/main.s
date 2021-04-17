   0x5555555551ec:      push   rbp
   0x5555555551ed:      mov    rbp,rsp
   0x5555555551f0:      sub    rsp,0x60
   0x5555555551f4:      mov    eax,0x0
   0x5555555551f9:      call   0x5555555551a9
   0x5555555551fe:      lea    rax,[rbp-0x60]
   0x555555555202:      add    rax,0x4
   0x555555555206:      mov    edx,0x10
   0x55555555520b:      mov    esi,0x0
   0x555555555210:      mov    rdi,rax
   0x555555555213:      call   0x555555555050 <memset@plt>
   0x555555555218:      lea    rdi,[rip+0xde9]        # 0x555555556008
   0x55555555521f:      mov    eax,0x0
   0x555555555224:      call   0x555555555040 <printf@plt>
   0x555555555229:      lea    rax,[rbp-0x60]
   0x55555555522d:      mov    rsi,rax
   0x555555555230:      lea    rdi,[rip+0xe32]        # 0x555555556069
   0x555555555237:      mov    eax,0x0
   0x55555555523c:      call   0x555555555090 <__isoc99_scanf@plt>
   0x555555555241:      mov    eax,DWORD PTR [rbp-0x60]
   0x555555555244:      cmp    eax,0x1
   0x555555555247:      jne    0x555555555267
   0x555555555249:      lea    rax,[rbp-0x60]
   0x55555555524d:      add    rax,0x14
   0x555555555251:      mov    rsi,rax
   0x555555555254:      lea    rdi,[rip+0xe15]        # 0x555555556070
   0x55555555525b:      mov    eax,0x0
   0x555555555260:      call   0x555555555040 <printf@plt>
   0x555555555265:      jmp    0x5555555551fe
   0x555555555267:      mov    eax,DWORD PTR [rbp-0x60]
   0x55555555526a:      cmp    eax,0x2
   0x55555555526d:      jne    0x55555555530d
   0x555555555273:      lea    rdi,[rip+0xe2e]        # 0x5555555560a8
   0x55555555527a:      mov    eax,0x0
   0x55555555527f:      call   0x555555555040 <printf@plt>
   0x555555555284:      lea    rax,[rbp-0x60]
   0x555555555288:      add    rax,0x4
   0x55555555528c:      mov    rsi,rax
   0x55555555528f:      lea    rdi,[rip+0xe3a]        # 0x5555555560d0
   0x555555555296:      mov    eax,0x0
   0x55555555529b:      call   0x555555555090 <__isoc99_scanf@plt>
   0x5555555552a0:      lea    rax,[rbp-0x60]
   0x5555555552a4:      add    rax,0x4
   0x5555555552a8:      lea    rsi,[rip+0xe26]        # 0x5555555560d5
   0x5555555552af:      mov    rdi,rax
   0x5555555552b2:      call   0x555555555070 <strcmp@plt>
   0x5555555552b7:      test   eax,eax
   0x5555555552b9:      je     0x5555555552d1
   0x5555555552bb:      lea    rdi,[rip+0xe26]        # 0x5555555560e8
   0x5555555552c2:      call   0x555555555030 <puts@plt>
   0x5555555552c7:      mov    edi,0x0
   0x5555555552cc:      call   0x5555555550a0 <exit@plt>
   0x5555555552d1:      lea    rdi,[rip+0xe58]        # 0x555555556130
   0x5555555552d8:      mov    eax,0x0
   0x5555555552dd:      call   0x555555555040 <printf@plt>
   0x5555555552e2:      lea    rax,[rbp-0x60]
   0x5555555552e6:      add    rax,0x14
   0x5555555552ea:      mov    edx,0x89
   0x5555555552ef:      mov    rsi,rax
   0x5555555552f2:      mov    edi,0x0
   0x5555555552f7:      call   0x555555555060 <read@plt>
   0x5555555552fc:      lea    rdi,[rip+0xe5e]        # 0x555555556161
   0x555555555303:      call   0x555555555030 <puts@plt>
   0x555555555308:      jmp    0x5555555551fe
   0x55555555530d:      lea    rdi,[rip+0xe5c]        # 0x555555556170
   0x555555555314:      call   0x555555555030 <puts@plt>
   0x555555555319:      mov    eax,0x0
   0x55555555531e:      leave  
   0x55555555531f:      ret 