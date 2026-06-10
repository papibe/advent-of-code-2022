package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parse(filename string) [][]int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	elf_calories := [][]int{}
	group_calories := strings.Split(strings.Trim(string(data), "\n"), "\n\n")

	for _, str_elf_calories := range group_calories {
		str_calories := strings.Split(str_elf_calories, "\n")
		calories := []int{}
		for _, str_calorie := range str_calories {
			calorie, _ := strconv.Atoi(str_calorie)
			calories = append(calories, calorie)
		}
		elf_calories = append(elf_calories, calories)
	}

	return elf_calories
}

func solve(elf_calories [][]int) int {
	max_calories := 0

	for _, calories := range elf_calories {
		total_elf_calories := 0
		for _, calorie := range calories {
			total_elf_calories += calorie
		}
		max_calories = max(max_calories, total_elf_calories)
	}

	return max_calories
}

func solution(filename string) int {
	elf_calories := parse(filename)
	return solve(elf_calories)
}

func main() {
	fmt.Println(solution("./example.txt")) // 24000
	fmt.Println(solution("./input.txt"))   // 67633
}
