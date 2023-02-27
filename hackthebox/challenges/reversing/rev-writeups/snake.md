---
title: snake
description: This challenge was interesting but it was pretty troll...
tags: python
---

For this reversing challenge, it is really important to read the code to understand what is going on. If you do the math, you will notice that the value for lock remains the same regardless of the lock\_pick value. Additionally, converting all the hex characters into a readable string reveals that the password array hex just says "this is a troll password!!!".

To find the actual usertitle and password, we first notice that the HTB flag is in the form HTB{usertitle:password}. The hex usertitle converted to ascii is "anaconda." The password examines the first character of the character in the chars array and the user input: this is a reference to the encrypted key which is udvvrjwa$$. 

The code for the solution can be found here:
<a href="https:github.com/dillonwu-97/csec-code/blob/master/hackthebox/challenges/reversing/snake.py">https:github.com/dillonwu-97/csec-code/blob/master/hackthebox/challenges/reversing/snake/solve.py</a>

The flag is: HTB{anaconda:udvvrjwa$$}


