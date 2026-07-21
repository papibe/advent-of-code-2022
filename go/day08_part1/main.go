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
	visible_trees := NewSet[TreePosition]()

	// from north (top row)
	for col := range size {
		max_tree := trees[0][col]
		visible_trees.add(TreePosition{0, col})

		for row := range size {
			if trees[row][col] > max_tree {
				visible_trees.add(TreePosition{row, col})
				max_tree = trees[row][col]
			}
		}
	}

	// from east (right col)
	for row := range size {
		max_tree := trees[row][size-1]
		visible_trees.add(TreePosition{row, size - 1})

		for col := size - 1; col >= 0; col-- {
			if trees[row][col] > max_tree {
				visible_trees.add(TreePosition{row, col})
				max_tree = trees[row][col]
			}
		}
	}

	// from south (bottom row)
	for col := range size {
		max_tree := trees[size-1][col]
		visible_trees.add(TreePosition{size - 1, col})

		for row := size - 1; row >= 0; row-- {
			if trees[row][col] > max_tree {
				visible_trees.add(TreePosition{row, col})
				max_tree = trees[row][col]
			}
		}
	}

	// from west (left row)
	for row := range size {
		max_tree := trees[row][0]
		visible_trees.add(TreePosition{row, 0})

		for col := range size {
			if trees[row][col] > max_tree {
				visible_trees.add(TreePosition{row, col})
				max_tree = trees[row][col]
			}
		}
	}

	return visible_trees.len()
}

func solution(filename string) int {
	trees := parse(filename)
	return solve(trees)
}

func main() {
	fmt.Println(solution("./example.txt")) // 21
	fmt.Println(solution("./input.txt"))   // 1835
}
