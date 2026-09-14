package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Point struct {
	x float32
	y float32
	z float32
}

func parse(filename string) []Point {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	points := []Point{}
	for _, line := range lines {
		str_coords := strings.Split(line, ",")
		x, _ := strconv.Atoi(str_coords[0])
		y, _ := strconv.Atoi(str_coords[1])
		z, _ := strconv.Atoi(str_coords[2])
		points = append(points, Point{float32(x), float32(y), float32(z)})
	}

	return points
}

func neighbors(p Point) []Point {
	return []Point{
		{p.x, p.y - 0.5, p.z},
		{p.x, p.y + 0.5, p.z},
		{p.x - 0.5, p.y, p.z},
		{p.x + 0.5, p.y, p.z},
		{p.x, p.y, p.z - 0.5},
		{p.x, p.y, p.z + 0.5},
	}
}

func solve(cubes []Point) int {
	surfaces := NewSet[Point]()

	for _, cube := range cubes {
		for _, neighbor := range neighbors(cube) {
			if surfaces.contains(neighbor) {
				surfaces.remove(neighbor)
			} else {
				surfaces.add(neighbor)
			}
		}
	}

	return surfaces.len()
}

func solution(filename string) int {
	cubes := parse(filename)
	return solve(cubes)
}

func main() {
	fmt.Println(solution("./example1.txt")) // 10
	fmt.Println(solution("./example2.txt")) // 64
	fmt.Println(solution("./input.txt"))    // 3326
}
