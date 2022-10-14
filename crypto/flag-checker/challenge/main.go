package main

import (
	"bufio"
	"bytes"
	b64 "encoding/base64"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

func validate_first(flag string) bool {
	if len(flag) != 50 {
		return false
	}
	var key []string
	for i := len(flag) - 1; i >= 0; i = i - 2 {
		var temp []string
		for j := 0; j < int(flag[i]); j++ {
			var b bytes.Buffer
			b.WriteString(strconv.Itoa(int(rune(rand.Intn(9)))))
			temp = append(temp, b.String())
		}
		key = append(key, strings.Join(temp, "t7")+"t7")
	}
	loookupTable := []int{118, 88, 312, 164, 525, 672, 721, 352, 405, 1100, 1254, 1128, 1274, 1288, 1635, 1488, 748, 738, 1672, 2020, 1680, 2200, 2070, 2256, 2575}

	for i := 1; i <= len(loookupTable); i++ {
		if len(key[i-1]) != ((3 * (loookupTable[i-1] + 7*i)) / i) {
			return false
		}
	}
	return true
}

func validate_last(flag string) bool {
	lookup_map := make(map[int]string)
	var index []int
	for i := 0; i < len(flag)/2; i = i + 2 {
		lookup_map[i] = string(flag[i]) + string(flag[i+(len(flag)/2)-1])
		index = append(index, i)
	}
	var temp []string
	for _, k := range index {
		temp = append(temp, lookup_map[k]+strconv.Itoa(k))
	}
	fmt.Println(temp)
	secret := "SXQwLmd2Mi5IXzQuYzA2LntfOC4zcjEwLmxfMTIuZDAxNC5uXzE2Ll9yMTguZW0yMC5ldDIyLnRkMjQ="
	b64Enc := b64.StdEncoding.EncodeToString([]byte(strings.Join(temp, ".")))
	fmt.Println(b64Enc)
	if b64Enc != secret {
		return false
	}
	return true
}

func main() {
	fmt.Println("Enter the flag : ")
	reader := bufio.NewReader(os.Stdin)
	flag, err := reader.ReadString('\n')
	flag = strings.Trim(flag, " \n")
	if err != nil {
		fmt.Println(err)
	}
	is_valid := validate_first(flag) && validate_last(flag)
	if is_valid {
		fmt.Println("Congratulations you got your flag")
	}
}
