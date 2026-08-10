package main

import (
	"fmt"
	"os"
	"strings"
)

const START = 'E'
const END = 'a'

type Grid [][]rune

type Position struct {
	row int
	col int
}

type QueueItem struct {
	pos   Position
	steps int
}

func parse(filename string) (Grid, Position) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("File error")
	}
	grid := [][]rune{}
	for _, line := range strings.Split(strings.Trim(string(data), "\n"), "\n") {
		grid = append(grid, []rune(line))
	}
	// find start and end:
	rows := len(grid)
	cols := len(grid[0])
	var start Position
	for row := range rows {
		for col := range cols {
			switch grid[row][col] {
			case START:
				start = Position{row, col}
			default:
			}
		}
	}
	// patch start and end
	grid[start.row][start.col] = 'z'

	return grid, start
}

func solve(grid Grid, start Position) int {
	// BFS init
	rows := len(grid)
	cols := len(grid[0])
	queue := NewQueue[QueueItem]()
	queue.append(QueueItem{start, 0})

	visited := NewSet[Position]()
	visited.add(start)

	// BFS traverse
	for queue.len() > 0 {
		state := queue.popleft()
		if grid[state.pos.row][state.pos.col] == END {
			return state.steps
		}

		for _, jump := range []Position{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
			new_pos := Position{state.pos.row + jump.row, state.pos.col + jump.col}
			// been here before
			if visited.contains(new_pos) {
				continue
			}
			// check if inside the grid range
			if new_pos.row < 0 || new_pos.row >= rows ||
				new_pos.col < 0 || new_pos.col >= cols {
				continue
			}
			// only one up max
			if grid[state.pos.row][state.pos.col]-grid[new_pos.row][new_pos.col] > 1 {
				continue
			}
			queue.append(QueueItem{new_pos, state.steps + 1})
			visited.add(new_pos)
		}
	}

	return -1
}

func solution(filename string) int {
	grid, start := parse(filename)
	return solve(grid, start)
}

func main() {
	fmt.Println(solution("./example.txt")) // 29
	fmt.Println(solution("./input.txt"))   // 418
}
