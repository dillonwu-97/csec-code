---
title: caulingo
layout: post
dir: /csec-writeups
---

<h2> Methodology </h2>

<img src = "{{ page.dir }}/assets/google-ctf/caulingo.png" alt="">

* find the p,q, and d value for the encryption by brute forcing the possibilites
* use extended gcd algorithm to calculate d
* took the msg to d power, modulo n to calculate unencrypted values 
* code can be found here: https://github.com/dillonwu-97/csec-code/blob/master/google_ctf/beginner_2019/caulingo/solve.py

* flag: CTF{017d72f0b513e89830bccf5a36306ad944085a47}
