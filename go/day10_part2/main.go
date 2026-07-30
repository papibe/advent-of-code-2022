package main

import (
	"fmt"
	"os"
	"slices"
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

const DISPLAY_LEN = 40

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

func solve(instructions []Instruction) string {
	cycle := 1
	sprite := 1 // former register

	display := slices.Repeat([]rune{' '}, 240)
	display_position := 1

	for _, instr := range instructions {
		display_position = (cycle - 1) % DISPLAY_LEN
		if sprite-1 <= display_position && display_position <= sprite+1 {
			display[cycle-1] = '#'
		} else {
			display[cycle-1] = '.'
		}

		if instr.kind == NOOP {
			cycle++
			continue
		}

		cycle++
		display_position = (cycle - 1) % DISPLAY_LEN
		if sprite-1 <= display_position && display_position <= sprite+1 {
			display[cycle-1] = '#'
		} else {
			display[cycle-1] = '.'
		}
		sprite += instr.amount
		cycle++

	}

	// generate output string
	output := []rune{}
	for index, bit := range display {
		if index%DISPLAY_LEN == 0 {
			output = append(output, '\n')
		}
		output = append(output, bit)
	}

	return string(output)
}

func solution(filename string) string {
	instructions := parse(filename)
	return solve(instructions)
}

func main() {
	fmt.Println(solution("./example.txt")) // see day 10 README
	fmt.Println(solution("./input.txt"))   // EZFCHJAB
}
