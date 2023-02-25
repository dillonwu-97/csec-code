---
title: diffie-helman
description: crypto diffie-helman ctfs
tags: diffie helman, diffie, helman, crypto
---


### <ins> Starter </ins>
The starter code can be found here: <a href="https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/diffie-helman/dh-starter.py"> https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/diffie-helman/dh-starter.py </a>

### <ins> Man in the Middle </ins>
The code for the man-in-the-middle challenges can be found here:
<a href="https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/diffie-helman/man-in-the-middle.py"> https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/diffie-helman/man-in-the-middle.py </a>
1. Parameter Injection <br/>
The attack for this is relatively straightforward. You receive information about Alice's key, and you send back your own public key as opposed to the one you receive from Bob. Then, Alice sends the iv and flag that was encrypted using your public key (as opposed to Bob's).

The flag is crypto{n1c3\_0n3\_m4ll0ry!!!!!!!!}. 

2. Export-grade <br/>
I used DH64 as one of the encryption parameters. DH64 means DH encryption is using a 64 bit key, which is insecure because you can easily use brute force to solve the discrete logarithm problem. I used this website to find the exponent: <a link="https://www.alpertron.com.ar/DILOG.HTM"> https://www.alpertron.com.ar/DILOG.HTM </a>

The flag is crypto{d0wn6r4d35\_4r3\_d4n63r0u5}




