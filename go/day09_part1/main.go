package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Plank struct {
	x int
	y int
}

type Instruction struct {
	direction rune
	amount    int
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func sign(n int) int {
	if n < 0 {
		return -1
	}
	if n > 0 {
		return 1
	}
	return 0
}

func (p *Plank) move(direction rune) {
	switch direction {
	case 'R':
		p.x += 1
	case 'U':
		p.y += 1
	case 'L':
		p.x -= 1
	case 'D':
		p.y -= 1
	default:
		panic("Unknown direction")
	}
}

func (p *Plank) follow(head Plank) {
	x_diff := head.x - p.x
	y_diff := head.y - p.y

	x_abs := abs(x_diff)
	y_abs := abs(y_diff)

	if x_abs <= 1 && y_abs <= 1 {
		return
	} else if x_abs == 2 && y_abs == 0 {
		p.x += sign(x_diff)
	} else if y_abs == 2 && x_abs == 0 {
		p.y += sign(y_diff)
	} else if x_abs == 2 && y_abs == 1 {
		p.x += sign(x_diff)
		p.y = head.y
	} else if y_abs == 2 && x_abs == 1 {
		p.x = head.x
		p.y += sign(y_diff)
	} else {
		panic("Unable to move")
	}
}

func parse(filename string) []Instruction {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("File error")
	}
	instructions := []Instruction{}

	for _, line := range strings.Split(strings.Trim(string(data), "\n"), "\n") {
		split_line := strings.Split(line, " ")
		direction := rune(split_line[0][0])
		amount, _ := strconv.Atoi(split_line[1])
		instructions = append(instructions, Instruction{direction, amount})
	}
	return instructions
}

func solve(instructions []Instruction) int {
	head := Plank{0, 0}
	tail := Plank{0, 0}
	visited := NewSet[Plank]()
	visited.add(head)

	for _, instr := range instructions {
		for range instr.amount {
			head.move(instr.direction)
			tail.follow(head)
			visited.add(tail)
		}
	}
	return visited.len()
}

func solution(filename string) int {
	instructions := parse(filename)
	return solve(instructions)
}

func main() {
	fmt.Println(solution("./example1.txt")) // 13
	fmt.Println(solution("./input.txt"))    // 5619
}
