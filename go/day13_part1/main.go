package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"os"
	"strings"
)

type Packages struct {
	left  any
	right any
}

func parse(filename string) []Packages {
	data_raw, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	data := strings.Split(strings.Trim(string(data_raw), "\n"), "\n\n")

	packets := []Packages{}

	for _, pair := range data {
		var left_package any
		var right_package any

		split_line := strings.Split(pair, "\n")
		left_err := json.Unmarshal([]byte(split_line[0]), &left_package)
		right_err := json.Unmarshal([]byte(split_line[1]), &right_package)

		if left_err != nil || right_err != nil {
			log.Fatalf("Error unmarshaling JSON: %v", err)
		}

		packets = append(packets, Packages{left_package, right_package})
	}

	return packets
}

func is_map(data any) (map[string]any, bool) {
	data_map, ok := data.(map[string]any)
	return data_map, ok
}

func is_list(data any) ([]any, bool) {
	data_list, ok := data.([]any)
	return data_list, ok
}

func is_int(data any) (float64, bool) {
	value, ok := data.(float64)
	return value, ok
}

func _is_right_order(left any, right any) (bool, error) {
	left_list, left_is_list := is_list(left)
	right_list, right_is_list := is_list(right)

	if left_is_list && right_is_list {
		index := 0

		for {
			if index >= len(left_list) && index >= len(right_list) {
				return false, errors.New("not comparable at this point")
			}
			if index >= len(left_list) {
				return true, nil
			}
			if index >= len(right_list) {
				return false, nil
			}
			result, err := _is_right_order(left_list[index], right_list[index])
			if err == nil {
				return result, nil
			}
			index++
		}
	}
	left_value, left_is_int := is_int(left)
	right_value, right_is_int := is_int(right)

	if left_is_int && right_is_int {
		if left_value < right_value {
			return true, nil
		} else if left_value > right_value {
			return false, nil
		} else {
			return false, errors.New("not comparable at this point")
		}
	}
	if left_is_int {
		return _is_right_order([]any{left}, right)
	}
	if right_is_int {
		return _is_right_order(left, []any{right})
	}

	return false, errors.New("not comparable at this point")
}

func is_right_order(left any, right any) bool {
	result, err := _is_right_order(left, right)
	if err != nil {
		panic("comparison failed!")
	}
	return result
}

func solve(packages []Packages) int {
	right_order_indexes := []int{}

	for i, pair := range packages {
		if is_right_order(pair.left, pair.right) {
			right_order_indexes = append(right_order_indexes, i+1)
		}
	}

	sum_of_indexes := 0
	for _, index := range right_order_indexes {
		sum_of_indexes += index
	}

	return sum_of_indexes
}

func solution(filename string) int {
	packages := parse(filename)
	return solve(packages)
}

func main() {
	fmt.Println(solution("./example.txt")) // 13
	fmt.Println(solution("./input.txt"))   // 5905
}
