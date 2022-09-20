from zlib import crc32

def main():
    data = open('./corrupt-flag.png', 'rb').read()
    # ihdr size
    start = 12
    offset = 17
    ihdr = bytearray(data[start:start + offset])
    wi = 4 # width
    hi = 8 # height
    crc_correct = '0xf11d93ca'
    print(ihdr)
    
    for i in range(500, 1000):
        for j in range(500, 1000):
            print(i, j)
            height = i.to_bytes(4, 'big')
            width = j.to_bytes(4, 'big')
            guess = ihdr
            guess = guess[:hi] + height + guess[hi+4:]
            guess = guess[:wi] + width + guess[wi+4:]
            #print(crc32(guess), crc_correct)
            if hex(crc32(guess)) == crc_correct:
                print(crc32(guess), 0xf11d93ca)
                print("Found: ", height, width)
                input()
                break

# uscg{h1dd3n_1n_pl41n_s1ght}

if __name__ == '__main__':
    main()
