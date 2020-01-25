# Bandit0

ssh bandit0@bandit.labs.overthewire.org -p 2220  
password: bandit0 
password in readme: boJ9jbbUNNfktd78OOpsqOltutMc3MY1

# Bandit1
cat /home/bandit1/-
password: CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9

# Bandit2
cat "spaces in this filename"
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK

# Bandit3
* Idea is to find the hidden file
* cat ./inhere/.hidden
* pIwrPrtPN36QITSp3EQaw936yaFoFgAB

# Bandit4
* Made a short script to iterate through the files
* for i in {1..9}; do echo test${i}; cat /home/bandit4/inhere/-file0${i}; done
* koReBOKuIDDepwhWk7jZC0RTdopnAYKh

# Bandit5
* Use built-in Linux search mechanisms
* find inhere -type f -size 1033c ! -executable -readable inhere/maybehere07/.file2
* DXjZPULLxYr17uwoI01bNLQbtFemEgo7

# Bandit6: 
* Similar idea as bandit5 plus a little extra work
* find ./ -group bandit6 -user bandit7 -size 33c 2>&1 | grep -v 'Permission'
* HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs

# Bandit7: 
* find "millionth"
* cat data.txt | grep -e "millionth"
* cvX2JJa4CFALtqS87jk27qwqGhBM9plV

# Bandit8: 
* sort data.txt | uniq -u
* UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR

# Bandit9: 
* strings data.txt | grep -e "=="
* truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk

# Bandit10: 
* base64 -d data.txt | cat
* IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR

# Bandit11:
* cat data.txt | tr a-zA-z n-za-mN-ZA-M
* 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu

# Bandit12:
* For this one, the basic idea is that you have to repeatedly decompress files
mkdir /tmp/xyz
cp /home/bandit12/data.txt /tmp/xyz
xxd -r data.txt > data
* 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL

# Bandit13:
* 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e

# Bandit14:
* BfMYroe26WYalil77FoDi9qh59eK5xNr

# Bandit15:
* cluFn7wTiGryunymYOu4RcffSxQluehd

# Bandit16:
* use certificate

# Bandit17:
* kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd

# Bandit18:
* IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x

# Bandit19:
* GbKksEFF4yrVs6il55v6gwY5aVje5f0j

# Bandit20:
* gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr

# Bandit21:
* Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI

# Bandit22:
* jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n

# Bandit23:
* UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ

# Bandit24:
* uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

# Bandit25:
* 5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z

# Bandit26:
* 3ba3118a22e93127a4ed485be72ef5ea

# Bandit27:
* 0ef186ac70e04ea33b4c1853d2526fa2

# Bandit28:
* bbc96594b4e001778eee9975372716b2

# Bandit29:
* 5b90576bedb2cc04c86a9e924ce42faf

# Bandit30:
*
