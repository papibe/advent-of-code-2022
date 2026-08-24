package main

import (
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

const MULTIPLIER = 4_000_000

type Sensor struct {
	x                int
	y                int
	manhattan_radius int
}

type Beacon struct {
	x int
	y int
}

type Interval struct {
	start int
	end   int
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func NewSensor(sensor_x, sensor_y, beacon_x, beacon_y int) Sensor {
	manhattan_radius := abs(beacon_x-sensor_x) + abs(sensor_y-beacon_y)
	return Sensor{
		sensor_x,
		sensor_y,
		manhattan_radius,
	}
}

func NewBeacon(sensor_x, sensor_y, beacon_x, beacon_y int) Beacon {
	return Beacon{
		beacon_x,
		beacon_y,
	}
}

func parse(filename string) []Sensor {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	line_regex := regexp.MustCompile(`Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)`)

	sensors := []Sensor{}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	for _, line := range lines {
		matches := line_regex.FindStringSubmatch(line)
		sensor_x, _ := strconv.Atoi(matches[1])
		sensor_y, _ := strconv.Atoi(matches[2])
		beacon_x, _ := strconv.Atoi(matches[3])
		beacon_y, _ := strconv.Atoi(matches[4])

		sensors = append(sensors, NewSensor(sensor_x, sensor_y, beacon_x, beacon_y))
	}

	return sensors
}

func merge(intervals []Interval) []Interval {
	sort.Slice(intervals, func(i, j int) bool {
		return intervals[i].start < intervals[j].start
	})

	merged_intervals := []Interval{intervals[0]}
	for i := 1; i < len(intervals); i++ {
		last := len(merged_intervals) - 1
		if intervals[i].start <= merged_intervals[last].end {
			merged_intervals[last].start = min(merged_intervals[last].start, intervals[i].start)
			merged_intervals[last].end = max(merged_intervals[last].end, intervals[i].end)
		} else {
			merged_intervals = append(merged_intervals, intervals[i])
		}
	}
	return merged_intervals
}

func solve(sensors []Sensor, row int) int {
	// count intersections

	adjacent_sensors := [][]Sensor{}
	n := len(sensors)

	for i := range n {
		for j := i + 1; j < n; j++ {
			s1 := sensors[i]
			s2 := sensors[j]
			distance := abs(s1.x-s2.x) + abs(s1.y-s2.y)
			if distance == (s1.manhattan_radius + s2.manhattan_radius + 2) {
				adjacent_sensors = append(adjacent_sensors, []Sensor{s1, s2})
			}
		}
	}
	// input has only 2 pairs, however example has multiple matching pairs
	adjacent_sensors = adjacent_sensors[:2]

	var left Sensor
	var right Sensor
	var sign int

	coords := [][]int{}

	for _, pair := range adjacent_sensors {
		s1 := pair[0]
		s2 := pair[1]

		if s1.x < s2.x {
			left = s1
			right = s2
		} else {
			left = s2
			right = s1
		}

		var x int
		var y int
		if left.y > right.y {
			x, y = left.x, left.y-left.manhattan_radius-1
			sign = -1
		} else {
			x, y = left.x, left.y+left.manhattan_radius+1
			sign = 1
		}
		coords = append(coords, []int{x, y, sign})
	}

	x1, y1, sign1 := coords[0][0], coords[0][1], coords[0][2]
	x2, y2, sign2 := coords[1][0], coords[1][1], coords[1][2]

	x := (x1 + sign1*y1 + x2 + sign2*y2) / 2
	y := -(x1 + sign1*y1 - x2 - sign2*y2) / 2

	return (MULTIPLIER * x) + y
}

func solution(filename string, row int) int {
	sensors := parse(filename)
	return solve(sensors, row)
}

func main() {
	fmt.Println(solution("./example.txt", 10))      // 26
	fmt.Println(solution("./input.txt", 2_000_000)) // 4724228
}
