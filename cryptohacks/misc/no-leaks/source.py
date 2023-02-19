import base64
import os
from utils import listener

FLAG = "crypto{????????????}"


def xor_flag_with_otp():
    flag_ord = [ord(c) for c in FLAG]
    otp = os.urandom(20)

    xored = bytearray([a ^ b for a, b in zip(flag_ord, otp)])

    # make sure our OTP doesnt leak any bytes from the flag

    # assert that each character in xored is not the same as the same corresponding character in the flag; the only way they are the same is if the byte is 0
    # idea is to slowly crack each character in the flag? 
    # what is the probability of hitting a 0 in the random bytes?
    # 20 * (1/256 characters) = 20 / 256 ~ 1/12? 
    # 20 characters long, we know the first seven characters and the last character
    # so idea can be to replace all other characters with 0x0, except for the one we are trying to guess, and after some number of iterations 
    # if there is a leaky ciphertext, either one of them is an 0x0 or one of the values is a character in the flag, and we know that 0x0 cannot be a character, so we can guess that the guessed character is the flag? but there are 256 characters that we need to guess, and it will get xored with some random value each time so 20 * 256 * 256 is a lot of tries 
    # actually, after reading more of the code, this isn't even what we can do
    for c, p in zip(xored, flag_ord):
        assert c != p

    return xored


class Challenge():
    def __init__(self):
        self.before_input = "No leaks\n"

    def challenge(self, your_input):
        if your_input == {"msg": "request"}:
            try:
                ciphertext = xor_flag_with_otp()
            except AssertionError:
                return {"error": "Leaky ciphertext"}

            # from each ciphertext given to us, we know that it contains characters which cannot be the character we are looking for. So the algorithm might be to create a 2d array of size 20 * 256, and to mark off each character until we can narrow down the combinations
            ct_b64 = base64.b64encode(ciphertext)
            return {"ciphertext": ct_b64.decode()}
        else:
            self.exit = True
            return {"error": "Please request OTP"}


"""
When you connect, the 'challenge' function will be called on your JSON
input.
"""
listener.start_server(port=13370)
