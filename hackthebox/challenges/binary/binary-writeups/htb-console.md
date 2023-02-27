---
title: htb-console
description: use system call
tags: binary
---
For this box, I triggered an overflow and returned to a system call. 

Note: If in gdb, you come across ^M when pressing enter, there is an issue with the terminal display / input which can be solved with the command stty sane. 

First, I found the number of bytes needed to trigger a seg fault in gdb using the following steps:
1. pattern create 50
2. Input the pattern into run, followed by the flag option. 
3. pattern search
This reveals that the offset is at 24.  

To find the location of the system command use objdump -D htbconsole. This link is useful for finding out what each column means: <a href="https://stackoverflow.com/questions/6666805/what-does-each-column-of-objdumps-symbol-table-mean"> https://stackoverflow.com/questions/6666805/what-does-each-column-of-objdumps-symbol-table-mean </a> It is also possible to find the location in gdb by using the command info functions.

I triggered the overflow and returned into the system function. System call takes the address of a string in the register rdi and runs the string so I had to find a rop gadget for 'pop rdi; ret'. I found the rop gadget using the command:  
ropper --file htbconsole  

To use a custom string, I saw in the code that the program allowed me to input my own string to a location in memory. I input "/bin/sh" and then popped that address into rdi. The code for the exploit can be found here: <a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/htbconsole/exp.py"> https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/binary/htbconsole/exp.py </a>. 



Note: This might be useful in the future for finding strings: <a href="https://stackoverflow.com/questions/6637448/how-to-find-the-address-of-a-string-in-memory-using-gdb"> https://stackoverflow.com/questions/6637448/how-to-find-the-address-of-a-string-in-memory-using-gdb </a>