package main

import (
	"fmt"
	"os"
	"regexp"
	"slices"
	"strconv"
	"strings"
)

type Monkey struct {
	id             int
	items          []int
	operation      []string
	test_divisible int
	true_monkey    int
	false_monkey   int
}

func is_integer(s string) (int, bool) {
	value, err := strconv.Atoi(s)
	return value, err != nil
}

func (m *Monkey) new_worry_level(item int) int {
	operator := m.operation[1]    // + or -
	str_operand := m.operation[2] // old or a number

	value, is_numeric := is_integer(str_operand)
	var operand int
	if is_numeric {
		operand = item
	} else {
		operand = value
	}

	switch operator {
	case "+":
		return item + operand
	case "*":
		return item * operand
	default:
		panic("unknown operator")
	}
}

func create_monkey_from_str_block(blocks string, block []string) Monkey {

	block_regex := `Monkey (\d+):\n` +
		`  Starting items: (.*)\n` +
		`  Operation: new = (\w+) (\W) (\w+)\n` +
		`  Test: divisible by (\d+)\n` +
		`    If true: throw to monkey (\d+)\n` +
		`    If false: throw to monkey (\d+)`

	regex := regexp.MustCompile(block_regex)
	matches := regex.FindStringSubmatch(blocks)
	monkey_id, _ := strconv.Atoi(matches[1])

	items := []int{}
	for _, str_item := range strings.Split(matches[2], ", ") {
		item, _ := strconv.Atoi(str_item)
		items = append(items, item)
	}
	op1 := matches[3]
	op2 := matches[4]
	op3 := matches[5]
	operation := []string{op1, op2, op3}
	test_divisible, _ := strconv.Atoi(matches[6])
	true_monkey, _ := strconv.Atoi(matches[7])
	false_monkey, _ := strconv.Atoi(matches[8])

	return Monkey{
		monkey_id,
		items,
		operation,
		test_divisible,
		true_monkey,
		false_monkey,
	}
}

func parse(filename string) map[int]*Monkey {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("File error")
	}
	monkeys := make(map[int]*Monkey)
	for _, block := range strings.Split(strings.Trim(string(data), "\n"), "\n\n") {
		monkey := create_monkey_from_str_block(block, strings.Split(block, "\n"))
		monkeys[monkey.id] = &monkey
	}
	return monkeys
}

func solve(monkeys map[int]*Monkey) int {
	// scores
	monkey_inspection := make(map[int]int)
	for monkey_id := range len(monkeys) {
		monkey_inspection[monkey_id] = 0
	}

	// play
	for range 20 {

		for monkey_id := range len(monkeys) {
			monkey := monkeys[monkey_id]

			for len(monkey.items) > 0 {
				monkey_inspection[monkey_id]++
				item := monkey.items[len(monkey.items)-1]
				monkey.items = monkey.items[:len(monkey.items)-1]

				new_item := monkey.new_worry_level(item) / 3
				if new_item%monkey.test_divisible == 0 {
					m := monkeys[monkey.true_monkey]
					m.items = append(m.items, new_item)
				} else {
					m := monkeys[monkey.false_monkey]
					m.items = append(m.items, new_item)
				}
			}
		}
	}
	values := []int{}
	for _, value := range monkey_inspection {
		values = append(values, value)
	}
	slices.Sort(values)
	n := len(values)
	return values[n-1] * values[n-2]
}

func solution(filename string) int {
	monkeys := parse(filename)
	return solve(monkeys)
}

func main() {
	fmt.Println(solution("./example.txt")) // 10605
	fmt.Println(solution("./input.txt"))   // 99840
}
