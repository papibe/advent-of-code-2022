package main

import (
	"fmt"
	"math"
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

func neighbor_surfaces(p Point) []Point {
	return []Point{
		{p.x, p.y - 0.5, p.z},
		{p.x, p.y + 0.5, p.z},
		{p.x - 0.5, p.y, p.z},
		{p.x + 0.5, p.y, p.z},
		{p.x, p.y, p.z - 0.5},
		{p.x, p.y, p.z + 0.5},
	}
}

func neighbor_points(p Point) []Point {
	return []Point{
		{p.x, p.y - 1, p.z},
		{p.x, p.y + 1, p.z},
		{p.x - 1, p.y, p.z},
		{p.x + 1, p.y, p.z},
		{p.x, p.y, p.z - 1},
		{p.x, p.y, p.z + 1},
	}
}

func solve(cubes []Point) int {
	surfaces := NewSet[Point]()
	cubes_set := NewSet[Point]()
	for _, cube := range cubes {
		cubes_set.add(cube)
	}

	min_x := float32(math.MaxFloat32)
	min_y := float32(math.MaxFloat32)
	min_z := float32(math.MaxFloat32)

	max_x := -min_x
	max_y := -min_y
	max_z := -min_z

	for _, cube := range cubes {
		min_x = min(min_x, cube.x)
		min_y = min(min_y, cube.y)
		min_z = min(min_z, cube.z)
		max_x = max(max_x, cube.x)
		max_y = max(max_y, cube.y)
		max_z = max(max_z, cube.z)

		for _, neighbor := range neighbor_surfaces(cube) {
			if surfaces.contains(neighbor) {
				surfaces.remove(neighbor)
			} else {
				surfaces.add(neighbor)
			}
		}
	}

	// adjust limits
	min_x -= 1
	min_y -= 1
	min_z -= 1
	max_x += 1
	max_y += 1
	max_z += 1

	// BFS setup
	start := Point{min_x, min_y, min_z}
	queue := NewQueue[Point]()
	queue.append(start)
	visited := NewSet[Point]()
	visited.add(start)

	air := NewSet[Point]()

	// BFS
	for !queue.is_empty() {
		point := queue.popleft()

		if cubes_set.contains(point) {
			continue
		}
		air.add(point)

		for _, n := range neighbor_points(point) {
			if min_x <= n.x && n.x <= max_x &&
				min_y <= n.y && n.y <= max_y &&
				min_z <= n.z && n.z <= max_z {

				if !visited.contains(n) {
					queue.append(n)
					visited.add(n)
				}
			}
		}

	}

	external_surface := NewSet[Point]()
	for cube := range air.elements {
		for _, n := range neighbor_surfaces(cube) {
			if surfaces.contains(n) {
				external_surface.add(n)
			}
		}
	}

	return external_surface.len()
}

func solution(filename string) int {
	cubes := parse(filename)
	return solve(cubes)
}

func main() {
	fmt.Println(solution("./example2.txt")) // 58
	fmt.Println(solution("./input.txt"))    // 1996
}
