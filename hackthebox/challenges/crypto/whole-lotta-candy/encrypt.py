from Crypto.Util.Padding import pad
from Crypto.Util import Counter
from Crypto.Cipher import AES
import os


class Encryptor:

    def __init__(self):
        self.key = os.urandom(16)

    def ECB(self, pt):
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct = cipher.encrypt(pad(pt, 16))
        return ct

    def CBC(self, pt):
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(pt, 16))
        return ct

    def CFB(self, pt):
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        ct = cipher.encrypt(pad(pt, 16))
        return ct

    def OFB(self, pt):
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_OFB, iv)
        ct = cipher.encrypt(pad(pt, 16))
        return ct

    # Maybe I can try encrypting both the plaintext in ECB and CTR mode? 
    def CTR(self, pt):
        counter = Counter.new(128)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=counter) # new counter is created 
        ct = cipher.encrypt(pad(pt, 16))
        return ct

    # I think the encryption function creates a new IV each time for the block modes that have IVs
    # but in CTR mode, the counter starts at some initial value each time which makes it exploitable
    def encrypt(self, pt, mode):
        if mode == "ECB":
            ct = self.ECB(pt)
        elif mode == "CBC":
            ct = self.CBC(pt)
        elif mode == "CFB":
            ct = self.CFB(pt)
        elif mode == "OFB":
            ct = self.OFB(pt)
        elif mode == "CTR":
            ct = self.CTR(pt)
        return ct
