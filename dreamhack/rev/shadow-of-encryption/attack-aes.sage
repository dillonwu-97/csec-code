
# https://crypto.stackexchange.com/questions/89596/linear-aes-expression-of-k-in-aesp-apk/89607#89607
# Implementation based on

# ripped from the medium blog post code
def bytes2mat(b):
    a = []
    for i in b:
        tmp = bin(i)[2:].zfill(8)
        for j in tmp:
            a.append(int(j))
    return Matrix(GF(2), a)

def mat2bytes(m):
    a = ""
    for i in range(128):
        a += str(m[0, i])
    a = [a[i:i+8] for i in range(0, 128, 8)]
    a = [int(i, 2) for i in a]
    return bytes(a)
def main():
    id_mat = identity_matrix(GF(2), 8, 8)
    zero_mat = Matrix(GF(2), 8, 8)

    # constructing x matrix
    x_mat = Matrix(GF(2), 8, 8)
    for i in range(7):
        x_mat[i, i+1] = 1
    x_mat[3,0] = 1
    x_mat[4,0] = 1
    x_mat[6,0] = 1
    x_mat[7,0] = 1
    X = x_mat
    I = id_mat
    Z = zero_mat

    # block matrix is used for shift / column mixing operations 
    C = block_matrix([
        [X, X+I, I, I],
        [I, X, X+I, I],
        [I, I, X, X+I],
        [X+I, I, I, X]
    ])

    sigma0 = block_matrix([
        [I, Z, Z, Z],
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
    ])
    sigma1 = block_matrix([
        [Z, Z, Z, Z],
        [Z, I, Z, Z],
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
    ])
    sigma2 = block_matrix([
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
        [Z, Z, I, Z],
        [Z, Z, Z, Z],
    ])
    sigma3 = block_matrix([
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
        [Z, Z, Z, I],
    ])
    zero_block = block_matrix([
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
        [Z, Z, Z, Z],
    ])
    ZB = zero_block 
    B0 = sigma0
    B1 = sigma1
    B2 = sigma2
    B3 = sigma3

    # shift matrix
    S = block_matrix([
        [B0, B1, B2, B3],
        [B3, B0, B1, B2],
        [B2, B3, B0, B1],
        [B1, B2, B3, B0],
    ])

    M = block_matrix([
        [C, ZB, ZB, ZB],
        [ZB, C, ZB, ZB],
        [ZB, ZB, C, ZB],
        [ZB, ZB, ZB, C],
    ])
    R = M*S
    A = S * (R**9)
    print(A.dimensions())
    # C = ciphertext, 
    # P = plaintext
    png_hex = "89504E470D0A1A0A0000000D49484452"
    png_header = b''.join([bytes.fromhex(png_hex[i:i+2]) for i in range(0, len(png_hex), 2)])
    print(png_header)
    assert len(png_header) == 16
    P = bytes2mat(png_header).transpose()

    f = open('./censored.png.enc', 'rb').read()
    censored_blocks = [f[i:i+16] for i in range(0,len(f), 16)]
    print(censored_blocks[0])
    for i in censored_blocks:
        assert len(i) == 16
    png_cipher = censored_blocks[0]
    C = bytes2mat(png_cipher).transpose()
    K = C - A*P

    print(len(censored_blocks))
    # solve the rest
    f = open('./dec_png', 'wb')
    f.write(png_header)
    for i,v in enumerate(censored_blocks):
        if i == 0: 
            continue
        print(i)
        C = bytes2mat(v).transpose()
        temp = C - K
        temp2 = A.inverse() * temp
        pt = mat2bytes(temp2.transpose())
        print("pt: ", pt)
        f.write(pt)
    f.close()
    
if __name__ == '__main__':
    main()
    # flag: DH{wh4t_1s_AES_?}
