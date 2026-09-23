package main

import (
	"fmt"
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
			// "geode":    math.MaxInt,
			"geode": 10_000,
		}
	}

	// fmt.Println(max_spend)
	// fmt.Println(blueprints)

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

func dfs(blue_print Blueprint, max_spend Spend, robots Robots, resources Resources, minute int) int {
	memo := make(map[State]int)
	// _ = memo

	var _dfs func(int, Robots, Resources) int

	_dfs = func(minute int, robots Robots, resources Resources) int {
		if minute == 0 {
			return resources["geode"]
		}

		// normalizing resources and robots
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
		cached_value, key_in_memo := memo[key]
		if key_in_memo {
			return cached_value
		}

		new_resources := Resources{
			"geode":    resources["geode"],
			"obsidian": resources["obsidian"],
			"clay":     resources["clay"],
			"ore":      resources["ore"],
		}

		// produce
		for robot, amount := range robots {
			new_resources[robot] += amount
		}

		new_resources_backup := Resources{
			"geode":    new_resources["geode"],
			"obsidian": new_resources["obsidian"],
			"clay":     new_resources["clay"],
			"ore":      new_resources["ore"],
		}

		max_geodes := _dfs(minute-1, robots, new_resources)

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
				next_resources := Resources{
					"geode":    new_resources_backup["geode"],
					"obsidian": new_resources_backup["obsidian"],
					"clay":     new_resources_backup["clay"],
					"ore":      new_resources_backup["ore"],
				}
				// buy
				for element, quantity := range cost {
					next_resources[element] -= quantity
				}

				// build
				new_force := Robots{
					"geode":    robots["geode"],
					"obsidian": robots["obsidian"],
					"clay":     robots["clay"],
					"ore":      robots["ore"],
				}
				new_force[resource]++

				max_geodes = max(max_geodes, _dfs(minute-1, new_force, next_resources))
			}
		}
		memo[key] = max_geodes
		return max_geodes
	}

	return _dfs(minute, robots, resources)
}

func solve(max_spend Spends, blue_prints Blueprints, working_minutes int) int {
	total_quality_level := 0
	robots := Robots{"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
	start_resources := Resources{"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}

	for bp_number, blue_print := range blue_prints {
		quality_level := dfs(
			blue_print,
			max_spend[bp_number],
			robots,
			start_resources,
			working_minutes,
		)
		// fmt.Println(bp_number, quality_level)
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
