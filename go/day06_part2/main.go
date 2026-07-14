package main

import (
	"fmt"
	"os"
	"strings"
)

func parse(filename string) string {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	return strings.Trim(string(data), "\n")
}

func solve(datastream string, packet_size int) int {
	start := 0
	current := 0
	current_packet_size := 0
	seen_at := make(map[byte]int)

	for current < len(datastream) && current_packet_size < packet_size {
		char := datastream[current]

		position, char_is_seen := seen_at[char]
		if char_is_seen {
			// re setting start position and cleaning seen_at's
			new_start := position + 1
			for i := start; i < new_start; i++ {
				delete(seen_at, datastream[i])
			}
			start = new_start
			current_packet_size = current - start
		}
		seen_at[char] = current
		current_packet_size++

		current++
	}
	return current
}

func solution(filename string, packet_size int) int {
	datastream := parse(filename)
	return solve(datastream, packet_size)
}

func main() {
	fmt.Println(solution("./input.txt", 14)) // 2122
}
