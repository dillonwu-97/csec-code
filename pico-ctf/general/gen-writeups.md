---
title: general
tags: general
---

### 2Warm
picoCTF{101010}

### Warmed Up
picoCTF{61}

### Lets Warm Up
picoCTF{p}

### strings it
strings strings | grep pico to get picoCTF{5tRIng5\_1T\_d66c7bb7}

### bases 
echo bDNhcm5fdGgzX3IwcDM1 | base64 -d to get l3arn\_th3\_r0p35.

### first grep
cat file | grep pico to get picoCTF{grep\_is\_good\_to\_find\_things\_f77e0797}

### what's a net cat?
nc jupiter.challenges.picoctf.org 25103 to get picoCTF{nEtCat\_Mast3ry\_d0c64587}

### plumbing
nc jupiter.challenges.picoctf.org 14291 | grep pico to get picoCTF{digital\_plumb3r\_ea8bfec7}

### Based
The first is binary, second is octal, third is hex. The flag is picoCTF{learning\_about\_converting\_values\_02167de8}.

### flag\_shop
The solution to this problem is to trigger and overflow of the int. The max value of an int is 2147483647, but we could 
enter a number large enough such that 900 * the large number > 2147483647. I used the number 2147480000, and the flag is picoCTF{m0n3y\_bag5\_68d16363}.  

