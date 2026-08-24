package main

import (
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

type Sensor struct {
	x                int
	y                int
	beacon_x         int
	beacon_y         int
	manhattan_radius int
	lower_reach      int
	higher_reach     int
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
		beacon_x,
		beacon_y,
		manhattan_radius,
		sensor_y - manhattan_radius,
		sensor_y + manhattan_radius,
	}
}

func NewBeacon(sensor_x, sensor_y, beacon_x, beacon_y int) Beacon {
	return Beacon{
		beacon_x,
		beacon_y,
	}
}

func parse(filename string) ([]Sensor, *Set[Beacon]) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	line_regex := regexp.MustCompile(`Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)`)

	sensors := []Sensor{}
	beacons := NewSet[Beacon]()
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	for _, line := range lines {
		matches := line_regex.FindStringSubmatch(line)
		sensor_x, _ := strconv.Atoi(matches[1])
		sensor_y, _ := strconv.Atoi(matches[2])
		beacon_x, _ := strconv.Atoi(matches[3])
		beacon_y, _ := strconv.Atoi(matches[4])

		sensors = append(sensors, NewSensor(sensor_x, sensor_y, beacon_x, beacon_y))
		beacons.add(NewBeacon(sensor_x, sensor_y, beacon_x, beacon_y))
	}

	return sensors, beacons
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

func solve(sensors []Sensor, beacons *Set[Beacon], row int) int {
	// count intersections

	intersections := []Interval{}

	for _, sensor := range sensors {
		if sensor.lower_reach <= row && row <= sensor.higher_reach {
			distance_from_sensor := abs(sensor.y - row)
			reminder_distance := sensor.manhattan_radius - distance_from_sensor

			intersections = append(intersections, Interval{
				sensor.x - reminder_distance,
				sensor.x + reminder_distance,
			})
		}
	}

	merged_intervals := merge(intersections)
	total_intersections := 0
	for _, interval := range merged_intervals {
		total_intersections += interval.end - interval.start + 1
	}

	// subtract beacons on the row `row`
	for beacon := range beacons.elements {
		if beacon.y == row {
			for _, interval := range merged_intervals {
				if interval.start <= beacon.x && beacon.x <= interval.end {
					total_intersections--
				}
			}
		}
	}

	return total_intersections
}

func solution(filename string, row int) int {
	sensors, beacons := parse(filename)
	return solve(sensors, beacons, row)
}

func main() {
	fmt.Println(solution("./example.txt", 10))      // 26
	fmt.Println(solution("./input.txt", 2_000_000)) // 4724228
}
