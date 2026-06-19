package main

import (
	"fmt"
	"os"
	"strings"
)

func parse(filename string) []string {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	return strings.Split(strings.Trim(string(data), "\n"), "\n")
}

func NewSetFromString(s string) *Set[rune] {
	set := NewSet[rune]()
	for _, char := range s {
		set.add(char)
	}
	return set
}

func solve(rucksacks []string) int {
	priority_sum := 0

	for _, rucksack := range rucksacks {
		compartment_1 := NewSetFromString(rucksack[0 : len(rucksack)/2])
		compartment_2 := NewSetFromString(rucksack[len(rucksack)/2:])

		compartment_union := compartment_1.intersection(compartment_2)

		for _, item := range compartment_union.list_of_elements() {
			if 'a' <= item && item <= 'z' {
				priority_sum += int(item) - 'a' + 1
			} else {
				priority_sum += int(item) - 'A' + 27
			}
		}
	}

	return priority_sum
}

func solution(filename string) int {
	rucksacks := parse(filename)
	return solve(rucksacks)
}

func main() {
	fmt.Println(solution("./example.txt")) // 157
	fmt.Println(solution("./input.txt"))   // 8515
}
