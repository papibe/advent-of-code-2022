import re
from copy import deepcopy
from collections import deque
from typing import List, Dict, Deque, Set

import heapq as hq


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


class Priority:
    def __init__(self, minute, work_force, current_resources) -> None:
        self.minute = minute
        self.robots = work_force
        self.resources = current_resources

    def __lt__(self, other) -> bool:
        if self.resources["geode"] < other.resources["geode"]:
            return True
        if self.resources["geode"] > other.resources["geode"]:
            return False
        if self.robots["geode"] < other.robots["geode"]:
            return True
        if self.robots["geode"] > other.robots["geode"]:
            return True

        if self.resources["obsidian"] < other.resources["obsidian"]:
            return True
        if self.resources["obsidian"] > other.resources["obsidian"]:
            return False
        if self.robots["obsidian"] < other.robots["obsidian"]:
            return True
        if self.robots["obsidian"] > other.robots["obsidian"]:
            return True

        if self.resources["clay"] < other.resources["clay"]:
            return True
        if self.resources["clay"] > other.resources["clay"]:
            return False
        if self.robots["clay"] < other.robots["clay"]:
            return True
        if self.robots["clay"] > other.robots["clay"]:
            return True

        if self.resources["ore"] < other.resources["ore"]:
            return True
        if self.resources["ore"] > other.resources["ore"]:
            return False
        if self.robots["ore"] < other.robots["ore"]:
            return True
        if self.robots["ore"] > other.robots["ore"]:
            return True

        return False


def solve(blue_print, work_force, current_resources, working_minutes) -> int:
    queue: Deque = deque()
    queue.append((0, work_force, current_resources))
    visited: Set = set()
    key = tuple([0, *work_force, *current_resources])
    visited.add(key)

    while queue:
        minute, work_force, current_resources = queue.popleft()
        if minute == working_minutes:
            print(f'{current_resources["geode"] = }')
            # return current_resources["geode"]

        # not building ---------------------------------------------------------
        new_work_force = work_force.copy()
        new_current_resources = current_resources.copy()

        # produce
        for robot in new_work_force:
            new_current_resources[robot] += work_force[robot]

        key = tuple([minute + 1, *work_force.values(), *current_resources.values()])
        if key in visited:
            # print("save", key)
            continue
        visited.add(key)

        queue.append((minute + 1, new_work_force, new_current_resources))

        # Check if we can build ------------------------------------------------
        for resource, cost in blue_print.items():
            for element, quantity in cost.items():
                if current_resources[element] < quantity:
                    break
            else:
                new_work_force = work_force.copy()
                new_current_resources = current_resources.copy()
                # buy
                for element, quantity in cost.items():
                    new_current_resources[element] -= quantity
                # produce
                for robot in new_work_force:
                    new_current_resources[robot] += work_force[robot]
                # built
                new_work_force[resource] += 1

                key = tuple(
                    [minute + 1, *work_force.values(), *current_resources.values()]
                )

                if key in visited:
                    # print("save", key)
                    continue
                visited.add(key)

                queue.append((minute + 1, new_work_force, new_current_resources))


def solution(filename: str, working_minutes: int) -> int:
    blue_prints: Dict = parse(filename)
    # print(blue_prints)

    total_quality_level: int = 0
    for bp_number, blue_print in blue_prints.items():
        work_force = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        current_resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        quality_level = solve(
            blue_print, work_force, current_resources, working_minutes
        )
        print(quality_level)
        total_quality_level += quality_level * bp_number
        # break

    return total_quality_level


if __name__ == "__main__":
    result: int = solution("./example.txt", 24)
    print(result)

    # result = solution("./input.txt", 24)
    # print(result)
