Okay, so we have encrypted data
User gets prompted to put in ssh password
Then, some chrome key gets unencrypted with the password credentials?
ok, pretty sure i have the key; how to use?
how was the data encrypted?
in theory, should be the same way that LOCALAPPDATA is encrypted



Idea:

Okay, the idea is that there is data being exfiltrated with the putty executable. The exfiltrated data is encrypted with AES GCM and the key is base 64 encoded in the wireshark packet capture. Starting from the 4096th byte and onwards, we have the encrypted exfiltrated data. The encrypted exfiltrated is xored with rand() values generated from a sequence with the seed value being 47104. To decrypt the payload, we xor each byte with rand() values. Then, we use the key we grabbed to decrypt the xor-decrypted payload. The first 3 bytes are header bytes. Bytes 3->15 is the IV. Where did i fk up??? 

okay, to summarize. localdata contains a key encrypted using cryptprotectdata. it can be decrypted using cryptunprotectdata. this key is used to decrypt passwords in the logindata directory, which are binary blobs. these blobs contain info like iv, tag, header and was generated using aes-gcm with the decrypted symmetric key

I need to verify that the first bytes are decrypted correctly. 
I need to verify that AES-GCM is in fact the decryption algorithm to use because I actually don't know if this is the case.
