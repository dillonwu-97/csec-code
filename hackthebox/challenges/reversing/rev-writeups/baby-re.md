---
title: baby-re
description: This is one of the reversing challenges on HacktheBox. It is quite easy.
tags: ltrace, reversing
---

The exploit method for this challenge is very easy.
You can use ltrace to find the password or you can use gdb to find the password. I stepped through the program in gdb and saw that abcde122313 was the password.

The flag is: HTB{B4BY\_R3V\_TH4TS\_EZ}


