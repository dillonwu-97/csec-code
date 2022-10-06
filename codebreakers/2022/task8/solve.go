package main

import (
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"fmt"

	"golang.org/x/crypto/pbkdf2"
)

func main() {

	// Handling password
	salt_str := "UTVZH4QDSHy9S3rP/iuFMYCyZAPVizaeUcWA7NU3NeM="
	salt, _ := base64.StdEncoding.DecodeString(salt_str)
	fmt.Println("Password is ", salt)
	if len(salt) != 0x20 {
		panic(-1)
	}

	xor_str := "74da5fae94d4871897e587cb0a685a"

	// password_str := "74da5fae94d4871897e587cb0a685a" + "74da5fae94d4871897e587cb0a685a" + "74da5fae94d4871897e587cb0a685a" + "74da5fae94d4871897e587cb0a685a" + "74da5fae94d4871897e587cb0a685a" + "74da5fae94d4871897e587cb0a"

	password_str := "30922acbac92d142cdcad6b160056a17ab06fba7add062f191e2fb382d6e1aee31d4d59bd47efed3e6834e1d7546bb69e7ac83b15ad397cae47c293f35bd2cddceb3c16ac490c89346242c5fb61b9ec49fde60f2a9e0f637"

	password, _ := hex.DecodeString(password_str)
	xor, _ := hex.DecodeString(xor_str)
	fmt.Println("password is: ", password)
	fmt.Println("Xor is: ", xor)

	password_encoded := base64.StdEncoding.EncodeToString(xor)
	fmt.Println("password encoded is: ", password_encoded)

	for i := 0; i < len(password); i++ {
		password[i] ^= xor[i%15]
	}
	fmt.Println("After xor ^ password is: ", password)

	if len(password) != 0x58 {
		panic(-1)
	}

	iter := 0x1000
	keyLen := 0x20

	k_candidate := pbkdf2.Key(password, salt, iter, keyLen, sha256.New)
	fmt.Println("Result is: ", k_candidate)
	b64_encoded_c := base64.StdEncoding.EncodeToString(k_candidate)

	fmt.Println("sha256 key candidate is: ", b64_encoded_c)

    // 0QW1marERVzPvFYAi2qimnzxd3iGhvgHxnvAr68inHE=

	/* Did not work
	       Nd+QcUcRgDZ4A+nSMN0zDJPM8yg2wUsrAsWOztfOJNU= (password, password, 32, sha256)
	       p+kS61QYKUIqglXYJBD3pWL+BNlvZyRCireIvT91M6k= (password, password, 32, sha512)

	       4BXSsddL+f+r4M/kYnW3MkkRemGRTGkxyoga7U9Vn/E= (password, password, 32, sha256)
	       ba7ymYmzoHlFOONs2oyWDjOZtoyISlyzvO/q4NzGF6c= (password, password, 32, sha512)

	       4BXSsddL+f+r4M/kYnW3Mg== (password, password, 16, sha256)
	       ba7ymYmzoHlFOONs2oyWDg== (password, password, 16, sha256)

	   // using just 0x15 array repeated multiple times
	       rkpan5AcdJL2EW0L1/N2+BE5IYHBnAgalYLuRM8TIBc=

	       // xor 0x58 array with 0x15 array
	   AyDFdYlOAzdzZBBxmqnIqDy+1npF+irIh1ojh24M/rc=

	   // no xor with 0x58 array
	   ZxYEPc+vHvLc7k8IYl/+XvI0Ab5ZwYqJwpYE7nQge7k=

	   // encoded password post xor
	   REh1ZThGVlpaL1F6am0wY3FZVTN5V3pmdGUwMkU0bjRuekFPU2ZpNmFIRHUvMmE2SThXNkJEck0vdkFlQWdzc1pnRnJTdU9YTEx2K2xEMFBLWXhlTGc9PQ==

	   // encoded password pre xor
	   MJIqy6yS0ULNytaxYAVqF6sG+6et0GLxkeL7OC1uGu4x1NWb1H7+0+aDTh11Rrtp56yDsVrTl8rkfCk/Nb0s3c6zwWrEkMiTRiQsX7YbnsSf3mDyqeD2Nw==

	   // encoded xor
	   dNpfrpTUhxiX5YfLCmha
	*/
}
