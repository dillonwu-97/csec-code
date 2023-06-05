import requests

def main():
    print('hi')

    r = requests.get('https://uscg-web-wordy-w7vmh474ha-uc.a.run.app/api/game')
    d = r.json()
    game_id = d['game_id']
    print(d)

    payload = {
        "guess": "cacao",
        "game_id": game_id,
    }
    print(payload)
    r = requests.post('https://uscg-web-wordy-w7vmh474ha-uc.a.run.app/api/guess',json=payload)
    d = r.json()
    payload [ "guess" ] = d["correct_word"]
    r = requests.post('https://uscg-web-wordy-w7vmh474ha-uc.a.run.app/api/guess',json=payload)
    print(r.json())

    # USCG{1ucky_gu355_l0l}


if __name__ == '__main__':
    main()
