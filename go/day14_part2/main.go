package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

const (
	ROCK = '#'
	AIR  = '\x00'
	SAND = '+'
	REST = 'o'
)

type Coord struct {
	x int
	y int
}

func parse(filename string) ([][]rune, int, int) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	max_x := 0
	max_y := 0
	min_x := math.MaxInt
	min_y := math.MaxInt

	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")
	scan := [][]Coord{}

	for _, line := range lines {
		path := []Coord{}
		for _, str_pair := range strings.Split(line, " -> ") {
			str_coord := strings.Split(str_pair, ",")
			x, _ := strconv.Atoi(str_coord[0])
			y, _ := strconv.Atoi(str_coord[1])

			max_x = max(max_x, x)
			max_y = max(max_y, y)
			min_x = min(min_x, x)
			min_y = min(min_y, y)

			path = append(path, Coord{x, y})
		}
		scan = append(scan, path)
	}

	// part 2 addition
	max_y += 2
	min_x = min(min_x, 500-max_y-1)
	max_x = max(max_x, 500+max_y+1)

	rows := max_y + 1
	cols := max_x - min_x + 1

	cave := make([][]rune, rows)
	for i := range rows {
		cave[i] = make([]rune, cols)
	}

	for _, path := range scan {
		for index := 1; index < len(path); index++ {
			origin := path[index-1]
			destination := path[index]

			path_min_x := min(origin.x, destination.x)
			path_min_y := min(origin.y, destination.y)
			path_max_x := max(origin.x, destination.x)
			path_max_y := max(origin.y, destination.y)

			for x := path_min_x; x <= path_max_x; x++ {
				for y := path_min_y; y <= path_max_y; y++ {
					cave[y][x-min_x] = ROCK
				}
			}
		}
	}
	// add floor for part 2
	for col := range cols {
		cave[rows-1][col] = ROCK
	}

	return cave, 0, 500 - min_x
}

func solve(cave [][]rune, sand_start_row, sand_start_col int) int {
	rows := len(cave)
	cols := len(cave[0])

	mins := make([]int, cols)
	for i := range cols {
		mins[i] = math.MaxInt
	}

	for col := range cols {
		for row := range rows {
			if cave[row][col] == ROCK {
				mins[col] = min(mins[col], row)
			}
		}
	}

	rest_counter := 0
	for {
		// drop sand at start
		sand_row := sand_start_row
		sand_col := sand_start_col
		cave[sand_row][sand_col] = SAND

		// falling down
		for {
			// try down
			if sand_row+1 >= rows {
				return rest_counter
			}
			if cave[sand_row+1][sand_col] == AIR {
				new_sand_row := max(sand_row+1, mins[sand_col]-1)
				cave[sand_row][sand_col] = AIR
				cave[new_sand_row][sand_col] = SAND
				sand_row = new_sand_row
				continue
			}

			// try left down
			if sand_row+1 >= rows || sand_col-1 < 0 || sand_col-1 >= cols {
				return rest_counter
			}
			if cave[sand_row+1][sand_col-1] == AIR {
				cave[sand_row][sand_col] = AIR
				cave[sand_row+1][sand_col-1] = SAND
				sand_row++
				sand_col--
				continue
			}

			// try right down
			if sand_row+1 >= rows || sand_col+1 < 0 || sand_col+1 >= cols {
				return rest_counter
			}
			if cave[sand_row+1][sand_col+1] == AIR {
				cave[sand_row][sand_col] = AIR
				cave[sand_row+1][sand_col+1] = SAND
				sand_row++
				sand_col++
				continue
			}

			// at rest
			rest_counter++
			cave[sand_row][sand_col] = REST
			mins[sand_col] = min(mins[sand_col], sand_row)

			if sand_row == sand_start_row && sand_col == sand_start_col {
				return rest_counter
			}

			break
		}
	}

	return -1
}

func solution(filename string) int {
	cave, sand_row, sand_col := parse(filename)
	return solve(cave, sand_row, sand_col)
}

func main() {
	fmt.Println(solution("./example.txt")) // 93
	fmt.Println(solution("./input.txt"))   // 26683
}
