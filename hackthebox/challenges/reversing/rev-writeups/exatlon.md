---
title: exatlon
description: This is one of the reversing challenges on HacktheBox. The binary is packed using UPX so you have to make sure to unpack it before trying to find the flag.
tags: upx, r2, gdb, reversing
---

The exploit for this was interesting. 
First, you have to unpack the binary using UPX. Packing is a way of obfuscating the binary so as to prevent reverse engineering. For example, if we don't unpack the unzipped binary file with upx -d exatlon\_v1, we can't use gdb to disass main. 

After unpacking the binary, I use r2 to look at the main function: r2 -A exatlon\_v1. I see that there is a chunk of string values right before hitting the instruction pointer that prints out "Looks Good." 

<img src = "/csec-writeups/hackthebox/htb-reversing/exatlon1.png" />

I set up a breakpoint at that instruction with the input "abcd." I observe that "abcd" results in "1552 1568 1584 1600 " and that 1552 / 97 = 16. 97 is the numerical equivalent of "a" in ascii. This means that to decode the pack of numbers, I just have to divide each number by 16 and convert to the ascii character. The numbers when decoded give me the flag. 

Code can be found here: <a href="https:github.com/dillonwu-97/csec-code/blob/master/hackthebox/challenges/reversing/exatlon.py">https:github.com/dillonwu-97/csec-code/blob/master/hackthebox/challenges/reversing/exatlon/solve.py</a>

The flag is: HTB{l3g1c3l\_sh1ft\_l3ft\_1nsr3ct1on!!}

