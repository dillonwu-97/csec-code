import requests

def main():
    a = open('./1.complex', 'rb').read()
    b = open('./2.complex', 'rb').read()
    c = open('./3.complex', 'rb').read()
    d = open('./4.complex', 'rb').read()

    for i,v in enumerate(a):
        if a[i] != b[i] and b[i] != c[i] and c[i] != d[i]:
            print(f"Payload starts: {i}th bytes")
            break

def solve():
    a = [
        '1010101010101010101010101010101001110011001000010100011010010011101000101111111110000100',
        '1010101010101010101010101010101001110011001000010100011010010011101000011111111100010100',
        '1010101010101010101010101010101001110011001000010100011010010011101100101111111100100100',
        '1010101010101010101010101010101001110011001000010100011010010011101100011111111101010111'
    ]
    b = []
    for v in a:
        b.append(''.join([hex(int(v[i:i+8],2))[2:].zfill(2) for i in range(0, len(v), 8)] )) 
    print(b)
    
    # <preamble><synch word><payload>
    # aaa...     7321...    rest
    # ['aaaaaaaa73214693a2ff84', 'aaaaaaaa73214693a1ff14', 'aaaaaaaa73214693b2ff24', 'aaaaaaaa73214693b1ff57']
    payload = 'aaaaaaaa'
    sync = '73214693'
    c = ['a2ff84', 'a1ff14', 'b2ff24', 'b1ff57']

    r = requests.session()
    for a in range(256):
        for b in range(256):
            pl = hex(a)[2:].zfill(2) + 'ff' + hex(b)[2:].zfill(2)
            data = {
                "pa" : payload,
                "sw" : sync,
                "pl" : pl
            }
            url = f"http://167.99.82.136:32275/transmit"
            print(f"Sending: {url} with {pl}")
            resp = r.post(url, data=data)
            if 'HTB' in resp.text:
                print("FOUND!")
                input()
                print(resp.text)

    
if __name__ == '__main__':
    # Flag: HTB{B4s1c_r4d10_fund4s}
    solve()

