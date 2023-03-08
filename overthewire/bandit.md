---
title: bandit
description: Bandit from overthewire
layout: post
---
<h2> Bandit0: </h2>
ssh bandit0@bandit.labs.overthewire.org -p 2220  
password: bandit0 
password in readme: boJ9jbbUNNfktd78OOpsqOltutMc3MY1

<h2> Bandit1: </h2>
cat /home/bandit1/-
password: CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9

<h2> Bandit2: </h2>
cat "spaces in this filetitle"
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK

<h2> Bandit3: </h2>
* Idea is to find the hidden file
* cat ./inhere/.hidden
* pIwrPrtPN36QITSp3EQaw936yaFoFgA

<h2> Bandit4: </h2>
* Made a short script to iterate through the files
* for i in {1..9}; do echo test${i}; cat /home/bandit4/inhere/-file0${i}; done
* koReBOKuIDDepwhWk7jZC0RTdopnAYKh

<h2> Bandit5: </h2>
* Use built-in Linux search mechanisms
* find inhere -type f -size 1033c ! -executable -readable inhere/maybehere07/.file2
* DXjZPULLxYr17uwoI01bNLQbtFemEgo7

<h2> Bandit6: </h2>
* Similar idea as bandit5 plus a little extra work
* find ./ -group bandit6 -user bandit7 -size 33c 2>&1 \| grep -v 'Permission'
* HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs

<h2> Bandit7: </h2>
* find "millionth"
* cat data.txt \| grep -e "millionth"
* cvX2JJa4CFALtqS87jk27qwqGhBM9plV

<h2> Bandit8: </h2>
* sort data.txt \| uniq -u
* UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR

<h2> Bandit9: </h2>
* strings data.txt \| grep -e "=="
* truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk

<h2> Bandit10: </h2>
* base64 -d data.txt \| cat
* IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR

<h2> Bandit11: </h2>
* cat data.txt \| tr a-zA-z n-za-mN-ZA-M
* 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu

<h2> Bandit12: </h2>
* For this one, the basic idea is that you have to repeatedly decompress files; It's a long one so strap in
* mkdir /tmp/xyz
* cp /home/bandit12/data.txt /tmp/xyz
* xxd -r data.txt > data
* mv data a.gz
* gzip -d a.gz
* mv a a.bz2
* bzip2 -d a.bz2
* mv a a.gz
* gzip -d a.gz
* mv a a.tar
* tar xvf a.tar
* tar xvf data5.bin
* bzip2 -d data6.bin
* tar xvf data6.bin.out
* mv data8.bin data8.gz
* gzip -d data8.gz
* cat data8 
* 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL

<h2> Bandit13: </h2>
* ssh -i sshkey.private bandit14@localhost
* cat /etc/bandit_pass/bandit14
* 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e

<h2> Bandit14: </h2>
* Use the password above
* echo 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e \| nc localhost 30000
* BfMYroe26WYalil77FoDi9qh59eK5xNr

<h2> Bandit15: </h2>
* openssl s_client -connect localhost:30001
* Enter BfMYroe26WYalil77FoDi9qh59eK5xNr
* cluFn7wTiGryunymYOu4RcffSxQluehd

<h2> Bandit16: </h2>
* Gotta use the certificate in the correct port within the range
* nmap --open -p 31000-32000 localhost
* echo cluFn7wTiGryunymYOu4RcffSxQluehd \| openssl s_client -quiet -connect localhost:31790 > /tmp/abd/a.txt
* chmod 400 /tmp/abd/a.txt
* ssh -i /tmp/abd/a.txt bandit17@localhost

<h2> Bandit17: </h2>
* diff passwords.old passwords.new
* kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd

<h2> Bandit18: </h2>
* ssh -t bandit18@localhost /bin/sh
* cat readme
* IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x

<h2> Bandit19: </h2>
* Doing something with elevated permissions
* ./bandit20-do cat /etc/bandit_pass/bandit20
* GbKksEFF4yrVs6il55v6gwY5aVje5f0j

<h2> Bandit20: </h2>
* You need to open two terminal tabs at once
* echo GbKksEFF4yrVs6il55v6gwY5aVje5f0j \| nc -lvp 4444
* ./suconnect 4444
* gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr

<h2> Bandit21: </h2>
* cron is a time-based scheduler so it runs programs periodically
* cd /etc/cron.d/
* cat cronjob_bandit22
* cat /usr/bin/cronjob_bandit22.sh
* cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
* Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI

<h2> Bandit22: </h2>
* Same directory as above
* cat cronjob_bandiit23
* cat /usr/bin/cronjob_bandit23.sh
* echo I am user bandit23 \| md5sum \| cut -d ' ' -f 1
* cat /tmp/8ca319486bfbbc3663ea0fbe81326349
* jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n

<h2> Bandit23: </h2>
* Same technique as above; move the script file **with permissions** to /var/spool/bandit24 so that it can be run
* For example, the script I used was:
``` 
#!/bin/bash 
cat /etc/bandit_pass/bandit24 > tmp/lmn/lmn
```
* UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ

<h2> Bandit24: </h2>
* Made another simple script to find the password
* ./hut.sh \| nc -v localhost 30002
* hut.sh:
```
#!/bin/bash
for i in {0000..9999}
do
  echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i"
done
```
* uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

<h2> Bandit25: </h2>
* ssh -i bandit26.sshkey bandit26@localhost

<h2> Bandit26: </h2>
* V hard this one was; make the terminal as small as possible so that you can write commands in vi
* Press v to start vi
* VI COMMAND:e /etc/bandit_pass/bandit26
* 5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z <-- password to get INTO bandit26, not bandit27; this is so you can access bandit26 w/o bandit25
* Running vi /etc/passwd in Bandit25 shows that bandit26 is not using /bin/bash so we need to set shell to be /bin/bash
* VI COMMAND:set shell=/bin/bash
* VI COMMAND:sh
* ./bandit27-do cat /etc/bandit_pass/bandit27
* 3ba3118a22e93127a4ed485be72ef5ea <-- password for bandit27

<h2> Bandit27: </h2>
* gitception
* git clone ssh://bandit27-git@localhost/home/bandit27-git/repo /tmp/atlanta
* Read the README.md
* 0ef186ac70e04ea33b4c1853d2526fa2

<h2> Bandit28: </h2>
* git clone ssh://bandit28-git@localhost/home/bandit28-git/repo /tmp/atl
* cd .git
* git log -p
* bbc96594b4e001778eee9975372716b2

<h2> Bandit29: </h2>
* git clone ssh://bandit29-git@localhost/home/bandit29-git/repo /tmp/atl
* cd .git
* git log --all
* git reset --hard 33ce2e95d9c5d6fb0a40e5ee9a2926903646b4e3
* Read the README
* 5b90576bedb2cc04c86a9e924ce42faf 

