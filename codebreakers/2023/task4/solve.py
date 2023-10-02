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
        '/bin/zsh',
        '-c',
        f'echo -n {inp} | cryptsetup open --test-passphrase ./myfiles/payload.enc -T1'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stderr
    if res.returncode == 0:
        return res.stdout
    else:
        return res.stderr

def solve():
    print("[*] Testing")
    sandbox()

#    password_list = open('./password_list', 'w')
    print("[*] Producing all hashes")
    hostname = 'overtlycra'
    #alphanum = string.ascii_letters + string.digits
    alphanum = string.digits
    #                password_list.write(id_hash + '\n')
#    password_list.close()

    a = [
        "dle",
        "fts",
        "kes",
        "mps",
        "nch",
        "ned",
        "nes",
        "nks",
        "nny",
        "ped",
        "pes",
        "ppy",
        "sis",
        "tch",
        "ted",
        "ter",
        "tes",
        "vat",
        "ved",
        "ven",
        "ver",
        "ves",
        "wls",
        "wly",
        "yon"
    ]
    hostname = 'overtlycra'
    for i in alphanum:
        for j in alphanum:
            for k in alphanum:
                #id = hostname + chr(i) + chr(j) + chr(k)
#    for s in a:
        #id = hostname + i + j + k
                id = hostname + i + j + k
                print(f"Trying: {id}")
                id_hash = sha1(id.encode()).hexdigest()
                print(f"Trying: {id_hash}")
                out = check_hash(id_hash)
                print(out)
                if "No key" not in out:
                    print("FOUND", id)
                    input()

def main():
    solve()

if __name__ == '__main__':
    main()
