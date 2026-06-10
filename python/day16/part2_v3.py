import re
from collections import deque
from typing import List, Dict, Deque

from part1 import Valve, parse


def solve(valves: Dict[str, Valve], max_minutes: int) -> int:
    minute: int = 0
    queue: Deque = deque()
    # queue.append((minute, 0, "AA", "AA", set(["AA"])))
    queue.append((minute, 0, "AA", "AA", set(["AA"])))

    max_pressure: int = 0
    history: Dict[str, int] = {"AAAA": 0}
    # man_history: Dict[str, int] = {"AA": 0}
    # elephant_history: Dict[str, int] = {"AA": 0}

    while queue:
        minute, current_pressure, man_valve, elephant_valve, opened = queue.popleft()
        # print(minute, man_valve, elephant_valve, current_pressure)

        max_pressure = max(max_pressure, current_pressure)
        if minute >= max_minutes:
            continue

        # no valves open now; both walk to next valve
        for elephant_neighbor in valves[elephant_valve].neighbors:
            for man_neighbor in valves[man_valve].neighbors:
                if (
                    man_neighbor + elephant_neighbor not in history
                    or current_pressure > history[man_neighbor + elephant_neighbor]
                ):
                    if man_neighbor == elephant_neighbor:
                        continue

                    history[man_neighbor + elephant_neighbor] = current_pressure
                    history[elephant_neighbor + man_neighbor] = current_pressure
                    queue.append(
                        (
                            minute + 1,
                            current_pressure,
                            man_neighbor,
                            elephant_neighbor,
                            opened,
                        )
                    )

        new_opened: Dict = opened.copy()

        # open elephant valve
        if valves[elephant_valve].flow > 0 and elephant_valve not in opened:
            current_pressure += valves[elephant_valve].flow * (max_minutes - minute - 1)
            new_opened.add(elephant_valve)

        # open man valve
        if valves[man_valve].flow > 0 and man_valve not in opened:
            current_pressure += valves[man_valve].flow * (max_minutes - minute - 1)
            new_opened.add(man_valve)

        for elephant_neighbor in valves[elephant_valve].neighbors:
            for man_neighbor in valves[man_valve].neighbors:
                if (
                    man_neighbor + elephant_neighbor not in history
                    or current_pressure > history[man_neighbor + elephant_neighbor]
                ):
                    if man_neighbor == elephant_neighbor:
                        continue

                    history[man_neighbor + elephant_neighbor] = current_pressure
                    history[elephant_neighbor + man_neighbor] = current_pressure
                    queue.append(
                        (
                            minute + 1,
                            current_pressure,
                            man_neighbor,
                            elephant_neighbor,
                            opened,
                        )
                    )

    return max_pressure


def solution(filename: str, max_minutes: int) -> int:
    valves: Dict[Valve] = parse(filename)
    # for name, valve in valves.items():
    #     print(valve)

    return solve(valves, max_minutes)


if __name__ == "__main__":
    result: int = solution("./example.txt", 26)
    print(result)

    # result = solution("./input.txt", 26)
    # print(result)
