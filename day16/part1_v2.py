import re
from collections import deque
from typing import List, Dict, Deque


class Valve:
    def __init__(
        self, name: str, flow: int = None, neighbors: List[str] = None
    ) -> None:
        self.name: str = name
        self.flow: int = flow
        self.neighbors: List[str] = neighbors


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


def solve(valves: Dict[str, Valve]) -> int:
    queue: Deque = deque([(0, "AA", 0, set(["AA"]))])
    arriving_preassure: Dict[str, int] = {valve: -1 for valve in valves}
    arriving_preassure["AA"] = 0

    max_pressure: int = 0
    while queue:
        minute, valve, current_pressure, opened = queue.popleft()
        if minute > 30:
            continue

        max_pressure = max(max_pressure, current_pressure)

        # not open valve
        for neighbor in valves[valve].neighbors:
            if current_pressure > arriving_preassure[neighbor]:
                arriving_preassure[neighbor] = current_pressure
                queue.append((minute + 1, neighbor, current_pressure, opened))

        if valves[valve].flow > 0 and valve not in opened:
            # open valve
            minute += 1
            current_pressure += valves[valve].flow * (30 - minute)
            arriving_preassure[valve] = current_pressure

            new_opened = opened.copy()
            new_opened.add(valve)

            # walk to other valve
            minute += 1
            for neighbor in valves[valve].neighbors:
                if current_pressure > arriving_preassure[neighbor]:
                    arriving_preassure[neighbor] = current_pressure
                    queue.append((minute, neighbor, current_pressure, new_opened))

    return max_pressure


def solution(filename: str) -> int:
    valves: Dict[Valve] = parse(filename)
    return solve(valves)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    result = solution("./input.txt")
    print(result)
