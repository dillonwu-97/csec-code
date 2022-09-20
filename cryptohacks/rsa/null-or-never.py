import gmpy2
from Crypto.Util.number import bytes_to_long, long_to_bytes


n = 95341235345618011251857577682324351171197688101180707030749869409235726634345899397258784261937590128088284421816891826202978052640992678267974129629670862991769812330793126662251062120518795878693122854189330426777286315442926939843468730196970939951374889986320771714519309125434348512571864406646232154103
e = 3
c = 63476139027102349822147098087901756023488558030079225358836870725611623045683759473454129221778690683914555720975250395929721681009556415292257804239149809875424000027362678341633901036035522299395660255954384685936351041718040558055860508481512479599089561391846007771856837130233678763953257086620228436828
COUNT = 4
candidates = [*range(36,58),*range(64,91),*range(95,123)]
iter_count = 0

# Checks if number gives ciphertext
def check(val):
    global iter_count
    iter_count +=1
    if iter_count % 1000000 == 0:
        print(iter_count, val)
    num = bytes_to_long(val)
    if pow(num, 3, n) == c:
        return True
    else:
        return False

# if assume 10 characters, 18 characters * 4 bytes * 8 bits = 576 bits to check
def recurse(current, count):
    is_val = check(current + b'}')
    print(current + b'}')
    if is_val == True:
        print("Found: ", current)
        input()
        return -1
    if count == COUNT:
        return -1
    else:
        for i in candidates:
            val = current + long_to_bytes(i)
            recurse(val, count + 1)
    return -1
        

def main():
    # Definitely not brute forcable
    # flag = b'crypto{'
    # recurse(flag, 0)
    # assert(bytes_to_long(b'hello') == bytes_to_long(b'hello' + b'\x00' * 10000))
    print(bytes_to_long(b'hello'))
    print(bytes_to_long(b'hello\x00'))
    print(bytes_to_long(b'hello\x00\x00'))
    print(bytes_to_long(b'\x00'))
    # print(bytes_to_long(b'hello' + b'\x00' * 10000))
    # print(bytes_to_long(b'hello' + b'\x00' * 100))
    print(bin(bytes_to_long(b'hello\x00')), len(bin(bytes_to_long(b'hello'))) -2 )
    print("ok")

    # means that it is divisible by 2 / can be right shifted by a lot

        

    

if __name__ == '__main__':
    main()

