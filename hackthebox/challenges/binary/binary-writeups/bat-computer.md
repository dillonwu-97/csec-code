---
title: bat-computer
description: im batman
tags: binary
---
# BatComputer
For this challenge, I looked at the code for the main function using ghidra. I also was able to find the breakpoints for the main function in gdb by breaking at one of the puts functions, and then subsequently looking at the instructions in that vicinity. Using ghidra, I was able to find the password for the bat computer, and also found that the leaked address told me the location of the buffer that I could overflow. I used pwntools to generate the shellcode, placed it into the buffer, and tried to return into it during execution. There were several challenges that I needed to overcome:

First, I had to find a way to return into the buffer. I realized that I could override the return of the main function by entering (3) instead of (1) or (2) when asked to choose an option. 

Second, I needed to find a way to execute the shellcode. When I just tried injecting the shellcode, it did not work. I disassembled the binary using IDA. I then placed a breakpoint at the return instruction in main. I walked through the shellcode that was supposed to execute and saw that some of the shellcode was being overwritten. This was most likely because the stack was not aligned, or because there wasn't enough space on the stack. To solve this issue, I used the popad instruction in pwntools which allowed me to successfully overcome this problem.

The code for the challenge can be found here: <a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/batcomputer/exp.py"> https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/batcomputer/exp.py </a>