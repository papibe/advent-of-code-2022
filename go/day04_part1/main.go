package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type SectionAssignment struct {
	start int
	end   int
}

type Assignments struct {
	first  SectionAssignment
	second SectionAssignment
}

func (sa SectionAssignment) is_contained(other SectionAssignment) bool {
	return sa.start <= other.start && other.end <= sa.end
}

func parse(filename string) []Assignments {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	assignments := []Assignments{}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	for _, line := range lines {
		sections := strings.Split(line, ",")
		first_pair := strings.Split(sections[0], "-")
		second_pair := strings.Split(sections[1], "-")

		first_pair_start, _ := strconv.Atoi(first_pair[0])
		first_pair_end, _ := strconv.Atoi(first_pair[1])
		second_pair_start, _ := strconv.Atoi(second_pair[0])
		second_pair_end, _ := strconv.Atoi(second_pair[1])

		assignments = append(
			assignments,
			Assignments{
				SectionAssignment{first_pair_start, first_pair_end},
				SectionAssignment{second_pair_start, second_pair_end},
			},
		)
	}
	return assignments
}

func solve(assignments []Assignments) int {
	fully_contained := 0

	for _, assignment := range assignments {
		first_section, second_section := assignment.first, assignment.second

		if first_section.is_contained(second_section) ||
			second_section.is_contained(first_section) {

			fully_contained++
		}
	}

	return fully_contained
}

func solution(filename string) int {
	assignments := parse(filename)
	return solve(assignments)
}

func main() {
	fmt.Println(solution("./example.txt")) // 2
	fmt.Println(solution("./input.txt"))   // 477
}
