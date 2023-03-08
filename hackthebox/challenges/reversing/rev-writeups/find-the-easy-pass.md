---
title: find-the-easy-pass
description: Find the Easy Pass challenge. My first Windows reverse engineering exploit! 
tags: x32dbg, reversing
---

This reversing challenge was relatively straightforward. At first, I tried using x64dbg to reverse the binary but realized that I had to use x32dbg because the file was a 32 bit binary. 

<img src = "/csec-writeups/hackthebox/htb-reversing/easypass1.png" />

I stepped through the binary, and found the function that was called right before "Wrong Password" was printed. I saw that the function compared my input with the string "fortran!"

<img src = "/csec-writeups/hackthebox/htb-reversing/easypass2.png" />

Flag: HTB{fortran!} 
