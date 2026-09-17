import re
from typing import Dict, List, Match, Optional, Tuple

type BluePrint = Dict[str, Dict[str, int]]
type BluePrints = Dict[int, BluePrint]
type Spend = Dict[str, int]
type Spends = Dict[int, Spend]
type Robots = Dict[str, int]
type Resources = Dict[str, int]


def parse(filename: str) -> Tuple[Spends, BluePrints]:
    with open(filename, "r") as fp:
        raw_data: List[str] = fp.read().splitlines()

    blue_prints: BluePrints = {}
    max_spend: Spends = {}

    for line in raw_data:
        bp_re: Optional[Match[str]] = re.match(r"Blueprint (\d+):", line)
        if bp_re:
            blue_print_number: int = int(bp_re.group(1))

        ore_re: Optional[Match[str]] = re.search(
            r"Each ore robot costs (\d+) ore\.", line
        )
        if ore_re:
            ore_ore: int = int(ore_re.group(1))

        clay_re: Optional[Match[str]] = re.search(
            r"Each clay robot costs (\d+) ore\.", line
        )
        if clay_re:
            clay_ore: int = int(clay_re.group(1))

        obsidian_re: Optional[Match[str]] = re.search(
            r"Each obsidian robot costs (\d+) ore and (\d+) clay", line
        )
        if obsidian_re:
            obsidian_ore: int = int(obsidian_re.group(1))
            obsidian_clay: int = int(obsidian_re.group(2))

        geode_re: Optional[Match[str]] = re.search(
            r"Each geode robot costs (\d+) ore and (\d+) obsidian", line
        )
        if geode_re:
            geode_ore: int = int(geode_re.group(1))
            geode_obsidian: int = int(geode_re.group(2))

        blue_prints[blue_print_number] = {
            "geode": {"ore": geode_ore, "obsidian": geode_obsidian},
            "obsidian": {"ore": obsidian_ore, "clay": obsidian_clay},
            "clay": {"ore": clay_ore},
            "ore": {"ore": ore_ore},
        }

        max_spend[blue_print_number] = {
            "obsidian": geode_obsidian,
            "clay": obsidian_clay,
            "ore": max(ore_ore, clay_ore, obsidian_ore, geode_ore),
            "geode": float("inf"),  # type: ignore
        }

    return max_spend, blue_prints


def normalize_and_shrink(
    max_spend: Spend, robots: Robots, resources: Resources, minute: int
) -> None:
    for resource, amount in robots.items():
        if amount >= max_spend[resource]:
            robots[resource] = max_spend[resource]
            resources[resource] = min(resources[resource], max_spend[resource])

    for resource, amount in resources.items():
        resources[resource] = min(
            amount, minute * max_spend[resource] - robots[resource] * (minute - 1)
        )


def dfs(
    blue_print: BluePrint,
    max_spend: Spend,
    robots: Robots,
    resources: Resources,
    minute: int,
) -> int:
    memo: Dict[Tuple[int, ...], int] = {}

    def _dfs(minute: int, robots: Robots, resources: Resources) -> int:

        if minute == 0:
            return resources["geode"]

        # normalizing resources and robots
        normalize_and_shrink(max_spend, robots, resources, minute)

        # memoization
        key: Tuple[int, ...] = (minute, *robots.values(), *resources.values())
        if key in memo:
            return memo[key]

        # not building ---------------------------------------------------------
        new_resources: Resources = resources.copy()

        # produce
        for robot in robots:
            new_resources[robot] += robots[robot]

        new_resources_backup: Resources = new_resources.copy()

        max_geodes: int = _dfs(minute - 1, robots, new_resources)

        # Check if we can build ------------------------------------------------
        for resource, cost in blue_print.items():
            if robots[resource] >= max_spend[resource]:
                continue
            for element, quantity in cost.items():
                if resources[element] < quantity:
                    break
            else:
                # buy
                new_resources = new_resources_backup.copy()
                for element, quantity in cost.items():
                    new_resources[element] -= quantity

                # built
                new_force: Robots = robots.copy()
                new_force[resource] += 1

                max_geodes = max(
                    max_geodes,
                    _dfs(minute - 1, new_force, new_resources),
                )

        memo[key] = max_geodes
        return max_geodes

    return _dfs(minute, robots, resources)


def solve(max_spend: Spends, blue_prints: BluePrints, working_minutes: int) -> int:
    total_quality_level: int = 0
    robots: Robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
    start_resources: Resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}

    for bp_number, blue_print in blue_prints.items():
        quality_level = dfs(
            blue_print,
            max_spend[bp_number],
            robots,
            start_resources,
            working_minutes,
        )

        total_quality_level += quality_level * bp_number

    return total_quality_level


def solution(filename: str, working_minutes: int) -> int:
    max_spend, blue_prints = parse(filename)
    return solve(max_spend, blue_prints, working_minutes)


if __name__ == "__main__":
    print(solution("./example.txt", 24))  # 33
    print(solution("./input.txt", 24))  # 1294
