package main

import (
	"fmt"
	"time"

	"os/exec"

	"github.com/levigross/grequests"
)

func main() {

	ticker := time.NewTicker(1 * time.Second)
	for range ticker.C {
		if checkServerIsOk() {
			cmd := exec.Command("top")
			s, err := cmd.Output()
			if err !=nil{
				panic(err)
			}
			fmt.Println(string(s))
		}
	}

}

func checkServerIsOk() bool {
	res, err := grequests.Get("http://localhost:8000", nil)
	if err != nil || res.Error != nil {
		return false
	}
	return true
}

// CGO_ENABLED=0 go build .
