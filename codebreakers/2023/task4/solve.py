from hashlib import sha1
import subprocess
import string
# Getting the candidates for the id values

def sandbox():
    teststr = 'overtlycraaaa'.encode()
    id_hash = sha1(teststr).hexdigest()
    print(id_hash)

def check_hash(inp):
    cmd = [
        '/bin/bash',
        '-c',
        f'echo -n {inp} | cryptsetup open --test-passphrase ./myfiles/payload.enc',
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stderr
    if res.returncode == 0:
        return res.stdout
    else:
        return res.stderr

def build_list():
    print("[*] Creating dictionary")
    alphanum = '0123456789abcdef'
    f = open('./dic.txt', 'w')
    hostname = 'overtlycra'

    for i in alphanum:
        for j in alphanum:
            for k in alphanum:
                id = hostname + i + j + k 
                id_hash = sha1(id.encode()).hexdigest()
                f.write(id_hash + '\n')
    f.close()

def solve():
    print("[*] Testing")
    sandbox()
    print("[*] Producing all hashes")
    hostname = 'overtlycra'
    alphanum = string.ascii_letters + string.digits

    hostname = 'overtlycra'
    for i in alphanum:
        for j in alphanum:
            for k in alphanum:
                id = hostname + i + j + k
                print(f"Trying: {id}")
                id_hash = sha1(id.encode()).hexdigest()
                print(f"Trying: {id_hash}")
                out = check_hash(id_hash)
                print(f"Message: {out}")
                if "No key" not in out:
                    print("FOUND", id)
                    input()

def recover():
    to_find = '87679d282b7869b3900d61875d0123ad367936e8'
    str_list = '0123456789abcdef'
    assert (len(to_find) % 2 == 0)
    for i in str_list:
        for j in str_list: 
            for k in str_list:
                id = 'overtlycra' + i + j + k
                id_hash = sha1(id.encode()).hexdigest()
                print(id_hash)
                if id_hash == to_find:
                    print(i + j + k)
                    input()

def main():
    #solve()
    #build_list()
    recover()

if __name__ == '__main__':
    main()
