package main

import (
	"fmt"
	"math"
	"os"
	"sort"
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

type StateKey struct {
	rock_index    int
	wind_index    int
	chamber_state string
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

func (c *Chamber) trim() string {
	upper_limit := c.size + 1
	start := Coord{upper_limit, 0}
	queue := NewQueue[Coord]()
	queue.append(start)
	visited := NewSet[Coord]()
	visited.add(start)

	new_chamber := NewSet[Coord]()
	min_row := math.MaxInt

	for !queue.is_empty() {
		coord := queue.popleft()
		if c.chamber.contains(coord) {
			new_chamber.add(coord)
			continue
		}

		for _, step := range []Coord{{-1, 0}, {1, 0}, {0, 1}, {0, -1}} {
			new_row := coord.row + step.row
			new_col := coord.col + step.col

			if 0 < new_row && new_row <= upper_limit && 0 <= new_col && new_col < c.width {
				new_coord := Coord{new_row, new_col}
				if !visited.contains(new_coord) {
					queue.append(new_coord)
					visited.add(new_coord)
					min_row = min(min_row, new_row)
				}
			}

		}
	}
	c.chamber = new_chamber

	points := []Coord{}
	for _, coord := range new_chamber.list_of_elements() {
		points = append(points, Coord{coord.row - min_row, coord.col})
	}

	sort.Slice(points, func(i, j int) bool {
		if points[i].row == points[j].row {
			return points[i].col < points[j].col
		}
		return points[i].row < points[j].row
	})

	state_list := []string{}
	for _, point := range points {
		state_list = append(state_list, fmt.Sprintf("(%d,%d)", point.row, point.col))
	}
	state := strings.Join(state_list, "")
	return state
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

	seen_state := make(map[StateKey]Coord)
	min_chamber_state_size := math.MaxInt
	max_chamber_state_size := math.MinInt

	gas_index := 0
	rock_index := 0
	var state_key StateKey

	current_number_of_rocks := 0
	for current_number_of_rocks < number_of_rocks {
		rock := rocks[rock_index]
		chamber.add_falling_rock(rock)
		rock_index = (rock_index + 1) % len(rocks)

		for !chamber.is_stable() {
			wind := string(wind_data[gas_index])
			chamber.gas_push(wind)
			chamber.fall_down()
			gas_index = (gas_index + 1) % len(wind_data)

		}

		chamber_state := chamber.trim()
		min_chamber_state_size = min(min_chamber_state_size, len(chamber_state))
		max_chamber_state_size = max(max_chamber_state_size, len(chamber_state))
		state_key = StateKey{rock_index, gas_index, chamber_state}

		_, has_been_seen := seen_state[state_key]
		if has_been_seen {
			break
		}

		seen_state[state_key] = Coord{current_number_of_rocks, chamber.size}
		current_number_of_rocks++
	}

	current_state := seen_state[state_key]
	previous_number_of_rocks, previous_chamber_size := current_state.row, current_state.col
	times := (number_of_rocks - current_number_of_rocks) / (current_number_of_rocks - previous_number_of_rocks)
	rocks_piles := (current_number_of_rocks - previous_number_of_rocks) * times
	size_reached := (chamber.size - previous_chamber_size) * times
	reminding_rocks := number_of_rocks - rocks_piles - current_number_of_rocks - 1

	current_number_of_rocks = 0
	for current_number_of_rocks < reminding_rocks {
		rock := rocks[rock_index]
		chamber.add_falling_rock(rock)
		rock_index = (rock_index + 1) % len(rocks)

		for !chamber.is_stable() {
			wind := string(wind_data[gas_index])
			chamber.gas_push(wind)
			chamber.fall_down()
			gas_index = (gas_index + 1) % len(wind_data)
		}
		current_number_of_rocks++
	}

	return chamber.size + size_reached
}

func solution(filename string, number_of_rocks int) int {
	wind_data := parse(filename)
	rocks := get_rocks(ROCKS)
	chamber := NewChamber(7)

	return solve(wind_data, chamber, rocks, number_of_rocks)
}

func main() {
	fmt.Println(solution("./example.txt", 1_000_000_000_000)) // 1514285714288
	fmt.Println(solution("./input.txt", 1_000_000_000_000))   // 1560932944615
}
