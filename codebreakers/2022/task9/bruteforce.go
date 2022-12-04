/*
To Run: Must run in directory with an existing table
*/

package main

import (
    "bufio"
    "bytes"
    "crypto/aes"
    "crypto/cipher"
    "encoding/hex"
    "fmt"
    "os"
    "os/exec"
    "strings"
)

// Files
const KEYLOG = "/home/cloudian/Desktop/csec-code/codebreakers/2022/task8/keygeneration.log"
const KEYMASTER = "/home/cloudian/Desktop/csec-code/codebreakers/2022/task8/keyMaster"
const ALLKEYS = "/home/cloudian/Desktop/csec-code/codebreakers/2022/task8/allkeys.txt"
const CIPHERTEXT = "/home/cloudian/Desktop/csec-code/codebreakers/2022/task9/important_data.pdf.enc"
const TEMP = "/home/cloudian/Desktop/csec-code/codebreakers/2022/task9/temp/"
const NEWKEYS = "/home/cloudian/Desktop/csec-code/codebreakers/2022/task9/temp/newkeys.txt"

// globals
var ciphertext, errc = os.ReadFile(CIPHERTEXT)
var iv, errv = hex.DecodeString(string(ciphertext[:32]))
var newkeyf, errf = os.OpenFile(NEWKEYS, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

func fatal(err error) {
    if err != nil {
        panic(err)
    }
}

// Get lock input values for a given path
// Returns an array of strings
func get_lock_input(path string) []string {

    ret := []string{}
    file, err := os.Open(KEYLOG)
    fatal(err)
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        ret = append(ret, scanner.Text())
    }

    return ret

}

func get_val_from_key(s string, key string) string {
    s_arr := strings.Fields(s)
    switch key {
        case "date":
            return s_arr[0]
        case "name":
            return s_arr[1]
        case "cid":
            return s_arr[2]
        case "demand":
            return s_arr[3]
        default:
            return "error"
    }
}

// Get plaintext key for a given input
func get_pt_key(input string) []byte {
    date := get_val_from_key(input, "date")
    name := get_val_from_key(input, "name")
    cid := get_val_from_key(input, "cid")
    demand := get_val_from_key(input, "demand")

    // Creating bg process to execute
    to_run := "sudo date --set " + date + " && "
    to_run += KEYMASTER + " lock " + cid + " " + demand + " " + name

    fmt.Printf("Command is: %s\n", to_run)

    pt_key, err := exec.Command("/bin/bash", "-c", to_run).Output()
    fatal(err)
    return pt_key
}

func recurse_key(k string, start int) {
    end := start + 2

    // for each combination of hex values
    for i:= 0; i <= 0xff; i++ {
        h := fmt.Sprintf("%02x", i)
        new_key := k[:start] + h + k[end:]

        // base case
        if start == 21 {
            if len(new_key) != 32 {
                panic("Bad key created")
            }
            fmt.Println(new_key)
            try_unlock(new_key)
            newkeyf.Write([]byte(new_key + "\n"))
        } else if start == 6 {
            recurse_key (new_key, 19) // 19 is start of fourth section
        } else {
            recurse_key (new_key, start + 2)
        }
    }
}

// Construct other key candidate using a given key
func construct_more_keys(k string) {

    // Need to create variations based on the key
    // First and fourth section of the key changes
    recurse_key(k, 2)
}

// Try to unlock using the given plaintext key
func try_unlock(k string) {
    // Using the key, try to decrypt the pdf block in cbc mode
    key := []byte(k)

    block, err := aes.NewCipher(key)
    fatal(err)

    mode := cipher.NewCBCDecrypter(block, iv)
    plaintext_candidate := make([]byte, len(ciphertext))
    mode.CryptBlocks(plaintext_candidate, ciphertext)

    // Check for pdf header
    fmt.Println(plaintext_candidate[:4])
    PDF_HEADER := []byte{0x25, 0x50, 0x44, 0x46}
    if bytes.Compare(plaintext_candidate, PDF_HEADER) == 0 {
        fmt.Printf("Found something! %s\n", k)
        bufio.NewReader(os.Stdin).ReadBytes('\n')
    }
}

func main() {

    all_keys := []string{}
    // Perform the operations if file of keys doesn't exist
    if _, err := os.Stat(ALLKEYS); os.IsNotExist(err) {
        f, err := os.OpenFile(ALLKEYS, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
        defer f.Close()
        fatal(err)

        log_arr := get_lock_input(KEYLOG)
        for _, val := range(log_arr) {
            if get_val_from_key(val, "name") == "ImpossibleCouch" {
                pt_key := get_pt_key(val)
                all_keys = append(all_keys, string(pt_key))
                fmt.Println(string(pt_key))
                f.Write(pt_key)
                fatal(err)
            }
        }

    // Otherwise just read from the file
    } else {
        f, err := os.Open(ALLKEYS)
        defer f.Close()
        fatal(err)

        scanner := bufio.NewScanner(f)
        for scanner.Scan() {
            if strings.Contains(scanner.Text(), "plainKey") {
                all_keys = append(all_keys, scanner.Text())
                fmt.Println("line: ", scanner.Text())
            }
        }
    }

    // I now have all of the keys that I need
    for i, val := range(all_keys) {
        new_val := strings.Split(strings.Split(val, "plainKey\":\"")[1], "\",\"result")[0]
        all_keys[i] = new_val
    }
    fmt.Println(all_keys)

    // Iterate through each key in order to try decryption
    ciphertext = ciphertext[32:]
    for _, k := range(all_keys) {
        construct_more_keys(k)
    }
}
