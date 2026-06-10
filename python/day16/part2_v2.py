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
    # history: Dict[str, int] = {"AAAA": 0}
    man_history: Dict[str, int] = {"AA": 0}
    elephant_history: Dict[str, int] = {"AA": 0}

    while queue:
        minute, current_pressure, man_valve, elephant_valve, opened = queue.popleft()
        print(minute, man_valve, elephant_valve, current_pressure)

        max_pressure = max(max_pressure, current_pressure)
        if minute >= max_minutes:
            continue

        # no valves open now; both walk to next valve
        for elephant_neighbor in valves[elephant_valve].neighbors:
            for man_neighbor in valves[man_valve].neighbors:
                if (
                    man_neighbor not in man_history
                    or current_pressure > man_history[man_neighbor]
                    or elephant_neighbor not in elephant_history
                    or current_pressure > elephant_history[elephant_neighbor]
                ):
                    if man_neighbor == elephant_neighbor:
                        continue

                    man_history[man_neighbor] = current_pressure
                    elephant_history[elephant_neighbor] = current_pressure
                    queue.append(
                        (
                            minute + 1,
                            current_pressure,
                            man_neighbor,
                            elephant_neighbor,
                            opened,
                        )
                    )

        # open elephant valve
        if valves[elephant_valve].flow > 0 and elephant_valve not in opened:
            current_pressure += valves[elephant_valve].flow * (max_minutes - minute - 1)
            new_opened = opened.copy()
            new_opened.add(elephant_valve)

            # both man and elephant open their valves
            if (
                man_valve != elephant_valve
                and valves[man_valve].flow > 0
                and man_valve not in opened
            ):
                current_pressure += valves[man_valve].flow * (max_minutes - minute - 1)
                new_opened.add(elephant_valve)
                # if (
                #     man_valve + elephant_valve not in history
                #     or current_pressure > history[man_valve + elephant_valve]
                # ):
                man_history[man_valve] = current_pressure
                elephant_history[elephant_valve] = current_pressure
                queue.append(
                    (
                        minute + 1,
                        current_pressure,
                        man_valve,
                        elephant_valve,
                        new_opened,
                    ),
                )

            # not open man valve
            else:
                # man walks to next vales
                for man_neighbor in valves[man_valve].neighbors:
                    if (
                        man_neighbor not in man_history
                        or current_pressure > man_history[man_neighbor]
                        or elephant_valve not in elephant_history
                        or current_pressure > elephant_history[elephant_valve]
                    ):
                        if man_neighbor == elephant_valve:
                            continue
                        man_history[man_neighbor] = current_pressure
                        elephant_history[elephant_valve] = current_pressure
                        queue.append(
                            (
                                minute + 1,
                                current_pressure,
                                man_neighbor,
                                elephant_valve,
                                new_opened,
                            )
                        )
        # not open elephant valve
        else:
            # open man valve
            if valves[man_valve].flow > 0 and man_valve not in opened:
                current_pressure += valves[man_valve].flow * (max_minutes - minute - 1)
                new_opened = opened.copy()
                new_opened.add(man_valve)
                # if minute == 8 and man_valve == "CC":
                # print(minute, f"opening1 {man_valve = } {elephant_valve = } {current_pressure = } {history = }")
                # print(minute, f"opengin2 {history[man_valve + elephant_neighbor] = }")

                for elephant_neighbor in valves[elephant_valve].neighbors:
                    if (
                        man_valve not in man_history
                        or current_pressure > man_history[man_valve]
                        or elephant_neighbor not in elephant_history
                        or current_pressure > elephant_history[elephant_neighbor]
                    ):
                        # if minute == 8 and man_valve == "CC":
                        #     print(minute, f"2opening {man_valve = } {elephant_valve = } {current_pressure = } {history = }")

                        if man_valve == elephant_neighbor:
                            continue

                        man_history[man_valve] = current_pressure
                        elephant_history[elephant_neighbor] = current_pressure
                        # print(minute, f"opening {man_valve = } {elephant_neighbor = } {current_pressure = } pushed")
                        queue.append(
                            (
                                minute + 1,
                                current_pressure,
                                man_valve,
                                elephant_neighbor,
                                new_opened,
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
