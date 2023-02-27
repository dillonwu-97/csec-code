---
title: restaurant
description: restaurant
tags: aslr, return to libc, binary
---
WORK IN PROGRESS

Useful links:

https://sploitfun.wordpress.com/2015/05/08/bypassing-aslr-part-i/

https://book.hacktricks.xyz/exploiting/linux-exploiting-basic-esp/rop-leaking-libc-address


basically there's an overflow in the fill menu option. you pick that, then you can input more data and cause an overflow and ROP. use that to put the puts GOT address into rdi, then the address to puts in PLT to call it, then the address to main. that will print the GOT address giving you an ASLR leak and then restarting the whole thing by jumping back to main. use that leaked address to find the offset from puts to whatever you want in the bundled libc, then do the whole overflow again to ROP together whatever you want to start a shell and you should be good. only reason i haven't put out a writeup yet is that i can't write a working exploit because that bundled libc immediately crashes for me, so i can only make it work with my systems libc lol
