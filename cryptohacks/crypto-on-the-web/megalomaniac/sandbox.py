from string import ascii_letters, digits
from Crypto.Random import get_random_bytes, random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256, SHA512
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
import json

# Alice password and salt
""" SALT = get_random_bytes(8) """
SALT = b'AAAAAAAA'
PASS = "".join([random.choice(ascii_letters + digits) for _ in range(20)]).encode()

FLAG = b"crypto{???????????????????????????????????}"

class Client:
    def __init__(self, password, salt):
        self.password = password
        self.salt = salt
        self.gen_keys()
        self.cipher_enc = AES.new(self.enc_key, AES.MODE_ECB)
        self.cipher_master = AES.new(self.master_key, AES.MODE_ECB)
        self.prepare_crypto_material()

    def gen_keys(self):

        # This creates the keys using PBKDF2 (public key derivation function)
        keys = PBKDF2(self.password, self.salt, 32,
                      count=1000, hmac_hash_module=SHA512)

        # From that extract the encryption and authentication key
        self.enc_key, self.auth_key = keys[:16], keys[16:]
        self.auth_key_hashed = SHA256.new(self.auth_key).hexdigest()

        # Master key, shared key, shared public key
        self.master_key = get_random_bytes(16) # master key is 16 bytes
        self.share_key = RSA.generate(2048) # this is 2048 bytes long?
        self.share_key_pub = (self.share_key.n, self.share_key.e)

    
    def prepare_crypto_material(self):
        # encrypted master key (encrypted) using the public key
        self.master_key_enc = self.cipher_enc.encrypt(self.master_key)

        # encrypted rsa private key??
        self.share_key_enc = self.cipher_master.encrypt(self.format_rsa_privkey())

    def format_rsa_privkey(self):
        data = b""
        data += self.format_number(self.share_key.p)
        data += self.format_number(self.share_key.q)
        data += self.format_number(self.share_key.d)
        data += self.format_number(self.share_key.u)
        return pad(data, 16)

    def format_number(self, num):
        num_bytes = long_to_bytes(num)
        return long_to_bytes(len(num_bytes), 2) + num_bytes

    def get_encrypted_flag(self):
        secret = SHA256.new(long_to_bytes(self.share_key.p) +
                            long_to_bytes(self.share_key.q)).digest()
        ct = AES.new(secret, AES.MODE_ECB).encrypt(pad(FLAG, 16))
        return ct


class Client_new_login:
    def __init__(self, password, salt):
        self.password = password
        self.salt = salt
        self.gen_keys()
        self.cipher_enc = AES.new(self.enc_key, AES.MODE_ECB)

    def gen_keys(self):
        keys = PBKDF2(self.password, self.salt, 32,
                      count=1000, hmac_hash_module=SHA512)
        self.enc_key, self.auth_key = keys[:16], keys[16:]
        self.auth_key_hashed = SHA256.new(self.auth_key).hexdigest()

    def login_step2(self, SID_enc, share_key_enc, master_key_enc):
        self.master_key = self.cipher_enc.decrypt(master_key_enc)
        # master key is used to create the cipher master
        self.cipher_master = AES.new(self.master_key, AES.MODE_ECB)

        share_key = unpad(self.cipher_master.decrypt(share_key_enc), 16)
        p, q, d, u = self.parse_rsa_privkey(share_key)

        # this is what we attack atm 
        SID = self.RSA_CRT_decrypt(SID_enc, p, q, d, u)
        #Remove padding on the plaintext
        print("sid before padding off: ", SID.hex(), len(SID))
        SID = SID[:-16]
        print("sid is: ", SID.hex(), len(SID))
        print("q is: ", q, long_to_bytes(q).hex())
        print("p is: ", p , long_to_bytes(p).hex())
        return SID

    # We can manipulate u so that it eventually tells us what q is
    def RSA_CRT_decrypt(self, ciphertext, p, q, d, u):

        # if the ciphertext were smaller than m and we were doing RSA decryption without the CRT speedup, then ct ^ d % m not necessarily < m unless d is 1
        # 
        ct = bytes_to_long(ciphertext)
        dp = d % (p - 1)
        dq = d % (q - 1)
        mp = pow(ct, dp, p) 
        mq = pow(ct, dq, q) 
        t = (mq - mp) % q 
        h = (t * u) % q 
        m = h * p + mp # m = 0 when h = 0, mp = 0
        return long_to_bytes(m)

    def parse_rsa_privkey(self, share_key):
        index = 0
        elements = []
        while index < len(share_key):
            length = bytes_to_long(share_key[index:index + 2])
            index += 2
            elements.append(bytes_to_long(share_key[index:index + length]))
            index += length
        assert len(elements) == 4
        return elements

# Objective for the first challenge is to leak q I believe
class Challenge():
    def __init__(self):
        self.C = Client(PASS, SALT)
        self.C_ = None
        material = json.dumps({"auth_key_hashed": self.C.auth_key_hashed, "master_key_enc": self.C.master_key_enc.hex(), "share_key_pub": self.C.share_key_pub, "share_key_enc": self.C.share_key_enc.hex()})
        self.before_input = f"NEW CLIENT REGISTRATION :\nEmail : alice@CH.org\nUsername : Alice\nNew client is uploading crypto material...\n{material}\n"
        self.current_step = "PROCESSING"
        self.max_payload_size = 8192

    def challenge(self, message):
        if not "action" in message:
            self.exit = True
            return {"error": "Please choose an action."}

        if message["action"] == "wait_login":
            self.current_step = "LOGIN"
            self.before_send = f"Login attempt from Alice:\n"

            # some random password and salt
            self.C_ = Client_new_login(PASS, SALT)

            # Give me the auth key. What is this used for?
            # this is different from C.auth_key_hashed I think?
            return {"auth_key_hashed": self.C_.auth_key_hashed}

        # this indiciates that the sequence of steps must be wait_login -> block
        elif message["action"] == "block":
            if self.current_step != "LOGIN":
                self.exit = True
                return {"error": "Wrong order"}
            self.current_step = "PROCESSING"
            return {"message": "User was successfully blocked."}

        # this indicates that the sequence of steps must be wait_login -> send_challenge
        elif message["action"] == "send_challenge":
            if self.current_step != "LOGIN":
                self.exit = True
                return {"error": "Wrong order"}
            self.current_step = "PROCESSING"

            # Have to provide three sources of information for processing
            if not "SID_enc" in message or not "share_key_enc" in message or not "master_key_enc" in message:
                return {"error": "Please provide the encrypted SID, share_key and master_key."}

            else:
                # check to see if login is permitted using the encrypted keys
                # login_step2 should be used for the oracle that gives us information about q
                try:
                    SID_enc = bytes.fromhex(message["SID_enc"])

                    # we modify the share_key_enc value
                    # Specifically, we modify q_inv? (which is the u portion of the payload)
                    # We also send a custom SID_enc value which should be the key we are looking for
                    share_key_enc = bytes.fromhex(message["share_key_enc"])
                    master_key_enc = bytes.fromhex(message["master_key_enc"])
                    return {"SID": self.C_.login_step2(SID_enc, share_key_enc, master_key_enc).hex()}
                except Exception as e:
                    return {"error": "An error occured during the login."}

        # Flag for this challenge
        elif message["action"] == "get_encrypted_flag":
            return {"encrypted_flag": self.C.get_encrypted_flag().hex()}

        else:
            return {"error": "This is not a valid action."}

def main():
    pass

if __name__ == '__main__':
    main()
