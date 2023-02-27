---
title: impossible-password
description: This is the Impossible Password challenge on HacktheBox. 
tags: r2, ghidra
---

Using ltrace to trace the program allows you to find that the first password is SuperSeKretKey. Trying to find the second password is very difficult (impossible), hence the title of the challenge. 

The second part is generated through the srand(time(0)) function. This generates a random number based on the date and time. It then uses malloc() to create random pointer, and uses this as a seed for several rand() iterations in order to generate each subsequent character in the sequence. 

In order to solve this challenge, I used ghidra to reverse the binary. By reversing the binary, I was able to find the main function, and also found the get\_flag function. The get\_flag function takes an array of characters and uses the xor operation with the number 9 to generate the HTB flag. 

<img src = "/csec-writeups/hackthebox/htb-reversing/3.png" />

<br/>

<img src = "/csec-writeups/hackthebox/htb-reversing/2.png" />

In order to get the array of characters, I used r2. Specifically, in command line I typed:
r2 -A impossible-password.bin
pdf@main

<img src = "/csec-writeups/hackthebox/htb-reversing/1.png" />

Finally, I wrote a simple python script to xor each of the characters and got the flag. The code can be found here: <a href="https:github.com/dillonwu-97/csec-code/blob/master/hackthebox/challenges/reversing/impossible-password.py">https:github.com/dillonwu-97/csec-code/blob/master/hackthebox/challenges/reversing/impossible-password/solve.py</a>

Flag: HTB{40b949f92b86b18}

<h2> Extra: </h2>

I also learned about stripped binaries in this challenge. A great walkthrough is found here: <a href="https:medium.com/@tr0id/working-with-stripped-binaries-in-gdb-cacacd7d5a33">https:medium.com/@tr0id/working-with-stripped-binaries-in-gdb-cacacd7d5a33</a>. In the challenge, I tried using gdb to disassemble the main function, but it was not possible because the binary was stripped of any debug symbols.



