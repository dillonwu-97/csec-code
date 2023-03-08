---
title: tear or dear
description: This is one of the reversing challenges on HacktheBox that involved the use of dnspy.
tags: reversing, dnspy
---

I used dnspy in order to walk through the C# code. First, I found the password value, which was "roiw!@#". I got the value by setting a breakpoint at the button1_Click function which does a check to see if the this.o value matches the this.username value (note: this.username is not the username input, it's the password input). Afterwards, I set another breakpoint at the last line of the check function, and saw that the this.textBox_user input is the same as the this.aa value, which was "piph".

<img src = "/csec-writeups/hackthebox/htb-reversing/tear-or-dear-1.png" />

<img src = "/csec-writeups/hackthebox/htb-reversing/tear-or-dear-2.png" />


Flag: HTB{piph:roiw!@#}