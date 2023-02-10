from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from os import urandom
from utils import *

FLAG = "crypto{???????????????????????????????}"


class CFB8:
    def __init__(self, key):
        self.key = key

    # At some point the encryption function will encrypt something that is all 0's 
    # the probability will be 1/256 
    def encrypt(self, plaintext):
        IV = urandom(16)
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct = b''
        state = IV
        for i in range(len(plaintext)):
            b = cipher.encrypt(state)[0]
            c = b ^ plaintext[i]
            ct += bytes([c])
            state = state[1:] + bytes([c])
        return IV + ct

    def decrypt(self, ciphertext):
        IV = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = b''
        state = IV
        for i in range(len(ct)):
            b = cipher.encrypt(state)[0]
            c = b ^ ct[i]
            pt += bytes([c])
            state = state[1:] + bytes([ct[i]])
        return pt

class Challenge():
    def __init__(self):
        self.before_input = "Please authenticate to this Domain Controller to proceed\n"

        # some random 20 byte password
        self.password = urandom(20)
        self.password_length = len(self.password)
        self.cipher = CFB8(urandom(16))

    def challenge(self, your_input):

        # the password check should be checking that zero equals to zero
        # this should be the last step I think
        if your_input['option'] == 'authenticate':
            if 'password' not in your_input:
                return {'msg': 'No password provided.'}
            your_password = your_input['password']
            if your_password.encode() == self.password:
                self.exit = True
                return {'msg': 'Welcome admin, flag: ' + FLAG}
            else:
                return {'msg': 'Wrong password.'}

        # Why would I need reset connection?
        # Because the key might not work to create the 0 values
        if your_input['option'] == 'reset_connection':
            # Generate a new cipher
            # Idea is probably to run this ~256 times until we get the 0 ciphertext
            self.cipher = CFB8(urandom(16))
            return {'msg': 'Connection has been reset.'}

        # This is the starting point? 
        # What is the point of reset password?
        # what is the token?
        if your_input['option'] == 'reset_password':
            if 'token' not in your_input:
                return {'msg': 'No token provided.'}

            # What should the length of the tokens ciphertext be?
            token_ct = bytes.fromhex(your_input['token'])
            if len(token_ct) < 28:
                return {'msg': 'New password should be at least 8-characters long.'}

            # the length is attached to the token ciphertext? 
            # Not sure how to attach the password length
            token = self.cipher.decrypt(token_ct)
            # The new password
            new_password = token[:-4]

            # The length of the password
            # What should the length be?
            # I think password length would be 0
            self.password_length = bytes_to_long(token[-4:])

            # Setting my password for comparison; the value should be set to 0
            self.password = new_password[:self.password_length]
            return {'msg': 'Password has been correctly reset.'}

listener.start_server(port=13399)
