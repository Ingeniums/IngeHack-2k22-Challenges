package main

import (
	"bufio"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	hex "encoding/hex"
	"fmt"
	"os"
	"strconv"
	"strings"

	padding "github.com/andreburgaud/crypt2go/padding"
)

func initAes() ([]byte, cipher.Block, error) {
	key := make([]byte, 16)
	rand.Read(key)
	cipher, err := aes.NewCipher(key)
	if err != nil {
		return nil, nil, err
	}
	counter := []byte(strconv.Itoa(128))
	nonce := make([]byte, 13)
	rand.Read(nonce)
	nonceCounter := append(nonce, counter...)
	return nonceCounter, cipher, nil
}

func encrypt(input []byte, block cipher.Block, nonceCounter []byte) []byte {
	padded_input := make([]byte, 16)
	padder := padding.NewPkcs7Padding(16)
	padded_input, _ = padder.Pad(input)
	temp := make([]byte, 16)
	mode := cipher.NewCBCEncrypter(block, []byte{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0})
	mode.CryptBlocks(temp, nonceCounter)
	fmt.Println(nonceCounter)
	result := make([]byte, 16)
	for i := 0; i < 16; i++ {
		result[i] = temp[i] ^ padded_input[i]
	}
	return result
}

func main() {
	flag, err := os.ReadFile("./flag.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println("Hello and welcome to our secure service")
	counterNonce, cipher, err := initAes()
	for true {
		fmt.Println("What is your request ?")
		fmt.Println("[1] Encrypt Text ")
		fmt.Println("[2] Get encrypted secret")
		var i int
		_, err = fmt.Scanf("%d", &i)
		if err != nil {
			panic(err)
		}
		if i == 1 {
			reader := bufio.NewReader(os.Stdin)
			fmt.Print("Enter text (length <= 16): ")
			text, _ := reader.ReadString('\n')
			strimmed_text := strings.TrimSuffix(text, "\n")
			if len(strimmed_text) > 16 {
				panic("Text length invalid")
			}
			cipherResult := encrypt([]byte(text), cipher, counterNonce)
			hexResult := hex.EncodeToString(cipherResult)
			fmt.Println(hexResult)
		} else if i == 2 {
			cipherResult := encrypt(flag, cipher, counterNonce)
			hexResult := hex.EncodeToString(cipherResult)
			fmt.Println(hexResult)
		} else {
			panic("Go Away !!")
		}
	}
}
