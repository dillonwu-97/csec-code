---
title: crypto
description: Crypto challenges from pico-ctf
tags: rsa, crypto
---

### The Numbers
The numbers are 16 9 3 15 3 20 6 {20 8 5 14 21 13 2 5 18 19 1 19 15 14}, and it stands for PICOCTF{THENUMBERSMASON}. 

### caesar
The flag is picoCTF{crossingtherubiconvfhsjkou}, the mapping being from a->e.

### Easy1
For the challenge, you just have to find the plaintext letter which maps to the ciphertext for a given key. e.g. 'C' (plaintext) + 'S' (key) = 'U' (ciphertext). The flag is picoCTF{CRYPTOISFUN}.

<img src = "/csec-writeups/pico-ctf/crypto/easy1.png"> <br/>

### 13
picoPGS{not\_too\_bad\_of\_a\_problem} flag was found using echo 'cvpbPGS{abg\_gbb\_onq\_bs\_n\_ceboyrz}' | tr 'a-z' 'n-za-m'. The flag is picoCTF{not\_too\_bad\_of\_a\_problem}. 

### la cifra de
The message is encrypted using the Vignere cipher. There are a couple of steps to this problem. First, I had to find the key size. This was done using the Kasiski method. Then, I had to find the text of the flag using frequency analysis. Additionally, it is important to note that the encryption is done using the formula: (plaintext + key) % 26 = ciphertext. The code for the problem can be found here: 
<a href="https://github.com/dillonwu-97/csec-code/blob/main/pico-ctf/crypto/la-cifra-de.py"> https://github.com/dillonwu-97/csec-code/blob/main/pico-ctf/crypto/la-cifra-de.py </a>
The flag is picoCTF{b311a50_0r_v1gn3r3_c1ph3ra966878a}.

### rsa-pop-quiz
For each question, the answers are in order:
1) 4636878989 

2) 93089

3) N

4) 836623060

5) 256931246631782714357241556582441991993437399854161372646318659020994329843524306570818293602492485385337029697819837182169818816821461486018802894936801257629375428544752970630870631166355711254848465862207765051226282541748174535990314552471546936536330397892907207943448897073772015986097770443616540466471245438117157152783246654401668267323136450122287983612851171545784168132230208726238881861407976917850248110805724300421712827401063963117423718797887144760360749619552577176382615108244813

6) N

7) 1405046269503207469140791548403639533127416416214210694972085079171787580463776820425965898174272870486015739516125786182821637006600742140682552321645503743280670839819078749092730110549881891271317396450158021688253989767145578723458252769465545504142139663476747479225923933192421405464414574786272963741656223941750084051228611576708609346787101088759062724389874160693008783334605903142528824559223515203978707969795087506678894006628296743079886244349469131831225757926844843554897638786146036869572653204735650843186722732736888918789379054050122205253165705085538743651258400390580971043144644984654914856729

8) 14311663942709674867122208214901970650496788151239520971623411712977120527163003942343369341


The library gmpy2 is very useful, and the functions invert(exp, phi) and pow(base, exp, modulo) is extremely useful. The code for the #8 is:
```python 
import gmpy2
e = 65537
n = 23952937352643527451379227516428377705004894508566304313177880191662177061878993798938496818120987817049538365206671401938265663712351239785237507341311858383628932183083145614696585411921662992078376103990806989257289472590902167457302888198293135333083734504191910953238278860923153746261500759411620299864395158783509535039259714359526738924736952759753503357614939203434092075676169179112452620687731670534906069845965633455748606649062394293289967059348143206600765820021392608270528856238306849191113241355842396325210132358046616312901337987464473799040762271876389031455051640937681745409057246190498795697239
c = 13433290949680532374013867441263154634705815037382789341947905025573905974395028146503162155477260989520870175638250366834087929309236841056522311567941474209163559687755762232926539910909326834168973560610986090744435081572047926364479629414399701920441091626046861493465214197526650146669009590360242375313096062285541413327190041808752295242278877995930751460977420696964385608409717277431821765402461515639686537904799084682553530460611519251872463837425068958992042166507373556839377045616866221238932332390930404993242351071392965945718308504231468783743378794612151028803489143522912976113314577732444166162766
p = 153143042272527868798412612417204434156935146874282990942386694020462861918068684561281763577034706600608387699148071015194725533394126069826857182428660427818277378724977554365910231524827258160904493774748749088477328204812171935987088715261127321911849092207070653272176072509933245978935455542420691737433

q = n // p
phi = (p-1) * (q-1)
d = gmpy2.invert(e, phi)
plain = pow(c, d, n)
print(plain)
```

After converting the last number to hex and ascii, the flag is picoCTF{wA8\_th4t$\_ill3aGal..oa2d2239b}.

```python
x = 14311663942709674867122208214901970650496788151239520971623411712977120527163003942343369341
hex_string = str(hex(x))[2:]
bytes_object = bytes.fromhex(hex_string)
ascii_string = bytes_object.decode("ASCII")
print(ascii_string)
```

### Tapping
Morse code. The flag is PICOCTF{M0RS3C0D31SFUN2683824610}.

# Mr-Worldwide
The flag contains locations from around the world. Just take the first letter of the names of the cities in each location.

Kyoto, Kyoto Prefecture 602-0953, Japan
Odesa, 65011, Ukraine
Dayton, OH 45402, United States of America
Istasyon Arkası Sokağı 1, 34110 Fatih, Turkey
Abu Dhabi, Abu Dhabi Emirate, United Arab Emirates
Kuala Lumpur, Malaysia
_
Addis Ababa, Ethiopia
Loja, Ecuador
Amsterdam, Netherlands
NY 10591, United States of America <-- this should be an S (Sidewalk Clock))
Kodiak, AK 99615, United States of America
Alexandria, 21561, Egypt

The flag is picoCTF{KODIAK_ALASKA}

### Flags
The flags are from the International Code of Signals, and the U.S. Navy. They can be found here: <a href= "http://www.quadibloc.com/other/flaint.htm"> http://www.quadibloc.com/other/flaint.htm </a>
The flag is PICOCTF{F1AG5AND5TUFF}.

### waves over lambda
use of ngrams
https://www.google.com/search?q=ngram_score+python&rlz=1C5CHFA_enUS752US752&oq=ngram_score+python&aqs=chrome..69i57j0i10i22i30.2364j0j7&sourceid=chrome&ie=UTF-8

http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-simple-substitution-cipher/
paper:
https://people.cs.uct.ac.za/~jkenwood/JasonBrownbridge.pdf


### miniRSA
I saw that the exponent for e was only 3. This stackoverflow response was also very helpful: <a href="https://crypto.stackexchange.com/questions/33561/cube-root-attack-rsa-with-low-exponent"> https://crypto.stackexchange.com/questions/33561/cube-root-attack-rsa-with-low-exponent </a>

This is also a useful resource I found for RSA attacks in general. It might be useful for future reference. <a href="Different possible attacks on RSA: https://www.utc.edu/center-academic-excellence-cyber-defense/pdfs/course-paper-5600-rsa.pdf"> Different possible attacks on RSA: https://www.utc.edu/center-academic-excellence-cyber-defense/pdfs/course-paper-5600-rsa.pdf </a>

```python
import gmpy2
a = 2205316413931134031074603746928247799030155221252519872649649212867614751848436763801274360463406171277838056821437115883619169702963504606017565783537203207707757768473109845162808575425972525116337319108047893250549462147185741761825125 
gmpy2.get_context().precision=2000
plaintext = int(gmpy2.root(a,3))
hex_string = str(hex(plaintext)[2:])
bytes_object = bytes.fromhex(hex_string)
ascii_string = bytes_object.decode("ASCII")
print(ascii_string)
```

The flag is picoCTF{n33d_a_lArg3r_e_606ce004}.


### b00tl3gRSA2
This link was somewhat helpful in deciding the values for d: <a href="https://security.stackexchange.com/questions/2335/should-rsa-public-exponent-be-only-in-3-5-17-257-or-65537-due-to-security-c"> https://security.stackexchange.com/questions/2335/should-rsa-public-exponent-be-only-in-3-5-17-257-or-65537-due-to-security-c
 </a>

The basic idea behind the attack is that if we use e as the value for decryption instead of d, it is easy to bruteforce the plaintext possibilities because there aren't many e values that are commonly used.

```python
import gmpy2

c= 4065571951557301009957182821220977078010174966477150653413044209621618699831837377473890962335829586414085984936531282725061469327690309960367481637884537090049255021031743872024515116425192071483925275092639183371512615027063611684821383836655938711667522553669891846649888421976735011263820746921294420800
n= 86470731054156303262263814023617576199721691896993592355150624936366244310708760397159848260637642244407332744582544244881306019061985238104817861439897100692305923988568211736175733611113480097937135653547108979557568091878020679277882393532848031843142813999471880711649980951277428856490984523764855017257
e= 28346387322695485287493717754602743596362678009597789617438332943724802672860628475099290172445169995252256537293610945832582793132546360917404015062861420230629862581424832910794110755860830199828494853755874012505185037033738152429655193286995256141647447668495646592034680337865693478103392926109533200753


# bruteforce attack
d_values = [3,5,17,257,65537]

for d in d_values:
	plaintext = pow(c, d, n)
	temp = pow(plaintext, e, n)
	if (temp == c):
		break

plaintext = bytes.fromhex(str(hex(plaintext))[2:]).decode("ascii")
print(plaintext)
```
The flag is picoCTF{bad_1d3a5_4783252}. 

### AES-ABC
The idea behind the attack is that ECB does not do a good job encrypting data because it encrypts similar patterns of data the same way. A good example of its ineffectiveness is by looking at the encryption of the Linux penguin image. In this specific exercise, we can find the flag by reverting the extra "abc" encryption to just the ECB encryption, and then looking at the image. 

The code can be found here:
<a href="https://github.com/dillonwu-97/csec-code/blob/main/pico-ctf/crypto/aes-abc.py"> https://github.com/dillonwu-97/csec-code/blob/main/pico-ctf/crypto/aes-abc.py </a>

The difference between the original and new image is as follows:  
<img src = "/csec-writeups/pico-ctf/crypto/aes-abc-1.png"> <br/>
<img src = "/csec-writeups/pico-ctf/crypto/aes-abc-2.png"> <br/>

picoCTF{d0Nt_r0ll_yoUr_0wN_aES}

### b00tl3gRSA3
The issue with n is that there are too many factors. You can calculate all of them, and then subsequently find the phi value.

```python
from sympy.ntheory import factorint
import gmpy2
n = 110504266836106505813652631353060736454736857680719872119876889565718044235936347375359009429367497498998137089143270754548057540932964497639424945495362650460647113738611898305812733562104005634913388059611308731386179931675943974396964618045291287518024952235399343249965286369836183996053730793484060645037745612935056338405992117338274121759
# a = factorint(n)
a = {16312549609: 1, 13869851497: 1, 11130556741: 1, 13466215501: 1, 11131415249: 1, 13296880199: 1, 13500553091: 1, 12929722381: 1, 16819243393: 1, 15069174623: 1, 13044867527: 1, 16958367841: 1, 14081926759: 1, 10676737921: 1, 10682180557: 1, 13978756423: 1, 11221436491: 1, 11880584693: 1, 13693693697: 1, 14679283973: 1, 11204189509: 1, 16705017011: 1, 14214223297: 1, 15366412717: 1, 13062777709: 1, 13709012441: 1, 8802854363: 1, 13658721683: 1, 13685118883: 1, 12974428517: 1, 10052779661: 1, 13230055667: 1, 15273103441: 1, 11776366519: 1}
factors = [i for i in a.keys()]
e = 65537
phi = 1
for i in factors:
	phi *= (i-1)
d = gmpy2.invert(e, phi)
c = 100385348975271299349033869906461176266183490581879592649498706755521216560860726568202690835163273089989248207677411805303731754096555044392244539312449253094506268129543711063052633948205841583597267302567565305474748595911882590775952098693135640020919098972330872308637758058224042492917363641167996691807861167644374526064489397274013326711
plaintext = pow(c, d, n)
ret = bytes.fromhex(hex(plaintext)[2:])
print(ret)
```

The flag is picoCTF{too_many_fact0rs_0731311}.

### john_pollard
I used <a href="https://www.sslchecker.com/certdecoder"> https://www.sslchecker.com/certdecoder </a> in order to find information about the certificate. The modulo is 4966306421059967 (0x11a4d45212b17f) and the exponent is 65537 (0x10001). 

The modulo is pretty small, so I just brute forced p and q.
```python
import gmpy2

if __name__ == '__main__':
	m = 4966306421059967
	e = 65537
	r = int(gmpy2.sqrt(m)) + 1
	ret = 0
	for i in range(1,r,2):
		if (m % i == 0):
			phi = (m // i - 1) * (i - 1)
			temp = gmpy2.gcd(e, phi)
			if temp == 1:
				p = m//i
				q = i
				break
	print(p,q)
```
The flag is picoCTF{73176001,67867967}.


