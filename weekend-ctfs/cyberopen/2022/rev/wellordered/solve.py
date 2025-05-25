# Current order
# Find nth


def meta_prog():
    f = open('./checks.txt').read()
    s = ''
    count = 0
    for l in f.split('\n'):
        if "before" in l:
            h1 = l.split("hex_val1: ")[1].split(",")[0]
            h2 = l.split("hex_val2: ")[1].split(",")[0]
            c1 = l.split("pos?: ")[1].split(",")[0]
            c2 = l.split("pos?: ")[2].split(")")[0]
            s += "if fn (f(" + h1 + "), " + c1 + ") > fn(f(" + h2 + ")," + c2 + "):\n"
            s += "  print(\"Error" + str(count) + "\")\n"
            count += 1

    print(s)
    return s

# a = [ 0x6d, 0x34, 0x6b, 0x33, 0x5f, 0x33, 0x5f, 0x79, 0x30, 0x75, 0x35, 0x32, 0x30, 0x65, 0x72, 0x30, 0x6c, 0x55, 0x31, 0x33, 0x5f, 0x5f, 0x46, 0x33, 0x31]
# m4k3_R5Ur3_y_l1F3_1s_iN_00rud3R_a8c520d3ee
s = 'm4k3_5Ur3_y0uR_l1F3_1s_iN_0rd3R_a8c520d3ee'

a = [0x6d, 0x34, 0x6b, 0x33, 0x5f, 0x35, 0x55, 0x72, 0x33, 0x5f, 0x79, 0x30, 0x52,0x75, 0x5f, 0x6c, 0x31, 0x46, 0x33, 0x5f, 0x31, 0x73, 0x5f, 0x69, 0x4e, 0x5f, 0x30, 0x72, 0x64, 0x33, 0x52, 0x5f, 0x61, 0x38, 0x63, 0x35, 0x32, 0x30, 0x65, 0x65]
print(a)
s = ''.join([chr(i) for i in a])
print(len(s))
# assert(len(s) == 0x28)
def fn(needle, n):
    start = s.find(needle)
    while start >= 0 and n > 0:
        start = s.find(needle, start+len(needle))
        n -= 1
    return start

f = lambda x: chr(x)

def solve():
  if fn (f(0x6d), 0) > fn(f(0x34),0):
    print("Error0")
  if fn (f(0x33), 1) > fn(f(0x5f),1):
    print("Error1")
  if fn (f(0x35), 1) > fn(f(0x32),0):
    print("Error2")
  if fn (f(0x46), 0) > fn(f(0x33),2):
    print("Error3")
  if fn (f(0x5f), 3) > fn(f(0x31),1):
    print("Error4")
  if fn (f(0x33), 2) > fn(f(0x5f),3):
    print("Error5")
  if fn (f(0x5f), 0) > fn(f(0x35),0):
    print("Error6")
  if fn (f(0x79), 0) > fn(f(0x30),0):
    print("Error7")
  if fn (f(0x30), 2) > fn(f(0x65),0):
    print("Error8")
  if fn (f(0x52), 0) > fn(f(0x5f),2):
    print("Error9")
  if fn (f(0x72), 0) > fn(f(0x33),1):
    print("Error10")
  if fn (f(0x63), 0) > fn(f(0x35),1):
    print("Error11")
  if fn (f(0x73), 0) > fn(f(0x5f),4):
    print("Error12")
  if fn (f(0x6b), 0) > fn(f(0x33),0):
    print("Error13")
  if fn (f(0x61), 0) > fn(f(0x38),0):
    print("Error14")
  if fn (f(0x4e), 0) > fn(f(0x5f),5):
    print("Error15")
  if fn (f(0x31), 0) > fn(f(0x46),0):
    print("Error16")
  if fn (f(0x5f), 1) > fn(f(0x79),0):
    print("Error17")
  if fn (f(0x38), 0) > fn(f(0x63),0):
    print("Error18")
  if fn (f(0x52), 1) > fn(f(0x5f),6):
    print("Error19")
  if fn (f(0x31), 1) > fn(f(0x73),0):
    print("Error20")
  if fn (f(0x6c), 0) > fn(f(0x31),0):
    print("Error21")
  if fn (f(0x33), 0) > fn(f(0x5f),0):
    print("Error22")
  if fn (f(0x65), 0) > fn(f(0x65),1):
    print("Error23")
  if fn (f(0x32), 0) > fn(f(0x30),2):
    print("Error24")
  if fn (f(0x30), 1) > fn(f(0x72),1):
    print("Error25")
  if fn (f(0x5f), 5) > fn(f(0x30),1):
    print("Error26")
  if fn (f(0x64), 0) > fn(f(0x33),3):
    print("Error27")
  if fn (f(0x5f), 2) > fn(f(0x6c),0):
    print("Error28")
  if fn (f(0x35), 0) > fn(f(0x55),0):
    print("Error29")
  if fn (f(0x69), 0) > fn(f(0x4e),0):
    print("Error30")
  if fn (f(0x5f), 6) > fn(f(0x61),0):
    print("Error31")
  if fn (f(0x30), 0) > fn(f(0x75),0):
    print("Error32")
  if fn (f(0x33), 3) > fn(f(0x52),1):
    print("Error33")
  if fn (f(0x34), 0) > fn(f(0x6b),0):
    print("Error34")
  if fn (f(0x5f), 4) > fn(f(0x69),0):
    print("Error35")
  if fn (f(0x55), 0) > fn(f(0x72),0):
    print("Error36")
  if fn (f(0x72), 1) > fn(f(0x64),0):
    print("Error37")
    # 82, 117
  if fn (f(0x52), 0) > fn(f(0x75),0):
    print("Error38")
  

def main():

    # meta_prog()
    '''
    if fn (f(0x6d), 0) > fn(f(0x34), 0):
        print("Error")

    
   
    x = fn(f(64), 0) 
    '''
    solve()
    print(s)

if __name__ == '__main__':
    main()
    # m4k3_5Ur3_y0uR_l1F3_1s_iN_0rd3R_a8c520ee
