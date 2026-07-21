package main

import (
	"fmt"
	"os"
	"strings"
)

type Trees [][]int

type TreePosition struct {
	row int
	col int
}

func parse(filename string) Trees {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("File error")
	}
	trees := Trees{}

	for _, line := range strings.Split(strings.Trim(string(data), "\n"), "\n") {
		row := []int{}
		for _, str_value := range line {
			value := str_value - '0'
			row = append(row, int(value))
		}
		trees = append(trees, row)
	}
	return trees
}

func solve(trees Trees) int {
	size := len(trees)
	max_scenic_score := 0

	for current_row := 1; current_row <= size-1; current_row++ {
		for current_col := 1; current_col <= size-1; current_col++ {
			height := trees[current_row][current_col]

			// up
			ss_up := 0
			for row := current_row - 1; row >= 0; row-- {
				ss_up++
				if trees[row][current_col] >= height {
					break
				}
			}

			// right
			ss_right := 0
			for col := current_col + 1; col < size; col++ {
				ss_right++
				if trees[current_row][col] >= height {
					break
				}
			}

			// down
			ss_down := 0
			for row := current_row + 1; row < size; row++ {
				ss_down++
				if trees[row][current_col] >= height {
					break
				}
			}

			// left
			ss_left := 0
			for col := current_col - 1; col >= 0; col-- {
				ss_left++
				if trees[current_row][col] >= height {
					break
				}
			}
			current_score := ss_up * ss_right * ss_down * ss_left
			max_scenic_score = max(max_scenic_score, current_score)
		}
	}

	return max_scenic_score
}

func solution(filename string) int {
	trees := parse(filename)
	return solve(trees)
}

func main() {
	fmt.Println(solution("./example.txt")) // 8
	fmt.Println(solution("./input.txt"))   // 263670
}
