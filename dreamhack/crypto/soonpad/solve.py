# idea is to maybe 
from Crypto.Util.Padding import pad, unpad
from pwn import *
import string


LOCAL = False
if LOCAL:
    r = process('./soonpad.py')
else:
    """ r = remote('host3.dreamhack.games',24238) """
    r = remote('host3.dreamhack.games',24476)
current = 'soon_haari_loser'[:-1]


# 13 byte starting buffer?
def get_char(prepend, padding_size):
    # need to brute force the very first byte 
    for candidate in string.printable:
        r.sendlineafter(": ", candidate + prepend + 'z' * padding_size)
        """ print("current: ", current) """
        if LOCAL:
            pt = r.recvline().decode().split(": ")[1].strip()
            """ print(f"Length: {len(pt)} {pt}") """
            """ print("start: ", pt.encode().hex()[:32], "end: ", pt.encode().hex()[-32:]) """
            assert len(pt) % 16 == 0
        ct = r.recvline().decode().strip()
        to_find = ct[256:288] # the block to decrypt
        leak = ct[:32]
        """ print(f"Ct: {ct}") """
        """ print(f"to find: {to_find}\nleak: {leak}") """
        if leak == to_find:
            print(f"Found character!: {candidate}")
            return candidate

# need to figure out how to split the message actually
# encode() is utilized
def part2(guess):
    r.sendlineafter(": ", guess)
    if LOCAL:
        lencheck = r.recvline()
        soonpad1 = r.recvline()
        soonpad2 = r.recvline()
        print("lencheck: ", lencheck)
        print("soonpad1: ", soonpad1)
        print("soonpad2: ", soonpad2.strip())
    ct = r.recvline().decode().strip() 
    """ print("ct is: ", ct) """
    assert (len(ct) > 32)
    """ to_find = ct[320:352]  """
    """ to_find = ct[l:ri] """
    """ to_find = ct[-32:] """
    leak = ct[:32]
    if leak in ct[32:]:
        return True
    """ if to_find == leak: """
    """     return True """

def main():
    # does it work if i keep shifting it over?
    # maybe i shouldnt cut off the values 
    # what happens if i make the padding consistent as well 
    # consistnet padding and sliding window should work fine 
    start_val = 'soon_haari_loser'
    flag = ''
    """ for i in range(100): """
    """     print(f"i is: {i}") """
    """     l = get_char(start_val, 12) """
    """     start_val = l + start_val  """
    """     flag = l + flag """
    """     print(f"flag is: {flag}") """
    flag = 'DH{There are two ways to make a person angry. First one is to stop in the middle of the conversation'
    """ flag = 'HHFT@NDSCILLHAAPRLLF@RPRCNJRJCQGKSIOMOGJQCBLBNAGJNPHSENMPIDHOQFECABMQDMRJPOOI@MHKESMGKGHTOMKFKMMTPJE' """
    r.sendline(flag)
    r.recvline()
    r.recvline()

    # let's try to crack the first character in the second part first
    # 13 expanded -> 26 
    # 3 A's
    
    # ok first character leak is vald 
    # need to modify the first block now 
    # fields that need to be modified in guess: candidate
    # in extension, modify number of \x90 values and the number of A values to stretech the padding from 16 -> 32
    # handle this edge case first where padding is still involved
    # need to shrink the extension
    flag2 = 'soon_haari_los'
    for i in range(1, -1, -1):
        for candidate in string.printable:
            guess = pad(candidate.encode() + flag2.encode(),16 )
            extension = '\x90'.encode() * (16-i) + b'A' * (i)
            payload = guess + extension
            """ print("candidate: ", i, candidate, flag2) """
            """ print("payload: ", payload.hex(), len(payload.hex())) """
            if part2(payload):
                print("Found: ", candidate)
                flag2 = candidate + flag2 
                break

    for j in range(6):
        for i in range(15, -1, -1):
            for candidate in string.printable:
                guess = candidate.encode() + flag2[:16].encode()
                extension = '\x90'.encode() * (16-i) + b'A' * (i)
                payload = guess + extension
                """ print("candidate: ", candidate, flag2) """
                """ print("payload: ", payload.hex(), len(payload.hex())) """
                if part2(payload):
                    print("Found: ", candidate)
                    flag2 = candidate + flag2 
                    break
    print("flag2: ", flag2)
   

    # do this again for the non edge cases 
    # \x90 pushes one out now
     
    
    """ r.interactive() """


if __name__ == '__main__':
    # rand bytes 
    # flag:
    # DH{There are two ways to make a person angry. First one is to stop in the middle of the conversation, second one is to use a character with 2+ bytes.}
    main()


