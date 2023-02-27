---
title: you-know-0xdiablos
description: buffer overflow
tags: binary, buffer overflow, you know 0xdiablos
---
The two important functions for the overflow exercise are vuln() and flag(). They can be found here: 
<a href="https://github.com/dillonwu-97/csec-code/tree/main/hackthebox/challenges/binary/diablos"> https://github.com/dillonwu-97/csec-code/tree/main/hackthebox/challenges/binary/diablos </a> <br/>

You can find the functions using info functions in gdb. I saw that the size of the buffer was 180 bytes. I also found the location of the flag using the gdb command print &flag. In order to overwrite the return pointer so that we returned into the flag function, we have to fill the buffer with 180 (buffer) + 4 (ebx) + 4(ebp) of garbage values. 

After returning into the flag function, I saw that there was a comparison done for the values deadbeef and c0ded00d at locations ebp+8 and ebp+c respectively. I saw that the base pointer of the flag function was the return address of the vuln function. Since I needed to store the hex value deadbeef at 8 + ebp and c0ded00d at c + ebp, I added 4 bytes of garbage followed by the hex values for deadbeef and c0ded00d (all in little endian) to the payload. 

The code used to generate the payload can be found here: <a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/diablos/exp.py"> https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/diablos/exp.py </a> <br/>

It's important to note that in the flag function, there is some assembly starting from the command "jne 0x8049232 \<flag+80\>". This assembly is just used to check if there is a flag.txt file that the program can open. If it can find said file, it will continue with the program. Otherwise, it just exits. 

In order to send the payload, I did cat payload.hex | nc ip port. 

<img src = "/csec-writeups/hackthebox/htb-binary/diablos.png" />

The flag is HTB{0ur\_Buff3r\_1s\_not\_healthy}