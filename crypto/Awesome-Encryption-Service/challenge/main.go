package main

import (
	"bufio"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"fmt"
	"os"
	"strconv"
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

func encrypt(input []byte, cipher cipher.Block, nonceCounter []byte) []byte {
	return []byte{}
}

func main() {
	flag, err := os.ReadFile("./flag.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println("Hello and welcome to our secure service")
	fmt.Println("What is your request ?")
	fmt.Println("[1] Encrypt Text ")
	fmt.Println("[2] Get encrypted secret")
	counterNonce, cipher, err := initAes()
	var i int
	_, err = fmt.Scanf("%d", &i)
	if err != nil {
		panic(err)
	}
	if i == 1 {
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("Enter text: ")
		text, _ := reader.ReadString('\n')
		cipherResult := encrypt([]byte(text), cipher, counterNonce)
		fmt.Println(cipherResult)
	} else if i == 2 {
		cipherResult := encrypt(flag, cipher, counterNonce)
		fmt.Println(cipherResult)
	} else {
		panic("Go Away !!")
	}

}
