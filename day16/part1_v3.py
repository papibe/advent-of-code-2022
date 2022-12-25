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


def solve(valves: Dict[str, Valve]) -> int:
    minute: int = 0
    queue: Deque = deque()
    queue.append((minute, "AA", 0, set(["AA"]), {"AA": 0}, []))

    max_pressure: int = 0

    while True:
        minute, valve, current_pressure, opened, history, path = queue.popleft()
        new_path: List[str] = path[:]
        new_path.append(valve)
        print(minute, valve, current_pressure, path)
        if minute > 30:
            max_pressure = max(max_pressure, current_pressure)
            break

        old_pressure = current_pressure
        old_opened = opened

        if valves[valve].flow > 0 and valve not in opened:
            minute += 1  # open valve
            current_pressure += valves[valve].flow * (30 - minute)
            new_opened = opened.copy()
            new_opened.add(valve)
            opened = new_opened
            print(minute, valve, current_pressure, new_path, "opened")

        minute += 1  # walk to other valve
        for neighbor in valves[valve].neighbors:
            if neighbor not in history or current_pressure > history[neighbor]:
                new_history: Dict = history.copy()
                new_history[neighbor] = current_pressure
                queue.append(
                    (minute, neighbor, current_pressure, opened, new_history, new_path)
                )

        for neighbor in valves[valve].neighbors:
            if neighbor not in history or old_pressure > history[neighbor]:
                new_history: Dict = history.copy()
                new_history[neighbor] = old_pressure
                queue.append(
                    (minute, neighbor, old_pressure, old_opened, new_history, new_path)
                )

    return max_pressure


def solution(filename: str) -> int:
    valves: Dict[Valve] = parse(filename)
    # for name, valve in valves.items():
    #     print(valve)

    return solve(valves)


if __name__ == "__main__":
    result: int = solution("./example.txt")
    print(result)

    # result = solution("./input.txt")
    # print(result)
