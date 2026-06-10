package main

import (
	"fmt"
	"os"
	"strings"
)

const ROCK = "A"
const PAPER = "B"
const SCISSORS = "C"

// strategy translation
const LOSE = "X"
const DRAW = "Y"
const WIN = "Z"

var choice = map[string]map[string]string{
	LOSE: {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER},
	DRAW: {ROCK: ROCK, PAPER: PAPER, SCISSORS: SCISSORS},
	WIN:  {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK},
}

var strategy = map[string]string{
	"X": ROCK,
	"Y": PAPER,
	"Z": SCISSORS,
}

var play_value = map[string]int{
	ROCK:     1,
	PAPER:    2,
	SCISSORS: 3,
}

var match_result_value = map[string]map[string]int{
	ROCK:     {ROCK: 3, PAPER: 6, SCISSORS: 0},
	PAPER:    {ROCK: 0, PAPER: 3, SCISSORS: 6},
	SCISSORS: {ROCK: 6, PAPER: 0, SCISSORS: 3},
}

type Play struct {
	their_play  string
	my_strategy string
}

func parse(filename string) []Play {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	plays := []Play{}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	for _, line := range lines {
		split_line := strings.Split(line, " ")
		their_play := split_line[0]
		my_strategy := split_line[1]
		plays = append(plays, Play{their_play, my_strategy})
	}

	return plays
}

func solve(plays []Play) int {
	points := 0

	for _, play := range plays {
		my_play := choice[play.my_strategy][play.their_play]
		points += play_value[my_play] + match_result_value[play.their_play][my_play]
	}

	return points
}

func solution(filename string) int {
	plays := parse(filename)
	return solve(plays)
}

func main() {
	fmt.Println(solution("./example.txt")) // 12
	fmt.Println(solution("./input.txt"))   // 13693
}
