---
title: stopgan
layout: post
---

<h2> Methodology </h2>
* easy method is just overflowing with a lot of characters
* copy paste perl -e 'printf "A"x265' 
* flag: CTF{Why\_does\_cauliflower\_threaten\_us}
* harder method involves using ghidra to decompile the bof code
* saw from the main function that the buffer is of size 260, +4 for ebp
* return into a function called local\_flag which was at address 0x00400840
* actually had to return to 0x0040084c
* flag2: CTF{controlled\_crash\_causes\_conditional\_correspondence}
