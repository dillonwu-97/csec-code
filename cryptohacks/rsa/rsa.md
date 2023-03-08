---
title: rsa
description: cryptohack rsa ctfs
tags: rsa, crypto
---

tags: rsa, weiner, wiener, quadratic equation, quadratic, 
### <ins> Starter </ins>
The starter code can be found here: <a href="https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/starter.py"> https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/starter.py </a>

### <ins> RSA Primes 1 </ins>
The code can be found here: <a href="https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/primes-part-1.py"> https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/primes-part-1.py </a>

The attacks are pretty standard. 

### <ins> Public Exponents </ins>
Code: <a href="https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/public-exponent.py"> https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/public-exponent.py </a>

1. Salty can be solved by just decrypting ciphertext without any math since the public exponent is 1. The flag is crypto{saltstack_fell_for_this!}.

2. For modulus inutilis, the public exponent is normal but the plaintext is too small, so there is no modulo operation being done. As a result, you can just take the eth root of the ciphertext to recover the plaintext.
The flag is crypto{N33d_m04R_p4dd1ng}. 

3. Since e is really big, that means d cannot be massive, so we can use Weiner's Attack to decrypt the ciphertext.  The flag is crypto{s0m3th1ng5_c4n_b3_t00_b1g}.

4. This link is useful for crossed wires. It involves calculating p and q using e, d, and N. I also observed that each of the N's for the friends' public keys and my private key were the same, so calculating phi(n) for my private key meant that I could use it to break all of the private keys. 
<a href="https://stackoverflow.com/questions/2921406/calculate-primes-p-and-q-from-private-exponent-d-public-exponent-e-and-the"> https://stackoverflow.com/questions/2921406/calculate-primes-p-and-q-from-private-exponent-d-public-exponent-e-and-the </a>
The flag is crypto{3ncrypt_y0ur_s3cr3t_w1th_y0ur_fr1end5_publ1c_k3y}. 

5. This talks about attacking RSA via the LLL method (specifically Boneh Durfee's attack on low private key exponents. This provides a great explanation of the attack itself as well as the code behind it: <a href="https://www.cryptologie.net/article/265/small-rsa-private-key-problem/"> https://www.cryptologie.net/article/265/small-rsa-private-key-problem/ </a>
This link is useful for installing sage on Mac: <a href="https://ask.sagemath.org/question/49572/sage-90-installation-issues-on-macos-10152-catalina/"> https://ask.sagemath.org/question/49572/sage-90-installation-issues-on-macos-10152-catalina/ </a>
The github tool I used to solve this problem can be found here: <a href="https://github.com/Ganapati/RsaCtfTool"> https://github.com/Ganapati/RsaCtfTool </a> 
The flag is crypto{bon3h5_4tt4ck_i5_sr0ng3r_th4n_w13n3r5}. A quick db lookup can also be used to solve this problem. 

6. Endless emails uses the Chinese Remainder Theorem. It is important to note that not all the messages are the same, so you can use only some of them for the algorithm. The flag is crypto{1f_y0u_d0nt_p4d_y0u_4r3_Vuln3rabl3}. 

Note: I need to review the mathematics behind Weiner's attack and LLL reductions. The method used in the Everything is Still Big challenge was a database lookup, and not the intended attack.

### <ins> RSA Primes 2 </ins>
Code: <a href="https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/primes-part-2.py"> https://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/primes-part-2.pyhttps://github.com/dillonwu-97/csec-code/blob/main/cryptohacks/rsa/primes-part-2.py </a>

1. The first problem is solved using Fermat's Factorization method. The flag is crypto{f3rm47_w45_4_g3n1u5}. 

2. The second problem contains p and q, which are of the form 2^n -1. These are known as Mersenne primes. The general idea for this was to count the number of digits in n, and then I found the two Mersenne primes whose digits summed roughly equal to the number of digits of n. The flag is crypto{Th3se_Pr1m3s_4r3_t00_r4r3}. 

3. To solve the third problem, we use an attack that exploits the implementation of "Fast Prime."
<a href="https://crypto.stackexchange.com/questions/52292/what-is-fast-prime"> https://crypto.stackexchange.com/questions/52292/what-is-fast-prime </a>
<a href="https://crypto.stackexchange.com/questions/53906/how-does-the-roca-attack-work"> https://crypto.stackexchange.com/questions/53906/how-does-the-roca-attack-work </a> 


Good explanation of pkcs1 implementation and attack: https://www.youtube.com/watch?v=y9n5FQlKA6g