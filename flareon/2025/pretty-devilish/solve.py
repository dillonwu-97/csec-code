import zlib
import os
import binascii
from PIL import Image

def decrypt(val):
    '''
    decrypt with qpdf and write to dec
    '''
    f = open('./dump', 'rb')
    dump = f.read()
    dump = dump.split(b'stream\r')
    new_data = b'\n' + val + b'\nend'
    dump[1] = new_data
    new_data = b'stream\r'.join(dump)
    f.close()

    f = open('./dump', 'wb')
    f.write(new_data)
    f.close()
    _ = os.system("qpdf --decrypt dump dec 2>/dev/null")

# get compression
def decomp():
    f = open('./dec', 'rb')
    dec = f.read()
    # print(dec)
    # f.close()
    dec = dec.split(b'stream\n')[1].replace(b'end',b'')
    print("dec: ", dec.hex())
    dump = zlib.decompress(dec)
    if b'@' in dump:
        print(dump)
        input()
    print("dump: ", dump.hex())
    print(dump)
    f.close()
    return dump

def main():
    # for i in range(20):
    dump = decomp()
    f = open('./pic', 'wb')
    temp = dump.split(b'ID\n')[1].split(b'\nEI')[0]
    f.write(binascii.unhexlify(temp))
    f.close()
    print(dump)
    # decrypt(dump)
    #

def image_stuff():
    img = Image.open('./pic.jpg')
    pixels = img.load()
    img = img.convert("RGB")
    
    width, height = img.size

    print(f"Image Dimensions: {width}x{height}")
   
    # Correct iteration: j is the row (y), i is the column (x)
    for j in range(height):  # Iterate through rows (y-coordinate)
        for i in range(width): # Iterate through columns (x-coordinate)
            r, g, b = pixels[i, j] 

            print(f"Pixel ({i}, {j}): R={r}, G={g}, B={b}")

if __name__=='__main__':
    image_stuff()
    # main()
