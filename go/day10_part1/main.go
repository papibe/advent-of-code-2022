package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

var REQ_CYCLES = map[int]bool{
	20:  true,
	60:  true,
	100: true,
	140: true,
	180: true,
	220: true,
}

const (
	NOOP = iota
	ADD
)

type Instruction struct {
	kind   int
	amount int
}

func parse(filename string) []Instruction {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("File error")
	}
	instructions := []Instruction{}
	for _, line := range strings.Split(strings.Trim(string(data), "\n"), "\n") {
		var instruction Instruction
		if strings.HasPrefix(line, "noop") {
			instruction = Instruction{NOOP, 0}
		} else {
			split_line := strings.Split(line, " ")
			amount, _ := strconv.Atoi(split_line[1])
			instruction = Instruction{ADD, amount}
		}
		instructions = append(instructions, instruction)
	}
	return instructions
}

func solve(instructions []Instruction) int {
	cycle := 1
	x_register := 1
	signal_strength := 0

	for _, instr := range instructions {
		_, measure_cycle := REQ_CYCLES[cycle]
		if measure_cycle {
			signal_strength += cycle * x_register
		}

		if instr.kind == NOOP {
			cycle++
			continue
		}

		cycle++
		_, measure_cycle = REQ_CYCLES[cycle]
		if measure_cycle {
			signal_strength += cycle * x_register
		}
		x_register += instr.amount
		cycle++

	}

	return signal_strength
}

func solution(filename string) int {
	instructions := parse(filename)
	return solve(instructions)
}

func main() {
	fmt.Println(solution("./example.txt")) // 13140
	fmt.Println(solution("./input.txt"))   // 13180
}
