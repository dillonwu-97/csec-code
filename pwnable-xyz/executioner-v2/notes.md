lokihardt does this instead?
0:  00 ff                   add    bh,bh
2:  59                      pop    rcx 
3:  48 81 e9 ca 02 00 00    sub    rcx,0x2ca
a:  ff e1                   jmp    rcx

TODO: figure out if this works or not and why / why not
okay, get the return address which is on the stack, pop into rcx subtract to win and jump to win very interesting

figure out the pow situation first 
