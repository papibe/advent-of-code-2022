package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Instruction struct {
	source      rune
	destination rune
	quantity    int
}

type Stack map[rune][]rune

func parse(filename string) (Stack, []Instruction) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	blocks := strings.Split(strings.Trim(string(data), "\n"), "\n\n")
	stack_lines := strings.Split(blocks[0], "\n")
	instructions_data := blocks[1]

	number_of_rows := len(stack_lines)
	stacks_line := stack_lines[number_of_rows-1]
	stacks := make(Stack)

	re_stack := regexp.MustCompile(`\d`)

	for _, indexes := range re_stack.FindAllStringIndex(stacks_line, -1) {
		start := indexes[0]
		stack_id := rune(stacks_line[start])

		stack_content := []rune{}
		for row := number_of_rows - 2; row >= 0; row-- {
			if stack_lines[row][start] != ' ' {
				stack_content = append(stack_content, rune(stack_lines[row][start]))
			}
		}
		stacks[stack_id] = stack_content
	}

	instructions := []Instruction{}
	re_instr := regexp.MustCompile(`move (\d+) from (\d+) to (\d+)`)

	for _, line := range strings.Split(instructions_data, "\n") {
		match := re_instr.FindStringSubmatch(line)
		number_of_creates, _ := strconv.Atoi(match[1])
		source_stack := rune(match[2][0])
		destination_stack := rune(match[3][0])

		instructions = append(instructions, Instruction{source_stack, destination_stack, number_of_creates})
	}

	return stacks, instructions
}

func solve(stacks Stack, instructions []Instruction) string {
	for _, instr := range instructions {
		for range instr.quantity {
			// pop create from source
			create := stacks[instr.source][len(stacks[instr.source])-1]
			stacks[instr.source] = stacks[instr.source][:len(stacks[instr.source])-1]

			// add create to destination
			stacks[instr.destination] = append(stacks[instr.destination], create)
		}
	}

	message := []rune{}
	for i := 1; i <= len(stacks); i++ {
		stack_id := rune('0' + i)
		message = append(message, stacks[rune(stack_id)][len(stacks[rune(stack_id)])-1])
	}

	return string(message)
}

func solution(filename string) string {
	stacks, instructions := parse(filename)
	return solve(stacks, instructions)
}

func main() {
	fmt.Println(solution("./example.txt")) // "CMZ"
	fmt.Println(solution("./input.txt"))   // "MQTPGLLDN"
}
