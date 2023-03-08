---
title: weak-rsa
description: Weiner hehe
tags: rsa, crypto, wiener, wiener attack
---

I decoded the RSA public key to find the modulo and exponent value. I saw that the public exponent was very large, and thought it might be susceptible to the Wiener attack. Good explanations of the attack can be found here:  
<a href="https://sagi.io/2016/04/crypto-classics-wieners-rsa-attack/"> https://sagi.io/2016/04/crypto-classics-wieners-rsa-attack/ </a>  
<a href="https://www.youtube.com/watch?v=OpPrrndyYNU"> https://www.youtube.com/watch?v=OpPrrndyYNU </a>  

I used the library package found here: <a href="https://github.com/orisano/owiener"> https://github.com/orisano/owiener </a>

```python
import owiener
m = '3303b790fb149da3406d495ab9b9fb8a9e293445e3bd43b18ef2f0521b726ebe8d838ba774bb5240f08f7fbca0a142a1d4a61ea973294e684a8d1a2cdf18a84f2db7099b8e977588b0b891292558caa05cf5df2bc6334c5ee5083a234edfc79a95c478a78e337c723ae8834fb8a9931b74503ffea9e61bf53d8716984ac47837b'
e = '6117c60448b139451ab5b60b6257a12bda90c0960fad1e007d16d8fa43aa5aaa3850fc240e5414ad2ba1090e8e12d6495bbc73a0cba562504255c73ea3fbd36a8883f831da8d1b9b8133ac2109e20628e80c7e53baba4ce5a14298811e70b4a2313c914a2a3217c02e951aaee4c9eb39a3f080357b533a6cca9517cb2b95bfcd'

m = int(m, 16)
e = int(e, 16)

with open('flag.enc', 'rb') as f:
	file = f.read()

flag_enc = [str(hex(i)[2:].zfill(2)) for i in file]
flag = int(''.join(flag_enc), 16)

d = owiener.attack(e, m)
plaintext = pow(flag, d, m)
plaintext = '0' + hex(plaintext)[2:]
print('---plaintext---')
plaintext = bytes.fromhex(str(plaintext))
print(plaintext)
```

The flag is HTB{s1mpl3_Wi3n3rs_4tt4ck}.