import requests
import base64
from Crypto.Util.number import bytes_to_long, long_to_bytes

cookies = {
        "auth_name": "Q2wvZUVTd2VBRXJXMWM4Uy9vRHlhU3R3ZzQ1Wi85QUNobFRDRkdEWDVtVFNIUEd6SWFTb2ZnZ2ZERnM5TzVaVm1yeDZBZmJJT0hnWDU0dHlTL2o4QjFIMU9VMHVDYUl5UEszdFo3MzF0QWw4OXZPaCs0eHlmT1luR3U3L1dVdkk="
        }
b = base64.b64decode(cookies["auth_name"])

# For each byte, try a different byte from 0 -> 255 inclusive

for i in range(0, len(b)):
    print(i)
    for j in range(0, 256):
        temp = b[:i] + bytes([j]) + b[i+1:]
        assert (len(temp) == len(b))
        new_auth = base64.b64encode(temp).decode()
        cookies["auth_name"] = new_auth 
        r = requests.get(url = 'http://mercury.picoctf.net:10868/',cookies=cookies)
        if "picoCTF{" in r.text:
            print(cookies)
            input()
            break

Q2wvZUVTd2VBRXJXMU04Uy9vRHlhU3R3ZzQ1Wi85QUNobFRDRkdEWDVtVFNIUEd6SWFTb2ZnZ2ZERnM5TzVaVm1yeDZBZmJJT0hnWDU0dHlTL2o4QjFIMU9VMHVDYUl5UEszdFo3MzF0QWw4OXZPaCs0eHlmT1luR3U3L1dVdkk=

# picoCTF{cO0ki3s_yum_e57b2438}


