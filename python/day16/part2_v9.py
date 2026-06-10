import itertools
import re
import sys
from collections import deque
from typing import List, Dict, Deque, Set, Tuple

class Valve:
    def __init__(
        self, name: str, flow: int = None, neighbors: List[str] = None
    ) -> None:
        self.name: str = name
        self.flow: int = flow
        self.neighbors: List[str] = neighbors

    # need it?
    def update_flow_and_neighbors(self, flow: int, neighbors: List[str]) -> None:
        self.flow: int = flow
        self.neighbors: List[str] = neighbors

    def __repr__(self) -> str:
        return f"name: {self.name}, flow: {self.flow}, neighbors: {self.neighbors}"


def parse(filename: str) -> Dict[str, Valve]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    valves: Dict[str, Valve] = {}
    pattern: str = r"Valve (\w+) has flow rate=(\d+); tunnels* leads* to valves* (.*)$"
    for line in data:
        match_expr = re.match(pattern, line)
        valve_name: str = match_expr.group(1)
        valve_flow: int = int(match_expr.group(2))
        connecting_valves: List[str] = [
            valve.strip() for valve in match_expr.group(3).split(",")
        ]

        valves[valve_name] = Valve(valve_name, valve_flow, connecting_valves)

    return valves


def solve2(
    valves: Dict[str, Valve], opened_valves_setup: Set[str], max_minutes: int
) -> int:
    minute: int = 0
    queue: Deque = deque()

    max_pressure: int = 0
    history: Dict[str, int] = {valve: -1 for valve in valves}
    queue.append((minute, "AA", 0, history, opened_valves_setup))

    state: Set = set([(minute, "AA", frozenset())])
    history["AA"] = 0

    while queue:
        minute, valve, current_pressure, history, opened = queue.popleft()
        # new_history: Dict = history.copy()
        # new_history[valve] = max(new_history[valve], current_pressure)
        # print(minute, valve, current_pressure)
        # print(new_history)
        # print()
        max_pressure = max(max_pressure, current_pressure)
        if minute > max_minutes:
            # print("reached 30!")
            # break
            # print(opened)
            continue
        # max_pressure = max(max_pressure, current_pressure)

        # not open valve
        for neighbor in valves[valve].neighbors:
            if True or current_pressure > history[neighbor]:
                new_history: Dict = history.copy()
                new_history[neighbor] = current_pressure
                next_state: Tuple = (minute + 1, neighbor, frozenset(opened))
                if next_state in state:
                    # print("save")
                    pass
                else:
                    state.add(next_state)
                    queue.append(
                        (minute + 1, neighbor, current_pressure, new_history, opened)
                    )
            # else:
            #     print("save using preasure")

        if valves[valve].flow > 0 and valve not in opened:
            new_current_pressure = current_pressure + valves[valve].flow * (
                30 - minute - 1
            )
            new_opened = opened.copy()
            new_opened.add(valve)

            new_history_2: Dict = history.copy()
            new_history_2[valve] = new_current_pressure

            next_state_2: Tuple = (minute + 1, valve, frozenset(new_opened))
            if next_state_2 in state:
                # print("save")
                pass
            else:
                state.add(next_state_2)
                queue.append(
                    (minute + 1, valve, new_current_pressure, new_history_2, new_opened)
                )

            # print(minute, valve, current_pressure, f"{valve} opened")

            # minute += 1  # walk to other valve
            # for neighbor in valves[valve].neighbors:
            #     if neighbor not in history or current_pressure > history[neighbor]:
            #         history[neighbor] = current_pressure
            #         queue.append((minute, neighbor, current_pressure, new_opened))

    return max_pressure


def solve(
    valves: Dict[str, Valve],
    valve_index: Dict,
    opened_valves: int,
    memo: Dict,
    max_minutes: int,
) -> int:
    def sol(minutes: int, valve: str, opened: Set):
        if minutes == 0:
            return sol(26, "AA", opened)


        if (minutes, valve, opened) in memo:
            return memo[(minutes, valve, opened)]

        max_pressure = max(
            [sol(minutes - 1, neighbor, opened) for neighbor in valves[valve].neighbors]
        )

        if valves[valve].flow > 0:
            valve_bit = 1 << valve_index[valve]
            if opened & valve_bit == 0:  # not opened
                max_pressure = max(
                    max_pressure,
                    valves[valve].flow * (minutes - 1)
                    + sol(minutes - 1, valve, opened | valve_bit),
                )

        memo[(minutes, valve, opened)] = max_pressure
        return max_pressure

    return sol(max_minutes, "AA", opened_valves)


def solution(filename: str) -> int:
    valves: Dict[Valve] = parse(filename)

    good_valves = [valve for valve in valves if valves[valve].flow > 0]
    valve_index: Dict[str, int] = {valve: i for i, valve in enumerate(good_valves)}

    memo: Dict = {}

    return solve(valves, valve_index, 0, memo, 26)


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(32000)
    print(sys.getrecursionlimit())
    # exit(11)
    result: int = solution("./example.txt")
    print(result)

    # result = solution("./input.txt")
    # print(result)
