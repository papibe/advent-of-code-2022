package main

import (
	"fmt"
	"maps"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Blueprint = map[string]map[string]int
type Blueprints = map[int]Blueprint
type Spend = map[string]int
type Spends = map[int]Spend
type Robots = map[string]int
type Resources = map[string]int

type State struct {
	minute          int
	geode_robots    int
	obsidian_robots int
	clay_robots     int
	ore_robots      int

	geode_resources    int
	obsidian_resources int
	clay_resources     int
	ore_resources      int
}

type QueueItem struct {
	minutes   int
	robots    Robots
	resources Resources
}

func parse(filename string) (Spends, Blueprints) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	bp_re := regexp.MustCompile(`Blueprint (\d+):`)
	ore_re := regexp.MustCompile(`Each ore robot costs (\d+) ore\.`)
	clay_re := regexp.MustCompile(`Each clay robot costs (\d+) ore\.`)
	obsidian_re := regexp.MustCompile(`Each obsidian robot costs (\d+) ore and (\d+) clay`)
	geode_re := regexp.MustCompile(`Each geode robot costs (\d+) ore and (\d+) obsidian`)

	blueprints := make(Blueprints)
	max_spend := make(Spends)

	for _, line := range lines {
		matches := bp_re.FindStringSubmatch(line)
		blue_print_number, _ := strconv.Atoi(matches[1])

		matches = ore_re.FindStringSubmatch(line)
		ore_ore, _ := strconv.Atoi(matches[1])

		matches = clay_re.FindStringSubmatch(line)
		clay_ore, _ := strconv.Atoi(matches[1])

		matches = obsidian_re.FindStringSubmatch(line)
		obsidian_ore, _ := strconv.Atoi(matches[1])
		obsidian_clay, _ := strconv.Atoi(matches[2])

		matches = geode_re.FindStringSubmatch(line)
		geode_ore, _ := strconv.Atoi(matches[1])
		geode_obsidian, _ := strconv.Atoi(matches[2])

		blueprints[blue_print_number] = Blueprint{
			"geode":    {"ore": geode_ore, "obsidian": geode_obsidian},
			"obsidian": {"ore": obsidian_ore, "clay": obsidian_clay},
			"clay":     {"ore": clay_ore},
			"ore":      {"ore": ore_ore},
		}

		max_spend[blue_print_number] = Spend{
			"obsidian": geode_obsidian,
			"clay":     obsidian_clay,
			"ore":      max(ore_ore, clay_ore, obsidian_ore, geode_ore),
			"geode":    25,
		}
	}
	return max_spend, blueprints
}

func normalize_and_shrink(max_spend Spend, robots *Robots, resources *Resources, minute int) {
	for resource, amount := range *robots {
		if amount >= max_spend[resource] {
			(*robots)[resource] = max_spend[resource]
			(*resources)[resource] = min((*resources)[resource], max_spend[resource])
		}
	}

	for resource, amount := range *resources {
		(*resources)[resource] = min(amount, minute*max_spend[resource]-(*robots)[resource]*(minute-1))
	}

}

func bfs(blue_print Blueprint, max_spend Spend, initial_robots Robots, initial_resources Resources, minute int) int {
	// BFS setup
	queue := NewQueue[QueueItem]()
	queue.append(QueueItem{minute, initial_robots, initial_resources})

	visited := NewSet[State]()
	max_geodes := 0
	saves := 0

	// BFS
	for !queue.is_empty() {
		state := queue.popleft()
		minute, robots, resources := state.minutes, state.robots, state.resources

		if minute == 0 {
			max_geodes = max(max_geodes, resources["geode"])
			continue
		}
		normalize_and_shrink(max_spend, &robots, &resources, minute)

		// memoization
		key := State{
			minute,
			robots["geode"],
			robots["obsidian"],
			robots["clay"],
			robots["ore"],
			resources["geode"],
			resources["obsidian"],
			resources["clay"],
			resources["ore"],
		}
		if visited.contains(key) {
			saves++
			continue
		}

		visited.add(key)

		new_resources := maps.Clone(resources)

		// produce
		for robot, amount := range robots {
			new_resources[robot] += amount
		}

		new_resources_backup := maps.Clone(new_resources)

		queue.append(QueueItem{minute - 1, robots, new_resources})

		// Check if we can build
		for resource, cost := range blue_print {
			if robots[resource] >= max_spend[resource] {
				continue
			}
			can_build := true
			for element, quantity := range cost {
				if resources[element] < quantity {
					can_build = false
					break
				}
			}
			if can_build {
				next_resources := maps.Clone(new_resources_backup)

				// buy
				for element, quantity := range cost {
					next_resources[element] -= quantity
				}

				// build
				next_robots := maps.Clone(robots)
				next_robots[resource] = next_robots[resource] + 1

				queue.append(QueueItem{minute - 1, next_robots, next_resources})
			}
		}
	}
	return max_geodes
}

func solve(max_spend Spends, blue_prints Blueprints, working_minutes int) int {
	total_quality_level := 0
	robots := Robots{"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
	start_resources := Resources{"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}

	for bp_number, blue_print := range blue_prints {
		quality_level := bfs(
			blue_print,
			max_spend[bp_number],
			robots,
			start_resources,
			working_minutes,
		)
		total_quality_level += quality_level * bp_number
	}

	return total_quality_level
}

func solution(filename string, working_minutes int) int {
	max_spend, blue_prints := parse(filename)
	return solve(max_spend, blue_prints, working_minutes)
}

func main() {
	fmt.Println(solution("./example.txt", 24)) // 33
	fmt.Println(solution("./input.txt", 24))   // 1294
}
