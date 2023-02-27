---
title: space
description: space
tags: binary, elf, shellcode, space
---

I thought this challenge was pretty difficult because it involved writing shellcode, and working very closely with individual instructions. The first part of this writeup contains what I thought were the steps to solving the challenge. However, there are several issues with the steps, and I will talk about each of them in Part 2: Corrections.

<h3> Part 1: Incorrect </h3>
1) I used gdb / gef to walk through the binary, and saw a couple of things.   
(a) checks and aslr commands revealed that no stack protections are on.
(b) There are two buffers. One is in the main function, one is in the vuln function. The buffer in the main function is 32 bytes, and the buffer in the vuln function is 20 bytes. However, you are restricted to 14 bytes only in the vuln buffer.

2) I crafted my payload my payload using the following reasoning:  
(a) I fill the vuln buffer with garbage data: 18 bytes of ‘A’  size of buffer (14) + ebp (4)
(b) I find the location of the main buffer, which I calculated to be 0xffffd4f0.
(c) I set the return address to 0xffffd4f0.
(d) I find the distance between the end of the vuln function and the start of the main buffer, which I calculated to be roughly 24 bytes. I found the distance by finding the difference between the location of the main buffer (0xffffd510), the size of the main buffer (0x20), and the address of the base pointer of the vuln function (0xffffd4d8). 
(e) I write my shellcode into the main buffer. The shellcode is roughly 23 bytes, and I got it from shellstorm. I also create a NOP sled immediately after the base pointer in the vuln function so that if I drop anywhere in memory, I can slide into my shell.
(f) I use cat payload.hex | ./space in gdb  
3) My intention in the exploit is to achieve code execution from the main buffer. However, when the vuln function returns, I do not return into the main buffer. I instead return into the hard address 0x90909090. I am not sure why this is the case.

The code below is what I used for the exploit in this portion. 

```python
import pwn
import pwnlib
from pwnlib.util.packing import *

# shellcode
# http://shell-storm.org/shellcode/files/shellcode-827.php
shellcode = b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'

stack_start = p32(0xffffd510 - 0x20) # = '0xffffd4f0'

# 0xffffd4d8 is base pointer of vuln function
diff = (0xffffd510 - 0x20 - 0xffffd4d8) # distance between vuln base pointer and stack_start location, which is roughly 24 bytes 

# because of    0x080491bb <+23>:    lea    edx,[ebp-0xe], you actually only have
# 14 bytes of space + 4 bytes for ebp
payload = b'A'* 18 + stack_start +  b'\x90' * diff + shellcode
with open ('payload.hex', 'wb') as f:
	f.write(payload)
```

<h3> Part 2: Corrections </h3>

There were several issues with my assumptions and approach to this problem.   

First, I did not understand how the main buffer and vuln buffer interacted with each other. When I disassembled the program using ghidra, I got a btter understanding of what was going on. When you are first asked to put input into the program, you inject the payload. It then calls the vuln() function, and does a string copy of the buffer into a new buffer in vuln that is 10 bytes long. However, 31 bytes are actually copied since the main buffer is of size 31 bytes. 

<img src = "/csec-writeups/hackthebox/htb-binary/space-1.png" />

<img src = "/csec-writeups/hackthebox/htb-binary/space-2.png" />

After understanding how the buffers interacted with each other, I looked more closely at the assembly instructions for each of the programs. The return address is 18 bytes away from the end of the vuln buffer because the structure is vuln buffer (10 bytes) + ebx(4 bytes) + ebp(4 bytes) + ret (4 bytes). Since there are 31 bytes total being copied, there are still 9 bytes left after the end of the return address. 

The general idea for the exploit is as follows: 
1) after string copy finishes, do not return the the main function. Instead, stay on the stack and execute the subsequent 9 bytes that come after the end of vuln.
2) Within these 9 bytes, find a way to jump back to the top of the vuln stack to continue code execution. 
3) The 9 byte section should contain the first part of the shellcode, followed by a jump instruction to the top of the vuln buffer, followed by the rest of the shellcode.

I found the jmp esp gadget user ropper, and I had the vuln function return to this function call. 
<img src = "/csec-writeups/hackthebox/htb-binary/space-3.png" />
In the 9 byte-payload, I had some assembly instructions important for starting a shell, as well as another instruction (sub esp, 0x16 + jmp esp) to move to the top of the vuln stack. The rest of the vuln stack is the shell code. 

The exploit, which includes my thought process for crafting the shell payload can be found here: 
<a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/space/exp.py">
https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/space/exp.py </a>

The annotated assembly code for the main function is found here:
<a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/space/main.s">
https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/space/main.s </a>

The annotated assembly code for the vuln function is found here:
<a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/space/vuln.s">
https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/space/vuln.s </a>


<img src = "/csec-writeups/hackthebox/htb-binary/space-4.png" />
The flag is HTB{sh3llc0de\_1n\_7h3\_5p4c3}.