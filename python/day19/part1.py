import re
from copy import deepcopy
from collections import deque
from typing import List, Dict, Deque


class Collections:
    def __init__(self) -> None:
        self.minerals: Dict = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}

    def collect(self, mineral: str) -> None:
        self.minerals[mineral] += 1

    def __repr__(self) -> str:
        return f"{self.minerals}"


class Robot:
    def __init__(
        self, type_: str, collections: Collections = None, costs: Dict = None
    ) -> None:
        self.type: str = type_
        if collections is not None and costs is not None:
            for mineral, cost in costs.items():
                collections.minerals[mineral] -= cost

    def __repr__(self) -> str:
        return self.type


def parse(filename: str) -> List:
    with open(filename, "r") as fp:
        raw_data: str = fp.read().splitlines()

    blue_prints: Dict = {}
    for line in raw_data:
        bp_re = re.match(r"Blueprint (\d+):", line)
        blue_print_numer: int = int(bp_re.group(1))
        # print(blue_print_numer)

        ore_re = re.search(r"Each ore robot costs (\d+) ore\.", line)
        ore_ore: int = int(ore_re.group(1))
        # print(ore_ore)

        clay_re = re.search(r"Each clay robot costs (\d+) ore\.", line)
        clay_ore: int = int(clay_re.group(1))
        # print(clay_ore)

        obsidian_re = re.search(
            f"Each obsidian robot costs (\d+) ore and (\d+) clay", line
        )
        obsidian_ore: int = int(obsidian_re.group(1))
        obsidian_clay: int = int(obsidian_re.group(2))
        # print(obsidian_ore, obsidian_clay)

        geode_re = re.search(
            f"Each geode robot costs (\d+) ore and (\d+) obsidian", line
        )
        geode_ore: int = int(geode_re.group(1))
        geode_obsidian: int = int(geode_re.group(2))
        # print(geode_ore, geode_obsidian)

        blue_prints[blue_print_numer] = {
            "geode": {"ore": geode_ore, "obsidian": geode_obsidian},
            "obsidian": {"ore": obsidian_ore, "clay": obsidian_clay},
            "clay": {"ore": clay_ore},
            "ore": {"ore": ore_ore},
        }

    return blue_prints


def enough_resources(
    robot_type: str, collections: Collections, blue_print: Dict
) -> bool:
    # for robot, costs in blue_print.items():
    for mineral, cost in blue_print[robot_type].items():
        # print(mineral, cost, collections.minerals[mineral])
        # print(collections)
        if collections.minerals[mineral] < cost:
            return False
    return True


def solve2(blue_print: Dict, robots: List, working_minutes: int) -> int:
    collections: Collections = Collections()
    best_collections: Dict = {}

    queue: Deque = deque()
    queue.append((1, robots, collections))

    while queue:
        minute, robots, collections = queue.popleft()
        print(minute, robots, collections)
        if minute > working_minutes:
            continue
        if minute in best_collections:
            if collections.minerals["geode"] > best_collections[minute]:
                best_collections[minute] = collections.minerals["geode"]
            else:
                continue

        # build robots
        new_robots = []
        for robot_type in blue_print:
            current_collections: Collections = deepcopy(collections)
            current_robots: List[Robot] = deepcopy(robots)
            if enough_resources(robot_type, current_collections, blue_print):
                new_robots.append(
                    Robot(robot_type, current_collections, blue_print[robot_type])
                )
            else:
                continue

            # collect minerals
            for robot in current_robots:
                current_collections.collect(robot.type)

            current_robots.extend(new_robots)
            queue.append((minute + 1, current_robots, current_collections))

        # no build
        current_collections: Collections = deepcopy(collections)
        current_robots: List[Robot] = deepcopy(robots)

        for robot in current_robots:
            current_collections.collect(robot.type)

        queue.append((minute + 1, current_robots, current_collections))

    return best_collections[working_minutes]


def solve(blue_print: Dict, robots: List, working_minutes: int) -> int:
    collections: Collections = Collections()
    for minute in range(1, working_minutes + 1):
        print(f"== Minute: {minute} ==")
        # try to build robots
        new_robots = []
        for robot_name in blue_print:
            # print(f"Try to build {robot_name} robot")
            if enough_resources(robot_name, collections, blue_print):
                print(f"enough for {robot_name} robot")
                new_robots.append(
                    Robot(robot_name, collections, blue_print[robot_name])
                )
                pass

        # collect minerals
        for robot in robots:
            collections.collect(robot.type)
            print(f"{robot.type}-collecting robot collects {1} {robot.type}")

        robots.extend(new_robots)

        print("Minerals inventory", collections.minerals)
        print("Robots inventory", robots)

        print()

        # if minute == 3:
        #     break

    return collections.minerals["geode"]


def solution(filename: str, working_minutes: int) -> int:
    blue_prints: Dict = parse(filename)
    # print(blue_prints)

    total_quality_level: int = 0
    for _, blue_print in blue_prints.items():
        robots = [Robot("ore")]
        quality_level = solve2(blue_print, robots, working_minutes)
        # print(quality_level)
        total_quality_level += quality_level
        break

    return total_quality_level


if __name__ == "__main__":
    result: int = solution("./example.txt", 24)
    print(result)

    # result = solution("./input.txt", 24)
    # print(result)
