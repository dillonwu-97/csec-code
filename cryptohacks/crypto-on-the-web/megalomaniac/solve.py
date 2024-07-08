from pwn import *
from Crypto.Hash import SHA256, SHA512
from Crypto.Cipher import AES
from ast import literal_eval
import json 
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
from sandbox import Challenge

# modify the u value to be u' by flipping one of the bytes from position 33 -> 41
# should be 16 byte chunks  -> 41 chunks 
# but then where does the padding go?
# last block contains 8 byte padding 
# theoretically, it shouldnt matter what value it is 
def modify_u(sk_enc):
    sk_enc = bytes.fromhex(sk_enc)
    print(sk_enc, len(sk_enc) // 16, 34 * 16)
    # index 40 fucks up the padding i believe
    ret = sk_enc[:39*16] + b'\x03' + sk_enc[39*16+1:]
    assert len(ret) == len(sk_enc)
    return ret

def enc_msg(n, e, msg):
    return long_to_bytes(pow(bytes_to_long(msg), e, n)).hex()


def solve():

    r = remote('socket.cryptohack.org', 13408)
    l = r.recvuntil("...\n")
    d = literal_eval(r.recvline().decode().strip('\n'))
    ak_hashed = d['auth_key_hashed']
    mk_enc = d['master_key_enc']
    sk_pub = d['share_key_pub']
    sk_enc = d['share_key_enc']
    print(ak_hashed)
    n = sk_pub [0]
    e = sk_pub [1]

    m = {
        "action": "get_encrypted_flag"
    }
    r.sendline(json.dumps(m))
    enc_flag = literal_eval(r.recvline().decode().strip('\n'))['encrypted_flag']
    print(enc_flag)
    enc_flag = bytes.fromhex(enc_flag)
    print(enc_flag)

    m = {
        "action": "wait_login",
    }
    r.sendline(json.dumps(m))
    r.recvuntil("Alice:\n")
    """ print(r.recvline()) """
    l = literal_eval(r.recvline().decode().strip('\n'))
    # okay they are the same
    ak_hashed = l['auth_key_hashed']
    print(ak_hashed)

    # send challenge now
    # what are all of these values?
    sk_prime = modify_u(sk_enc)
    print("sk prime: ", sk_prime, len(sk_prime))
    # what is the max value and what is the min value? 
    # min value is 0 obviously
    """ what is 2^1024 in bytes? """
    """ print(long_to_bytes(pow(2,1024))) """
    """ val = enc_msg(n, e, pad(b"\x41"*16, 16)) # encrypt the message  """
    """ print("encrypted message to send: ", val) """
    """ print(type(val)) """
    # send the encrypted message over network and request decryption
    # check that the message matches 
    # is there padding?
    # is the response encrypted or not?
    # 1024 is the upper bound
    # what is a good stopping condition?
    # could technically make binary search good, but maybe there is another side channel that i can use instead 
    upper = pow(2,1024) // 2
    lower = 0
    mid = 0
    candidate = None
    for i in range(1024):
        if lower >= upper:
            print("mid: ", mid)
            input()
            break
        mid = (upper + lower) // 2
        print("candidate: ", mid)
        temp = long_to_bytes(mid) + b'\x10' * 1
        """ assert len(temp) % 16 == 0 """

        """ print(temp) """
        val = enc_msg(n, e, temp) # could be that the encryption is wrong? not sure, should be gettinb back the right value 
        m = {
            "action": "send_challenge",
            "SID_enc": val, # do not need to modify, i think this is the oracle
            # actually, we might be modifying the sid value 
            # not sure what length the SID is supposed to be 
            "share_key_enc": sk_prime.hex(), # need to double check this there was a bug here
            "master_key_enc": mk_enc # do not need to modify
        }
        """ print(m) """
        l = r.sendline(json.dumps(m))
        recv = r.recvline()
        """ print(recv) """
        cor_sid = literal_eval(recv.decode().strip('\n'))['SID']
        """ print("corrupted sid: ", cor_sid, temp.hex()) """
        print(temp.hex())
        
        if (cor_sid != temp[:-16].hex()): # go lower
            print(i, "not equal")
            upper = mid
        else: # go upper
            print(i, "equal")
            lower = mid
            if (n % mid == 0):
                input("Found!: ", mid)
                break

        m = {
            "action": "wait_login",
        }
        candidate = temp
        r.sendline(json.dumps(m))
        r.recvuntil("Alice:\n")
        """ print(r.recvline()) """
        l = literal_eval(r.recvline().decode().strip('\n'))

    print(candidate)
    p = None
    q = None
    phi = None
    for i in range(256):
        temp = bytes_to_long(candidate) - 16 + i
        if n % temp == 0:
            p = temp
            break
    print("public key: ", n)
    print("p: ", p)
    print("enc: ", enc_flag)
    q = n // p
    phi = (p-1) * (q-1)
    d = pow(e, -1, phi) 
    print("d: ", d)
    flag = pow(enc_flag, d, n)
    print(long_to_bytes(flag))

def quicksolve():

    n = 18948265214535448635762504022275411914869103440845532654495906580147995703453858449132423616448102527548721714128907071066104527184783481743326382047590195364650131723447580987632061357883926731051239318779182046432670457926736564042259559872632151163194324661797353998048959633686052721863691319769967067738236700475403285350709642183892830544844103412842112029859708528086727885936289111233013649007528314209690907298256548418374353076497183290735844267375101227628822021250642552177416473355805574108432528891524393015583508207292683540397361908648506487044119391383292409321598438935231036937076478182729056799777
    p = 130501124793449030733624886542471072022350913170750700735884120737800027355430886740583494384663112575433618680696385612163420803380795418618759061486938034030719692917949519739792950317286033603492441743870516972117531604838296006565230369011143324915346277228852406320402186719645238151871576121032765458111

    enc_flag =   14696471723617101650568002931762805377411199881741706590963808106847295056144762738151411662121548423618511680450894
    q = n // p

    secret = SHA256.new(long_to_bytes(p) + long_to_bytes(q)).digest()
    flag = AES.new(secret, AES.MODE_ECB).decrypt(long_to_bytes(enc_flag))
    print(flag)
    print(bytes_to_long(flag))

def local():
    c = Challenge()
    d= literal_eval(c.before_input.split('...')[1].strip('\n'))

    ak_hashed = d['auth_key_hashed']
    mk_enc = d['master_key_enc']
    sk_pub = d['share_key_pub']
    sk_enc = d['share_key_enc']
    print(ak_hashed)
    n = sk_pub [0]
    e = sk_pub [1]
    """ print(n,e) """
    m = {
        "action": "wait_login",
    }
    ret = c.challenge(m)
    print("ret: ", ret)

    sk_prime = modify_u(sk_enc)
    print("sk prime: ", sk_prime, len(sk_prime))
    upper = pow(2,1024) // 2
    lower = 0
    mid = 0
    for i in range(1024):
        if lower >= upper:
            print("mid: ", mid)
            break
        mid = (upper + lower) // 2
        temp = long_to_bytes(mid) + b'\x10' * 1 # not sure why 0x10 16 times blocks out the value instead; very confused 
        val = enc_msg(n, e, temp) 
        m = {
            "action": "send_challenge",
            "SID_enc": val, 
            "share_key_enc": sk_prime.hex(), 
            "master_key_enc": mk_enc 
        }
        recv = c.challenge(m)
        cor_sid = recv['SID']
        print("guess: ", temp.hex())
        
        if (cor_sid != temp[:-16].hex()): # go lower
            print(i, "not equal")
            upper = mid
        else: # go upper
            print(i, "equal")
            lower = mid

        m = {
            "action": "wait_login",
        }
        recv = c.challenge(m)
        print(recv)

    print("public key: ", n)



def main():
    """ solve() """
    quicksolve()


if __name__ == '__main__':
    main()

""" 425003226275396219829821321305797092867888560790242042147922010132869248491268022783665951232441857392393415769299202444347605206638136070433254579119085465090985801712572163666973754180061198430361604429652478326919283515048656650480876502448221542985466619833399865297 



378949073267189949691028296277501665241682951947500893025412706956742404834517157708741443687399841421650093390830672648079147566184553569932935757325886133619331122784081567101286971324045555122814724347517014525660551483635495358585068297461220357127533803362901217083

21384401437095063903309585511153083057086643417419080449815377017585382672906783722320438974127881139439561404005238144489125375037188468852657021685871461199512008939176542688043000422774389428016624031027798773942454510810631801355376332773338143013318757931053526823376715303262293636240332957876153685778960078544522121000705909279604414427470211500447215280279617022170957326173491092470587588985692836343889080391590833487061200830039353334576637959687960686177886481277302256479192511744716017359439509276861308434128387840251238998328418343475549165214840482430285750723401488559759134271104122519564605435893



# Very useful
https://www.linkedin.com/pulse/rsa-chinese-remainder-theorem-mega-exploits-marjan-sterjev-gcbee/ 

So the reason I think that the last 16 bytes of the SID being cut off isn't that relevant because it's just an oracle. if we have shot above the value in any way, the value returned will be completely wrong including the upper bytes 
and then something something padding i guess


"""

# Flag: b"crypto{M4lleaBl3_3nCRypt1on_g0n3_wr0nG_:'(}\x05\x05\x05\x05\x05"

