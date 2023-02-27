---
title: bypass
description: This is one of the reversing challenges on HacktheBox that involved the use of dnspy.
tags: reversing, dnspy, x64dbg
---

Cating file reveals that it is a 32 bit binary. I used to method detailed here: <a href="https://superuser.com/questions/358434/how-to-check-if-a-binary-is-32-or-64-bit-on-windows
"> https://superuser.com/questions/358434/how-to-check-if-a-binary-is-32-or-64-bit-on-windows </a>

I tried debugging using x64dbg but it didn't work. A very helpful guide for future reference can be found here though: <a href="http://reverseengineeringtips.blogspot.com/2015/01/an-introduction-to-x64dbg.html"> http://reverseengineeringtips.blogspot.com/2015/01/an-introduction-to-x64dbg.html </a>

I used dnSpy instead in order to reverse the binary which is a .NET program. 
I first reviewed the code in the {} folder, and saw the function 0 in class 0. I saw that function 0 called 
function 1 which took in two user inputs. However, regardless of the input, false is returned. At first, I tried to exploit the program by recompiling line 29 so that true would always be returned instead of false. This could be normally be done by right clicking the line, and then selecting "Edit Method". Unfortunately, there are a number of errors generated when I tried doing this method. 

I opted to edit specific values in the Locals tab by utilizing breakpoints instead. I created breakpoints in lines 10, 38/39, and 20. The breakpoint in line 10 was used to change the value of flag from false to true.
<img src = "/csec-writeups/hackthebox/htb-reversing/bypass-1.png" />


The breakpoint in line 38/39 could be used to examine the secret key, but I opted to change the flag instead. 
<img src = "/csec-writeups/hackthebox/htb-reversing/bypass-2.png" />

Finally, the breakpoint in line 20 was so that the program would not instantly close before showing me the flag, which turned out to be HTB{SuP3rC00lFL4g}. 
<img src = "/csec-writeups/hackthebox/htb-reversing/bypass-3.png" />
