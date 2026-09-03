package main

import (
	"fmt"
	"math"
	"os"
	"strings"
)

var ROCKS = [][][]string{
	{
		{"@", "@", "@", "@"},
	},
	{
		{".", "@", "."},
		{"@", "@", "@"},
		{".", "@", "."},
	},
	{
		{"@", "@", "@"},
		{".", ".", "@"},
		{".", ".", "@"},
	},
	{
		{"@"},
		{"@"},
		{"@"},
		{"@"},
	},
	{
		{"@", "@"},
		{"@", "@"},
	},
}

type Coord struct {
	row int
	col int
}

type Chamber struct {
	chamber        *Set[Coord]
	width          int
	size           int
	size_with_rock int
	stable         bool
	rock           *Set[Coord]
}

func NewChamber(width int) *Chamber {
	return &Chamber{
		NewSet[Coord](),
		width,
		0,
		0,
		true,
		NewSet[Coord](),
	}
}

func (c *Chamber) add_falling_rock(rock []Coord) {
	rock_row := c.size + 4
	rock_col := 2
	c.size_with_rock += 4 + 4

	for _, coord := range rock {
		c.rock.add(Coord{rock_row + coord.row, rock_col + coord.col})
	}
	c.stable = false
}

func (c *Chamber) move_left() {
	new_rock_position := NewSet[Coord]()

	for coord := range c.rock.elements {
		new_coord := Coord{coord.row, coord.col - 1}
		if coord.col-1 < 0 || c.chamber.contains(new_coord) {
			return
		}
		new_rock_position.add(new_coord)
	}
	c.rock = new_rock_position
}

func (c *Chamber) move_right() {
	new_rock_position := NewSet[Coord]()

	for coord := range c.rock.elements {
		new_coord := Coord{coord.row, coord.col + 1}
		if coord.col+1 >= c.width || c.chamber.contains(new_coord) {
			return
		}
		new_rock_position.add(new_coord)
	}
	c.rock = new_rock_position
}

func (c *Chamber) gas_push(wind string) {
	switch wind {
	case "<":
		c.move_left()
	case ">":
		c.move_right()
	default:
		fmt.Println("->", wind, "<-")
		panic("Unknown wind direction")
	}
}

func (c *Chamber) fall_down() {
	new_rock_position := NewSet[Coord]()

	for coord := range c.rock.elements {
		new_coord := Coord{coord.row - 1, coord.col}
		if coord.row-1 < 1 || c.chamber.contains(new_coord) {
			c.stabilize()
			return
		}
		new_rock_position.add(new_coord)
	}
	c.rock = new_rock_position
}

func (c *Chamber) stabilize() {
	max_row := math.MinInt

	for coord := range c.rock.elements {
		max_row = max(max_row, coord.row)
		c.chamber.add(coord)
	}
	c.rock = NewSet[Coord]()
	c.size = max(c.size, max_row)
	c.size_with_rock = max_row
	c.stable = true
}

func (c *Chamber) is_stable() bool {
	return c.stable
}

func get_rocks(rocks [][][]string) [][]Coord {
	coord_rocks := [][]Coord{}

	for _, rock := range rocks {
		rock_coords := []Coord{}
		for i, line := range rock {
			for j, value := range line {
				if value == "@" {
					rock_coords = append(rock_coords, Coord{i, j})
				}
			}
		}
		coord_rocks = append(coord_rocks, rock_coords)
	}
	return coord_rocks
}

func parse(filename string) string {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	return strings.Trim(string(data), "\n")
}

func solve(wind_data string, chamber *Chamber, rocks [][]Coord, number_of_rocks int) int {
	gas_index := 0
	rock_index := 0

	for range number_of_rocks {
		rock := rocks[rock_index]
		chamber.add_falling_rock(rock)
		rock_index = (rock_index + 1) % len(rocks)

		for !chamber.is_stable() {
			wind := string(wind_data[gas_index])
			chamber.gas_push(wind)
			chamber.fall_down()
			gas_index = (gas_index + 1) % len(wind_data)

		}
	}

	return chamber.size
}

func solution(filename string, number_of_rocks int) int {
	wind_data := parse(filename)
	rocks := get_rocks(ROCKS)
	chamber := NewChamber(7)

	return solve(wind_data, chamber, rocks, number_of_rocks)
}

func main() {
	fmt.Println(solution("./example.txt", 2022)) // 3068
	fmt.Println(solution("./input.txt", 2022))   // 3163
}
