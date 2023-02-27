---
title: mysterybox
description: signature forgery with rsa
tags: crypto, rsa, signature
---
A description of the attack on stack overflow can be found here:
<a href="https://crypto.stackexchange.com/questions/35644/chosen-message-attack-rsa-signature"> https://crypto.stackexchange.com/questions/35644/chosen-message-attack-rsa-signature </a>

For this problem, I needed to forge a signature for the string "Username: Admin, Access code: CryptoBestCategoryF3", which is the integer 861934499667986621552658522992711737960484613144058684918624923247791760594840402997853247655770722704545163272571668019. However, I could not get the signature for that integer value so instead, I got the signature for -1 and -861934499667986621552658522992711737960484613144058684918624923247791760594840402997853247655770722704545163272571668019. When the signatures are multiplied together, it is in effect, the same as the signature for 861934499667986621552658522992711737960484613144058684918624923247791760594840402997853247655770722704545163272571668019.

Flag: HTB{3mpl0y33s\_mu5t\_h45h\_4ll\_m3554g3s\_b3f0r3\_l00k1ng\_4t\_th3m\_t0\_pr3v3nt\_bl1ndn3ss}
