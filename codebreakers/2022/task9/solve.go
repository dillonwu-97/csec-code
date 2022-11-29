// This is the naiive way; definitely not correct, but try anyway
// Thoughts:
// What is the key encrypting key used for? What will it be applied against?
// Should try to create CBC Decrypter using the k-e-k as a first attempt
// Then try to examine the decompiled lock() program / function to see how the 
// key is generated for a victim.

// TODO: Create the encrypter and decrypter and verify that I am using the API correctly
// Do I need to use the uid?
// My intuition is that the key is generated from the uid and maybe the time unless it's not actually used except to generate the logs
// TODO: Examine the user.db and victims.db file to see what they are doing


package main

import (
    "crypto/aes"
    "crypto/cipher"
    "encoding/base64"
    "encoding/hex"
    "github.com/golang-jwt/jwt"
    "os"
)


func main() {

    pem_file, err := ioutil.ReadFile("./k.pem")

    // Get what is assumed to be the password
    password := "0QW1marERVzPvFYAi2qimnzxd3iGhvgHxnvAr68inHE="
    iv := "b783f0b2a814006f7a7931013b3f4907"

    key, err := base64.StdEncoding.DecodeString(password)
    if err != nil {
        panic(err)
    } 
    //fmt.Printf("Base64 decoded password: %x\n", key)

    // Get what is assumed to be the iv
    iv_d, err := hex.DecodeString(iv)
    if err != nil {
        panic(err)
    }
//    //fmt.Printf("Hex encoded iv %x\n", iv_d)

    // Read the ciphertext from the file
    ciphertext, err := os.ReadFile("./important_data.pdf.enc")
    if err != nil {
        panic(err)
    }
    //fmt.Println(string(ciphertext[:32]))
    // This is the data to be decrypted
    ciphertext = ciphertext[32:]
    //fmt.Println("ciphertext is: ", string(ciphertext))
    //fmt.Println("ciphertext length is: ", len(ciphertext))

    // Try creating the cipher
    block, err := aes.NewCipher(key)
    //fmt.Println("Block size is: ", aes.BlockSize)

    // Try decrypting the data
    mode := cipher.NewCBCDecrypter(block, iv_d)
    mode.CryptBlocks(ciphertext, ciphertext)

    // Try to write the file 
//    err = os.WriteFile("./decrypted.pdf", ciphertext, 0644)
//    if err != nil {
//        panic(err)
//    }
}
