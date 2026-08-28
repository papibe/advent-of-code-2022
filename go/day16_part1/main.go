package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type AdjacencyMatrix = [][]int
type Flows = map[string]int
type ValveIndex = map[string]int

type State struct {
	minutes int
	valve   int
	opened  int
}

func parse(filename string) (AdjacencyMatrix, ValveIndex, Flows) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")
	line_regex := regexp.MustCompile(`Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)`)

	flows := make(ValveIndex)
	tunnels := make(map[string][]string)
	valve_indexes := make(ValveIndex)
	index := 0

	for _, line := range lines {
		matches := line_regex.FindStringSubmatch(line)
		valve := matches[1]
		flow, _ := strconv.Atoi(matches[2])
		valves := []string{}
		for _, v := range strings.Split(matches[3], ", ") {
			valves = append(valves, v)
		}
		flows[valve] = flow
		tunnels[valve] = valves
		valve_indexes[valve] = index
		index++
	}
	n := len(flows)
	adjacency_matrix := make(AdjacencyMatrix, n)
	for i := range n {
		adjacency_row := make([]int, n)
		for j := range n {
			// adjacency_row[j] = math.MaxInt
			adjacency_row[j] = 1_000 // high enough value
		}
		adjacency_matrix[i] = adjacency_row
	}

	for valve_name, neighbors := range tunnels {
		valve_index := valve_indexes[valve_name]
		for _, neighbor := range neighbors {
			nb_index := valve_indexes[neighbor]

			adjacency_matrix[valve_index][nb_index] = 1
			adjacency_matrix[valve_index][valve_index] = 0
		}
	}

	return adjacency_matrix, valve_indexes, flows
}

func floyd_warshall(adjacency_matrix AdjacencyMatrix) {
	n := len(adjacency_matrix)

	for k := range n {
		for i := range n {
			for j := range n {
				adjacency_matrix[i][j] = min(
					adjacency_matrix[i][j],
					adjacency_matrix[i][k]+adjacency_matrix[k][j],
				)
			}
		}
	}
}

func compress_graph(am AdjacencyMatrix, valve_index ValveIndex, flows Flows) (AdjacencyMatrix, ValveIndex, Flows) {
	valves_with_flow := make(map[string]int)
	new_valve_index := make(map[string]int)
	valves_with_flow["AA"] = 0
	new_valve_index["AA"] = 0

	index := 1
	for valve, flow := range flows {
		if flow > 0 {
			valves_with_flow[valve] = flow
			new_valve_index[valve] = index
			index++
		}
	}

	n := len(valves_with_flow)
	adjacency_matrix := make(AdjacencyMatrix, n)
	for i := range n {
		adjacency_matrix[i] = make([]int, n)
	}

	for valve_name := range valves_with_flow {
		for connecting_valve := range valves_with_flow {
			adjacency_matrix[new_valve_index[valve_name]][new_valve_index[connecting_valve]] = am[valve_index[valve_name]][valve_index[connecting_valve]]
		}
	}

	return adjacency_matrix, new_valve_index, valves_with_flow
}

func solve(
	adjacency_matrix AdjacencyMatrix,
	flows []int,
	valve_indexes ValveIndex,
	opened int,
	memo map[State]int,
	max_minutes int,
) int {

	var dfs func(int, int, int) int

	dfs = func(minutes, valve, opened int) int {
		if minutes == 0 {
			return 0
		}
		state := State{minutes, valve, opened}
		cached_value, seen := memo[state]
		if seen {
			return cached_value
		}
		max_pressure := 0
		for neighbor := range len(adjacency_matrix[valve]) {
			if neighbor == valve {
				continue
			}
			distance := adjacency_matrix[valve][neighbor]
			if distance <= minutes-1 {
				neighbor_bit := 1 << neighbor
				if opened&neighbor_bit == 0 { // not opened
					max_pressure = max(
						max_pressure,
						flows[neighbor]*(minutes-distance-1)+
							dfs(minutes-distance-1, neighbor, opened|neighbor_bit),
					)
				}

			}
		}
		memo[state] = max_pressure
		return max_pressure
	}
	aa_index := valve_indexes["AA"]

	return dfs(max_minutes, aa_index, opened<<aa_index)
}

func solution(filename string) int {
	adjacency_matrix, valve_index, flows := parse(filename)

	floyd_warshall(adjacency_matrix)

	adjacency_matrix, new_valve_index, valves_with_flow := compress_graph(
		adjacency_matrix, valve_index, flows,
	)

	memo := make(map[State]int)
	new_flows := make([]int, len(valves_with_flow))
	for valve_name, valve_index := range new_valve_index {
		new_flows[valve_index] = flows[valve_name]
	}

	return solve(adjacency_matrix, new_flows, new_valve_index, 0, memo, 30)
}

func main() {
	fmt.Println(solution("./example.txt")) // 24000
	fmt.Println(solution("./input.txt"))   // 67633
}
