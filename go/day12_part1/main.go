package main

import (
	"fmt"
	"os"
	"strings"
)

const START = 'S'
const END = 'E'

type Grid [][]rune

type Position struct {
	row int
	col int
}

type QueueItem struct {
	pos   Position
	steps int
}

func parse(filename string) (Grid, Position, Position) {
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
	var end Position
	for row := range rows {
		for col := range cols {
			switch grid[row][col] {
			case START:
				start = Position{row, col}
			case END:
				end = Position{row, col}
			default:
			}
		}
	}
	// patch start and end
	grid[start.row][start.col] = 'a'
	grid[end.row][end.col] = 'z'

	return grid, start, end
}

func solve(grid Grid, start, end Position) int {
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
		if state.pos == end {
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
			if grid[new_pos.row][new_pos.col]-grid[state.pos.row][state.pos.col] > 1 {
				continue
			}
			queue.append(QueueItem{new_pos, state.steps + 1})
			visited.add(new_pos)
		}
	}

	return -1
}

func solution(filename string) int {
	grid, start, end := parse(filename)
	return solve(grid, start, end)
}

func main() {
	fmt.Println(solution("./example.txt")) // 31
	fmt.Println(solution("./input.txt"))   // 425
}
