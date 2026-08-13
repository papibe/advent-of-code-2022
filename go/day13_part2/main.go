package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

type Packet struct {
	str   string
	value any
}

func NewPacket(str string) Packet {
	var packet any

	err := json.Unmarshal([]byte(str), &packet)
	if err != nil {
		log.Fatalf("Error unmarshaling JSON: %v", err)
	}
	return Packet{str, packet}

}

func parse(filename string) []Packet {
	data_raw, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	data := strings.Split(strings.Trim(string(data_raw), "\n"), "\n\n")

	packets := []Packet{}

	for _, pair := range data {
		var left_package any
		var right_package any

		split_line := strings.Split(pair, "\n")
		left_err := json.Unmarshal([]byte(split_line[0]), &left_package)
		right_err := json.Unmarshal([]byte(split_line[1]), &right_package)

		if left_err != nil || right_err != nil {
			log.Fatalf("Error unmarshaling JSON: %v", err)
		}

		packets = append(packets, NewPacket(split_line[0]))
		packets = append(packets, NewPacket(split_line[1]))
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

func solve(packages []Packet) int {
	first_packet := NewPacket("[[2]]")
	second_packet := NewPacket("[[6]]")

	packages = append(packages, first_packet)
	packages = append(packages, second_packet)

	sort.Slice(packages, func(i, j int) bool {
		return is_right_order(packages[i].value, packages[j].value)
	})

	var divider_2_index int
	var divider_6_index int
	for index, packet := range packages {
		if packet.str == first_packet.str {
			divider_2_index = index + 1
		} else if packet.str == second_packet.str {
			divider_6_index = index + 1
		}
	}

	return divider_2_index * divider_6_index
}

func solution(filename string) int {
	packages := parse(filename)
	return solve(packages)
}

func main() {
	fmt.Println(solution("./example.txt")) // 140
	fmt.Println(solution("./input.txt"))   // 21691
}
