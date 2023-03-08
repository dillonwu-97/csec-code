---
title: rookie-mistake
description: rookie mistake; uses rsa and diffie helman
tags: crypto, rsa, diffie helman, tonelli-shanks, crt, chinese remainder theorem
---
I used these two resources to learn more about RSA in general:
<a href= "https://math.stackexchange.com/questions/1123180/understanding-why-the-public-exponent-e-is-chosen-the-way-it-is-in-rsa"> https://math.stackexchange.com/questions/1123180/understanding-why-the-public-exponent-e-is-chosen-the-way-it-is-in-rsa </a>

<a href ="https://math.stackexchange.com/questions/1221723/why-in-rsa-the-public-exponent-e-must-be-coprime-with-phi-n?rq=1"> https://math.stackexchange.com/questions/1221723/why-in-rsa-the-public-exponent-e-must-be-coprime-with-phi-n?rq=1 </a>

I really enjoyed this puzzle. 
For the first part of the puzzle, examining the code will reveal two important facts:
1. The modulo used is a prime number p, making phi(n) = p-1. 
2. The exponent is e, but e is an even integer. This means that e = i^(j * 32) for some integer j. The number 32 is the number of times the exponent can be divided by 2. 

This link is useful for better understanding how inversion in RSA works. 
<a href="https://crypto.stackexchange.com/questions/47375/discrete-logarithm-with-unknown-base"> https://crypto.stackexchange.com/questions/47375/discrete-logarithm-with-unknown-base </a>

Thus, to find the plaintext, we can calculate d by taking the inverse of integer j, i.e. do gmpy2.invert(j, phi). Aftewards, we can use tonelli-shanks to calculate p by repeatedly finding the square root of the resultant quadratic residue.

The first part of the flag is HTB{why\_d1d\_y0u\_m3ss\_3v3ryth1ng\_up\_1ts\_n0t\_th4t\_h4rd

The second part involves understanding DH key exchange. The link below explains why we should not use a nonprime as the modulus in the algorithm:
<a href="https://crypto.stackexchange.com/questions/30328/why-does-the-modulus-of-diffie-hellman-need-to-be-a-prime
"> https://crypto.stackexchange.com/questions/30328/why-does-the-modulus-of-diffie-hellman-need-to-be-a-prime </a>

Because the number is a product of primes, we apply the Chinese Remainder Theorem in order to get the second part of the flag. The second part of the flag is \_ju5t\_us3\_pr0p3r\_p4r4m3t3rs\_f0r\_4ny\_crypt0syst3m...}.

The full flag: HTB{why\_d1d\_y0u\_m3ss\_3v3ryth1ng\_up\_1ts\_n0t\_th4t\_h4rd\_ju5t\_us3\_pr0p3r\_p4r4m3t3rs\_f0r\_4ny\_crypt0syst3m...}

The code for the exploit can be found here: 
<a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/crypto/rookie-mistake/rookie-mistake.py"> https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/crypto/rookie-mistake/rookie-mistake.py </a>
The vulnerable / key generation code is found here: <a a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/crypto/rookie-mistake/gen.py"> https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/crypto/rookie-mistake/gen.py </a>

