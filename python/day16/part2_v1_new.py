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
    queue: Deque = deque()
    queue.append((0, "AA", 0, set()))  # minute, valve (position), opened valves
    # queue.append((0, "AA", 0, {"AA": 0}, set()))  # minute, valve (position), opened valves

    max_pressure: int = 0
    # history: Dict[str, int] = {"AA": 0}

    history: Dict[str, int] = {valve: -1 for valve in valves}
    history["AA"] = 0
    # print(history)

    while queue:
        minute, valve, current_pressure, opened = queue.popleft()
        # print(minute, valve, opened)

        if minute > 30:
            print(f"reached last minute {max_pressure = }")
            # break
            continue
        max_pressure = max(max_pressure, current_pressure)

        # not open valve
        for neighbor in valves[valve].neighbors:
            if current_pressure > history[neighbor]:
                # new_history: Dict = history.copy()
                # new_history[neighbor] = current_pressure
                history[neighbor] = current_pressure
                queue.append((minute + 1, neighbor, current_pressure, opened))

        if valves[valve].flow > 0 and valve not in opened:
            # minute += 1  # open valve
            current_pressure += valves[valve].flow * (30 - minute - 1)
            new_opened = opened.copy()
            new_opened.add(valve)

            # newer_history: Dict = history.copy()
            # newer_history[valve] = current_pressure
            history[valve] = current_pressure

            queue.append((minute + 1, valve, current_pressure, new_opened))

            # print(minute, valve, current_pressure, f"{valve} opened")

            # minute += 1  # walk to other valve
            # for neighbor in valves[valve].neighbors:
            #     if neighbor not in history or current_pressure > history[neighbor]:
            #         history[neighbor] = current_pressure
            #         queue.append((minute, neighbor, current_pressure, new_opened))

    return max_pressure


def solution(filename: str) -> int:
    valves: Dict[Valve] = parse(filename)
    # for name, valve in valves.items():
    #     print(valve)

    return solve(valves)


if __name__ == "__main__":
    # result: int = solution("./example.txt")
    # print(result)

    result = solution("./input.txt")
    print(result)
