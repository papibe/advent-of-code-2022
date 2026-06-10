import re
from copy import deepcopy
from collections import deque
from typing import List, Dict, Deque, Set, Tuple

import heapq as hq


def parse(filename: str) -> List:
    with open(filename, "r") as fp:
        raw_data: str = fp.read().splitlines()

    blue_prints: Dict = {}
    max_spend: Dict = {}
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

        max_spend[blue_print_numer] = {
            "obsidian": geode_obsidian,
            "clay": obsidian_clay,
            "ore": max(ore_ore, clay_ore, obsidian_ore, geode_ore),
            "geode": float("inf"),
        }

    return max_spend, blue_prints


class Priority:
    def __init__(self, tup) -> None:
        minute, work_force, current_resources = tup
        self.minute = minute
        self.robots = work_force
        self.resources = current_resources
        self.priority: int = -(
            1000 * self.robots["geode"]
            + 100 * self.robots["obsidian"]
            + 10 * self.robots["clay"]
            + self.robots["ore"]
        )
        # self.priority: int = (
        #     1000 * self.resources["geode"]
        #     + 100 * self.resources["obsidian"]
        #     + 10 * self.resources["clay"]
        #     + self.resources["ore"]
        # )

    def __lt__(self, other) -> bool:
        return self.priority < other.priority


def get_key(minute, max_spend, work_force, resources) -> Tuple:
    new_resources = {}
    for resource, amount in resources.items():
        new_resources[resource] = min(max_spend[resource], amount)

    return tuple([minute, *work_force.values(), *new_resources.values()])
    # return tuple([minute, *work_force.values(), *resources.values()])


def solve(blue_print, max_spend, work_force, current_resources, working_minutes) -> int:

    tup = (0, work_force, current_resources)
    heap = [(Priority(tup), tup)]
    hq.heapify(heap)
    # queue: Deque = deque()
    # queue.append((0, work_force, current_resources))
    visited: Set = set()
    key = get_key(0, max_spend, work_force, current_resources)
    visited.add(key)

    max_geodes: int = 0
    finish_counter: int = 0
    saves: int = 0
    while heap:
        if len(heap) > 10_000_000:
            break
        _, tup = hq.heappop(heap)
        minute, work_force, current_resources = tup
        # print(minute, work_force, current_resources)

        if minute == working_minutes:
            # print(f'{current_resources["geode"] = }')
            max_geodes = max(max_geodes, current_resources["geode"])
            finish_counter += 1
            # if finish_counter > 100_000:
            #     print("max-recursion")
            #     break
            # return current_resources["geode"]
            continue

        # not building ---------------------------------------------------------
        # new_work_force = work_force.copy()
        new_current_resources = current_resources.copy()

        # produce
        for robot in work_force:
            new_current_resources[robot] += work_force[robot]

        key = get_key(minute + 1, max_spend, work_force, new_current_resources)
        if key in visited:
            # print("save", key)
            saves += 1
        else:
            visited.add(key)

            tup = (minute + 1, work_force, new_current_resources)
            hq.heappush(heap, (Priority(tup), tup))

        # Check if we can build ------------------------------------------------
        for resource, cost in reversed(blue_print.items()):
            for element, quantity in cost.items():
                if current_resources[element] < quantity:
                    break
            else:
                # print(f"building {resource}")
                new_work_force = work_force.copy()
                new_resources = current_resources.copy()
                # buy
                for element, quantity in cost.items():
                    new_resources[element] -= quantity
                # produce
                for robot in new_work_force:
                    new_resources[robot] += work_force[robot]
                # built
                new_work_force[resource] += 1

                key = get_key(minute + 1, max_spend, new_work_force, new_resources)
                if key in visited:
                    # print("save", key)
                    saves += 1
                    continue
                visited.add(key)

                tup = (minute + 1, new_work_force, new_resources)
                hq.heappush(heap, (Priority(tup), tup))

                # queue.append((minute + 1, new_work_force, new_current_resources))

    print(f"{saves = }")
    return max_geodes


def solution(filename: str, working_minutes: int) -> int:
    max_spend, blue_prints = parse(filename)
    # print(blue_prints)

    total_quality_level: int = 0
    for bp_number, blue_print in blue_prints.items():
        work_force = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        current_resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        quality_level = solve(
            blue_print,
            max_spend[bp_number],
            work_force,
            current_resources,
            working_minutes,
        )
        print(quality_level)
        total_quality_level += quality_level * bp_number
        # break

    return total_quality_level


if __name__ == "__main__":
    result: int = solution("./example.txt", 24)
    print(result)

    result = solution("./input.txt", 24)
    print(result)
